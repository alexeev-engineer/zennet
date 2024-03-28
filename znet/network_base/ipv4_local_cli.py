from platform import system
from subprocess import check_output


def local_ipv4() -> (str, None):
	if system() == "Linux":
		try:
			return check_output('ip -h -br a | grep UP', shell=True).decode().split()[2].split("/")[0]
		except Exception:
			return

	elif system() == "Windows":
		try:
			net_set = check_output("wmic nicconfig get IPAddress, IPEnabled /value"). decode("cp866").strip().\
				split("\r\r\n")

			text = ""
			for net in net_set:
				if net.strip() == "":
					text = f"{text}|"
				else:
					text = f"{text}~{net.strip()}"
			text = text.strip().split("||")
			for tx in text:
				if tx.split("~")[-1].split("=")[1] != "TRUE":
					continue
				for item in tx.split("~"):
					if item.strip() == "":
						continue
					if item.strip().split("=")[0] == "IPEnabled":
						continue
					if item.strip().split("=")[1] != "":
						if item.strip().split("=")[0] == "IPAddress":
							return item.strip().split("=")[1].split(",")[0].replace('"', '').replace("{", "")
		except Exception:
			return
