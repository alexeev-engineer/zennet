python = python3
pip = pip3
req = requirements.txt
CC = gcc
CCFLAGS = -fPIC -shared
lint = ruff

install:
	$(python) -m venv venv
	$(pip) install -r $(req)

check:
	$(lint) check . --fix

binary:
	pyinstaller zennet.py --onefile --onedir --clean -n zennet
	
clean:
	rm -r znet/__pycache__
	rm -r znet/request/__pycache__
	rm -r znet/scanners/__pycache__
	$(lint) clean
