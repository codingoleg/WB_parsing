import json

import requests
import pandas
import xlsxwriter

URL = 'https://www.wildberries.ru/webapi/spa/modules/pickups'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
    "x-requested-with": "XMLHttpRequest"
}


def get_pickups(url: str) -> list:
    data = requests.get(url, headers=HEADERS).json()
    pickups = []

    with open('pickups.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    with open('pickups.json', encoding='utf-8') as file:
        data = json.load(file)
        for pickup in data['value']['pickups']:
            pickup['latitude'], pickup['longitude'] = pickup["coordinates"]
            del pickup["coordinates"]
            pickups.append(pickup)

    return pickups


def write_to_xlsx(data: list) -> None:
    df = pandas.DataFrame(data)

    with pandas.ExcelWriter('pickups.xlsx', engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)


if __name__ == '__main__':
    pickups = get_pickups(URL)
    write_to_xlsx(pickups)
