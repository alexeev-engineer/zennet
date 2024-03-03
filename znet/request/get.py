from functools import cache
from urllib.parse import urlparse
import socket
import ssl
import validators
from icecream import ic


@cache
async def send_request_get(url: str, timeout: int=1):
	"""Асинхронная функция отправки HTTP get запроса.

	Аргументы:
	 + url: str - URL адрес
	 + timeout: int=1 - таймаут
	"""
	status_code = None
	headers = None
	content = None
	text = None
	path = None
	request = f"GET {path} HTTP/1.1\r\nHost:{url}\r\n\r\n"

	if ":" in urlparse(url).netloc:
		# Если порт написан прямо (например 127.0.0.1:8000)
		#                                            ^^^^^
		port = int(str(urlparse(url).netloc).split(":")[-1])
	else:
		# 80 - HTTP, 443 - HTTPS
		port = 80 if urlparse(url).scheme == "http" else 443

	if not urlparse(url).path:
		# Если путя нету, то корневой каталог
		path = "/"
	else:
		# Получаем путь
		if "?" in url:
			key = f'?{url.split("?")[-1]}'
			path = f'{urlparse(url).path}{key}'
		else:
			path = urlparse(url).path

	timeout = (timeout, timeout)

	# Проверка URL
	if validators.url(url):
		host = urlparse(url).hostname
		request = f"GET {path} HTTP/1.1\r\nHost:{host}\r\n\r\n"

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(timeout[0])
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		response = b""

		try:
			# Подключаемся к серверу
			sock.connect((socket.gethostbyname(host), port))

			if port == 443:
				# Создаем SSL соединение, если порт 443 (https)
				context = ssl.create_default_context()
				sock = context.wrap_socket(sock, server_hostname=host)
			
			sock.sendall(request.encode())
			sock.settimeout(timeout[1])

			while True:
				data = sock.recv(1024)
				response += data
				if b'\r\n0\r\n\r\n' in data:
					break
				elif b'\r\n\r\n' in data:
					break
				elif not data:
					break

			if response:
				status_code = int("".join(response.decode().split('\r\n\r\n')[0].splitlines()[0].split()[1]))
				headers = dict()
				async for head in response.decode().split('\r\n\r\n')[0].splitlines()[1:]:
					headers.update({head.split(": ")[0]: head.split(": ")[1]})
				if port == 80:
					content = response.decode().split('\r\n\r\n')[1].split("\r\n")[1].encode()
				else:
					content = response.decode().split('\r\n\r\n')[1].encode()

				if port == 80:
					text = response.decode().split('\r\n\r\n')[1].split("\r\n")[1]
				else:
					text = response.decode().split('\r\n\r\n')[1]

			sock.close()
		except Exception as ex:
			sock.close()
			return [f'Ошибка: {ex}', 0, 0, 0, 0]
		else:
			request = request.replace('\n', ' ').replace('\r', ' ').strip()
			ic(request)
			ic(status_code)
			return [f"{request}", status_code, headers, content.decode(), text]
	else:
		return ['Ошибка: URL не прошел валидацию', 0, 0, 0, 0]

