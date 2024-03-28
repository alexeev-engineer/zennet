from ipaddress import IPv4Address
from _socket import gethostbyaddr


def domain_ip(ip) -> (str, None):
	try:
		IPv4Address(ip)
	except Exception:
		return
	try:
		return gethostbyaddr(ip)[0]
	except Exception:
		return
