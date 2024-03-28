from socket import getservbyport


def serv_on_port(port: int) -> str:
	try:
		return getservbyport(port)
	except Exception:
		return "Unknown"


def type_port(port) -> str:
	if type(port) == int:
		return serv_on_port(port)
	elif type(port) == str:
		if port.isdigit():
			return serv_on_port(int(port))
