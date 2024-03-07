import sys
import socket
from functools import cache
from urllib.parse import urlparse
import validators


@cache
async def scan_port(url: str, port: int) -> str:
	"""Асинхронная функция сканирования порта.

	Аргументы:
	 + url: str - URL адрес
	+ port: int - порт
	""" 
	# Валидация URL
	if validators.url(url):
		# Создание сокета и его настройка
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.settimeout(1)
		client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		# Получаем IP адрес
		ip = socket.gethostbyname(urlparse(url).hostname)

		# Проверка подключения по порту
		if client.connect_ex((ip, port)):
			return f'{ip}:{port} закрыт'
		else:
			return f'{ip}:{port} открыт'

		# Закрываем сокет
		client.close()
	else:
		# URL не прошел валидацию
		msg = f'Критическая ошибка: URL {url} не прошел валидацию'
		print(msg)
		sys.exit()
		return msg
