# **Backend-сервис,замеряющий среднюю скорость сайта и выводящий среднюю скорость загрузки.**
* ## Api метод, позволяющий замерять скорсть загрузки Web-страницы и записывать результат в БД. Есть возможность ограничения на добавление данных, по времени.
  * ### Пример http://127.0.0.1:5000/search?url=https://www.ya.ru/ 
* ## Api метод, возвращающий среднее время загрузки для каждого сайта за переданный период времени.
  * ### Пример http://127.0.0.1:5000/search/stats?from=2022-02-10&to=2022-02-20
  
# **Установка зависимостей.**
* ## Активируйте виртуальное окружение 
* ## Перейдите в корневой каталог проекта
* ## Убедитесь,что у вас установленны все пакеты, как в файле - _requirements.txt_ (воспользуйтесь командой: _pip install -r requirements.txt_)
# **Подключение к БД**
* ## Скачайте PgAdmin(интерфейс для PostgreSql)
* ## Создайте БД(sites_perf)
* ## В корневом файле(app.py)запустите Python консоль и передайте методы для создания нужных таблиц.
  * ###  1)_from app import db_
  * ###  2)_db.create_all()_

## P.s 
* ### Более подробная информация по отдельным функциям и логике, находится в коментариях к коду.