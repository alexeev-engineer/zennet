import sys
import socket
from functools import cache
from urllib.parse import urlparse
import validators


@cache
async def scan_port(url, port):
	if validators.url(url):
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		ip = socket.gethostbyname(urlparse(url).hostname)
		if client.connect_ex((ip, port)):
			return f'{ip}:{port} закрыт'
		else:
			return f'{ip}:{port} открыт'
	else:
		print(f'Критическая ошибка: URL {url} не прошел валидацию')
		sys.exit()
