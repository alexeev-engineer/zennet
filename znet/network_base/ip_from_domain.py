from ipaddress import IPv4Address
from socket import gethostbyname, gaierror


def ip_from_domain(domain: str) -> (str, None):
	try:
		IPv4Address(domain)
		return domain
	except Exception:
		if domain.startswith("http"):
			domain = domain.split("/")[2]
			if len(domain.split(".")) > 2:
				domain = ".".join(domain.split(".")[1:])

	try:
		ip_domain = gethostbyname(domain)
		return ip_domain
	except gaierror:
		return
