# Python HTTP-server backend

## Запуск сервера

Перейдите в директорию проекта. Сервер запускается командой:

```sh
python3 script.py
```

После отображения сообщения
```sh
Server hosted on 127.0.0.1:8000
```
сервер готов к обработке запросов.

>Note: Для запуска сервера на другом IP/Порту необходимо внести правки в settings.py

## API

Описание API также находится по ссылке на [swaggerhub.com](https://app.swaggerhub.com/apis/twilightKnight/Python_HTTP-server_backend/1.0.0 "Перейти на сайт")

Все описанные ниже методы в качестве ответа отображают на странице JSON объект или ошибку.

### Метод /get_city_by_id/{geonameid}

Данный метод принимает идентификатор geonameid города и возвращает всю информацию о нем.
+ В случае, если метка задана некорректно (не числовым значением),  метод вернет ошибку 400.
+ В случае, если идентификатор не был найден, метод вернет ошибку 404.

**Пример запроса**
```sh
http://127.0.0.1:8000/get_city_by_id/453417
```

*Пример ответа*
```sh
{'geonameid': '453417', 'name': 'Perechevskiy', 'asciiname': 'Perechevskiy', 'alternatenames': 'Perechevskij,Perechevskiy,Перечевский', 'latitude': '57.56819', 'longitude': '33.7828', 'feature_class': 'H', 'feature_code': 'STM', 'country_code': 'RU', 'cc2': '', 'admin1_code': '77', 'admin2_code': '', 'admin3_code': '', 'admin4_code': '', 'population': '0', 'elevation': '', 'dem': '196', 'timezone': 'Europe/Moscow', 'modification_date': '2020-01-08'}
```

### Метод /load_page/{pageinfo}

Данный метод принимает строку типа "page_number&amount_of_cities_per_page" и возвращает города с информацией о них.
+ В случае, если номер страницы или количество городов задано некорректно, метод вернет ошибку 400.

**Пример запроса**
```sh
http://127.0.0.1:8000/load_page/5000&2
```

*Пример ответа*
```sh
{"City №1": {'geonameid': '470422', 'name': 'Stantsiya Vympel', 'asciiname': 'Stantsiya Vympel', 'alternatenames': '', 'latitude': '51.31667', 'longitude': '47.95', 'feature_class': 'S', 'feature_code': 'RSTN', 'country_code': 'RU', 'cc2': '', 'admin1_code': '67', 'admin2_code': '', 'admin3_code': '', 'admin4_code': '', 'population': '0', 'elevation': '', 'dem': '106', 'timezone': 'Europe/Saratov', 'modification_date': '1994-04-09'}, "City №2": {'geonameid': '470423', 'name': 'Vymovo', 'asciiname': 'Vymovo', 'alternatenames': 'Vymovo,Вымово', 'latitude': '60.04141', 'longitude': '32.81836', 'feature_class': 'P', 'feature_code': 'PPL', 'country_code': 'RU', 'cc2': '', 'admin1_code': '42', 'admin2_code': '472711', 'admin3_code': '', 'admin4_code': '', 'population': '0', 'elevation': '', 'dem': '40', 'timezone': 'Europe/Moscow', 'modification_date': '2016-09-08'}, }
```


### Метод /compare/{cities}

Данный метод принимает строку типа "city1_name&city2_name" и возвращает города с информацией о них, а также, какой город расположен севернее, и различия временной зоны в часах.
+ В случае, если один из городов не будет найден, метод вернет ошибку 404.

**Пример запроса**
```sh
http://127.0.0.1:8000/compare/Озеро Бабошкина&Bol’shoy Darpuk
```

*Пример ответа*
```sh
{'North_most_city': 'Озеро Бабошкина', 'timezone_difference': '6.0', 'City №1': {'geonameid': '6693358', 'name': 'Озеро Бабошкина', 'asciiname': 'Ozero Baboshkina', 'alternatenames': 'Baboshkina', 'latitude': '55.81124', 'longitude': '37.98562', 'feature_class': 'H', 'feature_code': 'LK', 'country_code': 'RU', 'cc2': '', 'admin1_code': '', 'admin2_code': '', 'admin3_code': '', 'admin4_code': '', 'population': '0', 'elevation': '', 'dem': '148', 'timezone': 'Europe/Moscow', 'modification_date': '2008-06-15'}, 'City №2': {'geonameid': '7840262', 'name': 'Bol’shoy Darpuk', 'asciiname': "Bol'shoy Darpuk", 'alternatenames': "Bol'shoj Darpuk,Bol'shoy Darpuk,Bol’shoy Darpuk,Большой Дарпук", 'latitude': '54.67372', 'longitude': '121.7526', 'feature_class': 'H', 'feature_code': 'STM', 'country_code': 'RU', 'cc2': '', 'admin1_code': '93', 'admin2_code': '', 'admin3_code': '', 'admin4_code': '', 'population': '0', 'elevation': '', 'dem': '716', 'timezone': 'Asia/Chita', 'modification_date': '2016-10-16'}}
```

### Метод /autofill/{city}

Метод принимает неполное название города и возвращает возможные варинты продолжения. Количество вариантов задается параметром MAX_AMOUNT_OF_CITY_NAMES_FOR_AUTOFILL в settings.py.
+ В случае, если ни одно подходящее название не было найдено, метод вернет ошибку 404.

**Пример запроса**
```sh
http://127.0.0.1:8000/autofill/Озеро Малое
```

*Пример ответа*
```sh
{'most_similar_cities': ['Озеро Малое Пестино', 'Озеро Малое Пертешно', 'Озеро Малое Искровно', 'Озеро Малое Турали', 'Озеро Малое Замошенское']}
```
