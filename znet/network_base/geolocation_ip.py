from requests import get


def geo_ip(ip) -> (list, bool):
	try:
		req = get(url=f'http://ip-api.com/json/{ip}').json()
		return [req['lat'], req['lon']]
	except Exception:
		return
