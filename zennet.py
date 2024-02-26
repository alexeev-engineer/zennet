#! venv/bin/python3
import argparse
from functools import cache
from time import perf_counter
from rich import print
from rich.tree import Tree
from icecream import ic
import asyncio

from znet.request.get import send_request_get
from znet.scanners.port_scanner import scan_port


@cache
def write_to_file(filename: str, data: str):
	ic(filename)
	with open(filename, 'w') as file:
		file.write(data)


@cache
async def send_get(url: str, timeout: int, output):
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
async def main():
	program_started = perf_counter()

	print('zennet v 0.2.3 @ alexeev-engineer\n')

	parser = argparse.ArgumentParser(description='Невероятно быстрый инструмент для анализа сетевого трафика')
	parser.add_argument("--url", type=str, help='URL адрес')
	parser.add_argument('-o', '--output', type=str, default='zennet.md', help='Название файла для сохранения вывода')

	parser.add_argument('--get', action='store_true', help='Отправить HTTP GET запрос')

	parser.add_argument('--scan-ports', action='store_true', help='Сканировать порты')
	parser.add_argument('--ports', help='Список портов для сканирования')
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
			exit()
	elif args.scan_ports:
		if args.url:
			tasks = []
			text = ''
			ports = []

			start = perf_counter()
			if args.ports:
				for port in args.ports.split(' '):
					tasks.append(asyncio.create_task(scan_port(args.url, int(port))))
			else:
				for port in range(1, args.max_ports + 1):
					tasks.append(asyncio.create_task(scan_port(args.url, port)))

			for task in tasks:
				data = await asyncio.gather(task)
				if data[0].split(' ')[-1] == 'открыт':
					print(f'[bold green]{data[0]}[/bold green]')
					ports.append(data[0])
				else:
					print(f'[dim]{data[0]}[/dim]')
				text += f'{data[0]}\n'

			print(f'Список открытых портов: {" ".join(ports)}')

			write_to_file(args.output, text)
			end = perf_counter()
			total = end - start
			print(f'Время работы сканера портов: {round(total, 4)} сек.')
	else:
		print('[red]Вы не ввели ни одного аргумента. Используйте `--help` или `-h` для просмотра справки[/red]')

	program_ended = perf_counter()
	
	program_work_time = round(program_ended - program_started, 4)
	print(f'\nВремя исполнения программы: {program_work_time} сек')


if __name__ == '__main__':
	asyncio.run(main())
