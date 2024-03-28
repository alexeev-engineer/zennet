from socket import socket, AF_INET, SOCK_DGRAM


def local_ipv4() -> str:
	ip = None
	st = socket(AF_INET, SOCK_DGRAM)
	try:
		st.connect(('10.255.255.255', 1))
		ip = st.getsockname()[0]
	except Exception:
		ip = '127.0.0.1'
	finally:
		st.close()
		return ip
