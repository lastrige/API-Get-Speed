from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from get_speed_page import get_speed_page

from statistics import mean

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:yourpass@localhost/sites_perf'  # Введите свой пароль
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.create_all()


class Measurements(db.Model):
    __tablename__ = 'sites_perf'
    id = db.Column(db.Integer, primary_key=True)
    web_page = db.Column(db.String(50))
    load_speed = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now())

    def init(self, web_page, load_speed, date):
        self.web_page = web_page
        self.load_speed = load_speed
        self.date = date


twenty_four_hours = timedelta(seconds=5)  # Переменная, для определения промежутков времени между добавлениями в БД


@app.route("/search", methods=['GET'])  # Ручка, отвечающая за замер и отправку в БД
def search():
    query_params = request.args
    site_name = query_params.get('url')
    all_rows = Measurements.query.all()

    returned_result = None  # Заглушки, для избежания дублирования кода
    need_add_to_db = False

    if len(all_rows) > 0:
        current_site_rows = Measurements.query.filter(
            Measurements.web_page == site_name).all()

        if len(current_site_rows) > 0:  # Проверка на пустоту в БД ,на наличие нужных нам колонок
            current_site = current_site_rows[-1]
            last_site_speed = current_site.load_speed
            last_site_data = current_site.date
            if datetime.now() - last_site_data <= twenty_four_hours:  # Установка временных рамок
                returned_result = last_site_speed
            else:
                need_add_to_db = True
        else:
            need_add_to_db = True
    else:
        need_add_to_db = True

    if need_add_to_db:
        speed_page = get_speed_page(site_name)

        if type(speed_page) != str:
            measure = Measurements(web_page=site_name,
                                   load_speed=speed_page,
                                   date=datetime.now())
            db.session.add(measure)
            db.session.commit()  # Добавление в БД при соблюдении условий

        returned_result = speed_page

    return str(returned_result)


@app.route("/search/stats", methods=['GET'])  # Ручка отвечающая за выборку сайтов в рамках переданного периода времени
def stats():
    query_params = request.args
    from_date = datetime.fromisoformat(query_params.get('from'))
    to_date = datetime.fromisoformat(query_params.get('to'))

    rows = Measurements.query.filter(Measurements.date >= from_date, Measurements.date <= to_date).all()

    group_by_site_name = {}
    result = {}

    for row in rows:
        key = row.web_page
        value = row.load_speed

        if key in group_by_site_name:
            group_by_site_name[key] = [*group_by_site_name[key], value]
        else:
            group_by_site_name[key] = [value]  # Фильтрация нужных нам данных и добавление в пустой словарь

    for row in group_by_site_name:
        values = group_by_site_name[row]
        result[row] = mean(values) # Среднее значение скорости из полученных данных

    return result


if __name__ == '__main__':
    app.run()
