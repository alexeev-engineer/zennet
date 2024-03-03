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
	if validators.url(url):
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.settimeout(1)
		client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		ip = socket.gethostbyname(urlparse(url).hostname)

		if client.connect_ex((ip, port)):
			return f'{ip}:{port} закрыт'
		else:
			return f'{ip}:{port} открыт'

		client.close()
	else:
		msg = f'Критическая ошибка: URL {url} не прошел валидацию'
		print(msg)
		sys.exit()
		return msg
