# zennet ⚡️
Молниеносно быстрая и многофункциональная консольная программа для анализа сетевого трафика

## Преимущества zennet ⚡️
Программа zennet невероятно быстра, благодаря оптимизированным вычислениям, асинхронному подходу и многопоточности.

Также в zennet есть красивый вывод данных и сохранение логов в файл (формат markdown) из коробки.

## Сравнение скорости ⚡️
Функции zenmap более быстрые, чем функции из стандартных библиотек Python

### Отправка GET-запроса при помощи стандартной requests и zenmap ⚡️
Запрос при помощи стандартной библиотеки отправляется примерно за ~0.027 секунд

```python
# стандартная библиотека requests
import requests
from time import perf_counter

start = perf_counter()
requests.get('http://127.0.0.1:8000/login')
end = perf_counter()
total = round(end - start, 4)
print(total)

>>> 0.0277
```

А при помощи zenmap скорость выросла примерно в 138 раз!

```bash
# Отправляем http get запрос на 127.0.0.1:8000/login и сохраняем вывод в localhost_login_zennet.md
 $ python3 zennet.py --get --url http://127.0.0.1:8000/login -o localhost_login_zennet.md

>>> zennet v 0.2.2 @ alexeev-engineer
    GET /login HTTP/1.1 Host:127.0.0.1  
    ├── Код ответа:2 0 0
    ├── Заголовок ответа: {'Server': 'Werkzeug/3.0.1 Python/3.12.1', 'Date': 'Sun, 
    │   25 Feb 2024 16:17:43 GMT', 'Content-Type': 'text/html; charset=utf-8', 
    │   'Content-Length': '1549', 'Vary': 'Cookie', 'Connection': 'close'}
    ├── Время выполнения запроса: 0.0002
    └── Весь лог сохранен в localhost_login_zennet.md
    Время исполнения программы: 0.275 сек
```

## Установка ⚡️
Для установки у вас должен стоять Python >=3.9, pip и git.

```bash
git clone https://github.com/alexeev-engineer/zennet.git 			# Клонирование репозитория
cd zennet															# Переход в директорию с проектом
python3 -m venv venv												# Создание виртуального окружения
source venv/bin/activate											# Активация виртуального окружения
pip3 install -r requirements.txt									# Установка зависимостей
```

## Документация ⚡️
Вы можете получить документацию по использованию zennet по [этой ссылке](./docs/index.md)

## Поддержка ⚡️
Если вы обнаружили ошибку или хотите предложить что-то свое, то создайте [issue](https://github.com/alexeev-engineer/zennet/issues/new).
