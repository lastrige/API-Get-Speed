import requests
import json


def get_speed_page(site_name):# Функция, замеряющая скорость загрузки
    try:
        req_data = requests.get('https://www.googleapis.com/pagespeedonline/v5/runPagespeed',
                                params={'url': site_name, 'key': 'AIzaSyAxoQf3LrNK3UkSk07w8KCCgFo3uKFVO_0'})
        req_data.raise_for_status()
        req_json = req_data.json()
        return req_json["lighthouseResult"]["audits"]["speed-index"]["numericValue"]
    except requests.exceptions.HTTPError as ex:
        return json.loads(ex.response.text)["error"]['errors'][0]['message']

