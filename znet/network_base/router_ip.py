from ipaddress import IPv4Address
from socket import gethostbyname
from platform import system
from subprocess import check_output


def get_host(ip: str) -> str:
	try:
		sock = gethostbyname(ip)
		return sock
	except Exception:
		return ip


def check_ip(ip: str) -> str:
	try:
		IPv4Address(ip)
		return ip
	except Exception:
		return get_host(ip)


def router_ip() -> (str, None):
	if system() == "Linux":
		try:
			ip_route = str(check_output('route -n | grep UG', shell=True).decode().split()[1])
			return check_ip(ip_route)
		except Exception:
			return
	elif system() == "Windows":
		try:
			ip_route = check_output('route PRINT 0* -4 | findstr 0.0.0.0', shell=True).decode('cp866'). \
				split()[-3]
			return check_ip(ip_route)
		except Exception:
			return
