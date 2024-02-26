python = python3
pip = pip3
req = requirements.txt
lint = ruff

install:
	$(python) -m venv venv
	$(pip) install -r $(req)

check:
	$(lint) check . --fix

build:
	nuitka3 zennet.py --onefile --output-dir=build --output-filename=zennet --lto=yes --show-progress --enable-console --company-name=alexeev-engineer --product-name=ZENNET

clean:
	rm -r znet/__pycache__
	rm -r znet/request/__pycache__
	rm -r znet/scanners/__pycache__
	$(lint) clean
