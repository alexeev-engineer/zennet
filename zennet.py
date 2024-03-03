#! venv/bin/python3
"""⚡️ Молниеносно быстрая и многофункциональная консольная программа для анализа сетевого трафика
Blazing fast tool for network traffic analysis and working with network protocols
Copyright (C) 2024  Alexeev Bronislav
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import argparse
from functools import cache
from time import perf_counter
from rich import print
from rich.tree import Tree
from icecream import ic
from tqdm.asyncio import tqdm
import asyncio

# Модули
from znet.request.get import send_request_get
from znet.scanners.port_scanner import scan_port


@cache
def write_to_file(filename: str, data: str) -> None:
	"""Запись данных в файл
	Аргументы:

	with
 + filename: str - название файла
 + data: str - данные
	"""
	ic(filename)

	with open(filename, 'w') as file:
		file.write(data)


@cache
async def send_get(url: str, timeout: int, output: str) -> None:
	"""Функция создания асинхронной задачи отправки http get запроса.

	Аргументы:
	 + url: str - URL адрес
	 + timeout: int - таймаут
	+ output: str - название файла для сохранения вывода
	"""
	ic(url)
	task = asyncio.create_task(send_request_get(url, timeout))
	data = await asyncio.gather(task)

	data_tree = Tree(f"[yellow]{data[0][0]}")
	data_tree.add(f"[cyan]Код ответа:{data[0][1]}")
	data_tree.add(f"[cyan]Заголовок ответа: {data[0][2]}")
	data_tree.add(f'[italic]Весь лог сохранен в {output}')

	data = f'''# Запрос: {data[0][0]})
Код ответа: `{data[0][1]}`\n
Заголовок ответа: `{data[0][2]}`\n
Контент ответа:

```html
{data[0][3]}```

Текст ответа: 

```html
{data[0][4]}
```'''
	
	write_to_file(output, data)
	print(data_tree)


@cache
async def start_port_scanner(url: str, ports: str, max_ports: int, output: str) -> None:
	"""Асинхронная задача запуска сканера портов.

	Аргументы:
 + url: str - URL адрес
 + ports: str - порты
 + max_ports: int - максимальное количество портов
 + output: str - название файла для сохранения лога
	"""
	print(f'Начинаем сканировать {url}')
	text = f'# Результат сканирования портов по URL {url}:\n'
	tasks = []
	available_ports = []

	# Если порты были указаны напрямую, а не просто максимальное число для сканироваия портов
	if ports:
		# Разделяем список портов
		async for port in tqdm(ports.split(' '), desc='Создание задач', ascii=False, 
								unit='задача', smoothing=0.5, colour='blue', 
								bar_format='{desc}: {percentage:3.0f}%| {bar} | {n_fmt}/{total_fmt} {rate_fmt}{postfix}'):
			# Добавляем в список задач цель сканировать порт
			tasks.append(asyncio.create_task(scan_port(url, int(port))))
	else:
		# Если указано максимальное число для сканирования портов
		async for port in tqdm(range(1, max_ports + 1), desc='Создание задач', ascii=False, 
								unit='задача', smoothing=0.5, colour='blue', 
								bar_format='{desc}: {percentage:3.0f}%| {bar} | {n_fmt}/{total_fmt} {rate_fmt}{postfix}'):
			tasks.append(asyncio.create_task(scan_port(url, port)))

	# Проходимся в итерации по каждой задаче и сообщаем, открыт ли он
	async for task in tqdm(tasks, desc='Запуск задач', ascii=False, 
							unit='задача', smoothing=0.5, colour='blue', 
							bar_format='{desc}: {percentage:3.0f}%| {bar} | {n_fmt}/{total_fmt} {rate_fmt}{postfix}'):
		data = await asyncio.gather(task)
		if data[0].split(' ')[-1] == 'открыт':
			available_ports.append(data[0])
		# else:
		# 	print(f'[dim]{data[0]}[/dim]')
		text += f'{data[0]}\n'

	# Сообщаем, какие порты открыты (или вовсе нету открытых)
	if len(available_ports) > 0:
		print(f'[bold green]{" ".join(available_ports)}[/bold green]')
	print(f'Список открытых портов: {" ".join(available_ports)}' if len(available_ports) > 0 else "Открытых портов нету")

	# Сохраняем вывод в файл
	write_to_file(output, text)


@cache
async def main() -> None:
	"""Главная функция zennet
	Здесь находится парсер аргументов и запускаются все нужные задачи.
	"""
	program_started = perf_counter()

	print('⚡️ zennet v 0.2.3 @ alexeev-engineer\n')

	parser = argparse.ArgumentParser(description='Невероятно быстрый инструмент для анализа сетевого трафика')
	parser.add_argument("--url", type=str, help='URL адрес')
	parser.add_argument('-o', '--output', type=str, default='zennet.md', help='Название файла для сохранения вывода')

	parser.add_argument('--get', action='store_true', help='Отправить HTTP GET запрос')

	parser.add_argument('--scan-ports', action='store_true', help='Сканировать порты')
	parser.add_argument('--ports', type=str, help='Список портов для сканирования (приоритет выше --max-ports)')
	parser.add_argument('--max-ports', type=int, default=2**16, help='Максимальное количество портов для сканирования')

	args = parser.parse_args()

	if args.get:
		if args.url:
			start = perf_counter()
			task = asyncio.create_task(send_get(args.url, 3, args.output))
			end = perf_counter()
			total = end - start
			await task
			print(f'Запрос выполнен за {round(total, 4)} сек.')
		else:
			print('Вы не задали URL')
	elif args.scan_ports:
		if args.url:
			start = perf_counter()
			task = asyncio.create_task(start_port_scanner(args.url, args.ports, args.max_ports, args.output))
			await task
			end = perf_counter()
			total = end - start
			print(f'Время работы сканера портов: {round(total, 4)} сек.')
		else:
			print('Вы не задали URL')
	else:
		print('[red]Вы не ввели ни одного аргумента. Используйте `--help` или `-h` для просмотра справки[/red]')

	program_ended = perf_counter()
	
	program_work_time = round(program_ended - program_started, 4)
	print(f'\n⚡️ Время исполнения программы: {program_work_time} сек')


if __name__ == '__main__':
	asyncio.run(main())
