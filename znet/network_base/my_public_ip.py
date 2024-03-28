from requests import get


def public_ip() -> str:
	try:
		return get('https://api.ipify.org/').text
	except Exception:
		return '127.0.0.1'
