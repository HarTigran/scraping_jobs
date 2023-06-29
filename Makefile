install:
	pip install --upgrade pip && \
		pip install -r requirements.txt

format:	
	black app/**/*.py

lint:
	pylint --disable=R, app/*.py

all: install lint format build