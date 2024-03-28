from platform import system
from subprocess import check_output

from getmac.getmac import get_mac_address
from netifaces import ifaddresses, AF_INET


def local_ipv4() -> str:
	if system() == "Linux":
		try:
			return ifaddresses(_get_default_iface_linux()).setdefault(AF_INET)[0]['addr']
		except Exception:
			return '127.0.0.1'
	elif system() == "Windows":
		try:
			mac_address = get_mac_address().replace(":", "-").upper()
			interface_temp = check_output('getmac /FO csv /NH /V', shell=False).decode('cp866').split("\r\n")
			for face in interface_temp:
				if mac_address in face:
					return ifaddresses(face.split(",")[-1].replace('"', '').split("_")[-1]). \
						setdefault(AF_INET)[0]['addr']
		except Exception:
			return '127.0.0.1'
