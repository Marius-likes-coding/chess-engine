.PHONY: clean lint build test reqs instbot install
.DEFAULT_GOAL := lint test

clean :
	# cleaning build residents
	# find . -type d \( -name '*.egg' -name '*.egg-info' \) -exec rm -f {} +
	rm -rf *.egg-info

lint :
	black src

build :
	# building paprika
	python3 setup.py sdist bdist_wheel

test :
	python3 -m unittest discover -s src

reqs :
	# installing requirements ...
	pip3 install -r requirements.txt

instbot :
	# install chess-bot :
	pip install ./dist/chess-bot-*.tar.gz

install : build clean reqs instbot