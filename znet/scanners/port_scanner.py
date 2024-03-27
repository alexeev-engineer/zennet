#! venv/bin/python3
"""Zennet.

Blazing fast tool for network traffic analysis and working with network protocols
Copyright (C) 2024  Alexeev Bronislav
License: BSD 3-Clause
Link: https://github.com/alexeev-engineer/zennet.

Contacts: bro.alexeev@inbox.ru, t.me/alexeev_dev

"""
import sys
import socket
from functools import cache
from urllib.parse import urlparse
import validators


@cache
async def scan_port(url: str, port: int) -> str:
	"""Scan one port.

	Arguments:
	---------
	 + url: str - url address
	 + port: int - port for scan
	
	""" 
	if validators.url(url):
		# Create socket
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.settimeout(1)
		client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		# Get IP address
		ip = socket.gethostbyname(urlparse(url).hostname)

		# Try connect
		if client.connect_ex((ip, port)):
			return f'{ip}:{port} closed'
		else:
			return f'{ip}:{port} opened'

		# Close socket
		client.close()
	else:
		msg = f'Critical error: invalid URL {url}'
		sys.exit()
		return msg
