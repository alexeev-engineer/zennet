#! venv/bin/python3
"""Blazing fast tool for network traffic analysis and working with network protocols
Copyright (C) 2024  Alexeev Bronislav
License: BSD 3-Clause
Link: https://github.com/alexeev-engineer/zennet.

Contacts: bro.alexeev@inbox.ru, t.me/alexeev_dev

"""
import argparse
from functools import cache
from time import monotonic
from rich import print
from rich.tree import Tree
from paintlog.logger import pydbg_obj, Logger
from tqdm.asyncio import tqdm
import asyncio

# Модули
from znet.request.get import send_request_get
from znet.scanners.port_scanner import scan_port
from znet.osint.whois import *

logger = Logger('zennet.log')
__version__ = '0.3.3'


@cache
def write_to_file(filename: str, data: str) -> None:
	"""Write output to file.

	Arguments:
	---------
	 + filename: str - filename
	 + data: str - output
	
	"""
	pydbg_obj(filename)

	with open(filename, 'w') as file:
		file.write(data)


@cache
async def send_get(url: str, timeout: int, output: str) -> None:
	"""Create task for sending get request.

	Arguments:
	---------
	 + url: str - url address
	 + timeout: int - timeout for connecting
	 + output: str - filename for output data
	
	"""
	pydbg_obj(url)
	logger.log(f'Send HTTP-get request on {url}', 'info')
	task = asyncio.create_task(send_request_get(url, timeout))
	data = await asyncio.gather(task)

	data_tree = Tree(f"[yellow]{data[0][0]}")
	data_tree.add(f"[cyan]Response code:{data[0][1]}")
	data_tree.add(f"[cyan]Headers: {data[0][2]}")
	data_tree.add(f'[italic]Log saved in {output}')

	data = f'''Report on sending a GET request to a {url}
# Request: {data[0][0]})
Response code: `{data[0][1]}`\n
Headers: `{data[0][2]}`\n
Content:

```html
{data[0][3]}```

Response text:

```html
{data[0][4]}
```

Report generated by [zennet ⚡️](https://github.com/alexeev-engineer/zennet)
'''
	
	write_to_file(output, data)
	print(data_tree)


@cache
async def start_port_scanner(url: str, ports: str, max_ports: int, output: str) -> None:
	"""Start port scanner.

	Arguments:
	---------
	 + url: str - url address
	 + ports: str - list of ports for scanning
	 + max_ports: int - count of max ports for scanning)
	 + output: str - filename for output data
	
	"""
	logger.log(f'Start scanning {url}', 'info')
	text = f'# Result of scanning URL {url}:\n'
	tasks = []
	available_ports = []

	# Если порты были указаны напрямую, а не просто максимальное число для сканироваия портов
	if ports:
		# Разделяем список портов
		async for port in tqdm(ports.split(' '), desc='Create tasks', ascii=False, 
								unit='task', smoothing=0.5, colour='blue', 
								bar_format='{desc}: {percentage:3.0f}%| {bar} | {n_fmt}/{total_fmt} {rate_fmt}{postfix}'):
			# Добавляем в список задач цель сканировать порт
			tasks.append(asyncio.create_task(scan_port(url, int(port))))
	else:
		# Если указано максимальное число для сканирования портов
		async for port in tqdm(range(1, max_ports + 1), desc='Creating tasks', ascii=False, 
								unit='task', smoothing=0.5, colour='blue', 
								bar_format='{desc}: {percentage:3.0f}%| {bar} | {n_fmt}/{total_fmt} {rate_fmt}{postfix}'):
			tasks.append(asyncio.create_task(scan_port(url, port)))

	async for task in tqdm(tasks, desc='Launch task', ascii=False, 
							unit='task', smoothing=0.5, colour='blue', 
							bar_format='{desc}: {percentage:3.0f}%| {bar} | {n_fmt}/{total_fmt} {rate_fmt}{postfix}'):
		data = await asyncio.gather(task)
		if data[0].split(' ')[-1] == 'opened':
			available_ports.append(data[0])
		text += f'{data[0]}\n'

	if len(available_ports) > 0:
		print(f'[bold green]{" ".join(available_ports)}[/bold green]')
	print(f'List of opened ports: {" ".join(available_ports)}' if len(available_ports) > 0 else "No ports open")

	text += '\nReport generated by [zennet ⚡️](https://github.com/alexeev-engineer/zennet)'
	
	logger.log(f'Open ports of {url}: {available_ports}', 'info')

	write_to_file(output, text)


async def osint_ip(ip: str, output: str) -> None:
	logger.log(f'OSINT IP {ip}', 'info')
	task1 = asyncio.create_task(whois_info(ip))
	task2 = asyncio.create_task(ipwhois_info(ip))
	info1 = await asyncio.gather(task1)
	info2 = await asyncio.gather(task2)

	text = f'# IP address analysis report {ip}'

	data_tree = Tree(f"[green]{ip}")
	for i in range(len(info1[0])):
		name = info1[0][i].split(': ')[0]
		data = info1[0][i].split(': ')[-1]
		data_tree.add(f'[cyan]{name}[/cyan]: {data}')
		text += f'{info1[0][i]}\n'
	data_tree.add('[bold]IPWhois info:')
	for name, data in info2[0].items():
		data_tree.add(f'[cyan]{name}[/cyan]: {data}')
		text += f'{name}: {data}\n'

	data_tree.add(f'[italic]Log saved in {output}')

	text += '\nReport generated by [zennet ⚡️](https://github.com/alexeev-engineer/zennet)'

	write_to_file(output, text)
	print(data_tree)

@cache
async def main() -> None:
	"""Main function."""
	program_started = monotonic()

	print(f'⚡️ zennet v {__version__} @ alexeev-engineer\n')

	parser = argparse.ArgumentParser(description='Blazing fast tool for analysis network traffic')
	parser.add_argument("--url", type=str, help='URL address')
	parser.add_argument('-o', '--output', type=str, default='zennet.md', help='Filename for output')

	parser.add_argument('--get', action='store_true', help='Send HTTP-get request')

	parser.add_argument('--scan-ports', action='store_true', help='Port scannner')
	parser.add_argument('--ports', type=str, help='List of ports for scanning (overwrite max ports)')
	parser.add_argument('--max-ports', type=int, default=2**16, help='Max ports count for scanning')
	parser.add_argument('--whois', action='store_true', help='WhoIs IP (needed --url (but IP))')

	args = parser.parse_args()

	if args.get:
		if args.url:
			start = monotonic()
			task = asyncio.create_task(send_get(args.url, 3, args.output))
			await task
			end = monotonic()
			total = end - start
			print(f'Request execution time: {round(total, 4)} seconds')
		else:
			print('URL not set')
	elif args.whois:
		if args.url:
			start = monotonic()
			task = asyncio.create_task(osint_ip(args.url, args.output))
			await task
			end = monotonic()
			total = end - start
			print(f'Whois execution time: {round(total, 4)} seconds')
		else:
			print('URL not set')
	elif args.scan_ports:
		if args.url:
			start = monotonic()
			task = asyncio.create_task(start_port_scanner(args.url, args.ports, args.max_ports, args.output))
			await task
			end = monotonic()
			total = end - start
			print(f'Port scanner operating time: {round(total, 4)} seconds')
		else:
			print('URL not set')
	else:
		print('[red]View help with `--help` flag[/red]')

	program_ended = monotonic()
	
	program_work_time = round(program_ended - program_started, 4)
	print(f'\n⚡️ Software execution time: {program_work_time} seconds')


if __name__ == '__main__':
	asyncio.run(main())
