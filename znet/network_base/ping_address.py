from ipaddress import IPv4Address
from ping3 import ping


def ping_addr(addr: str) -> bool:
	try:
		IPv4Address(addr)
	except Exception:
		if addr.startswith("http"):
			addr = addr.split("/")[2]
			if len(addr.split(".")) > 2:
				addr = ".".join(addr.split(".")[1:])

	try:
		if ping(addr) is not None:
			return True
		return False
	except Exception:
		return False
