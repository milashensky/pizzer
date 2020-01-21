FIXTURES = currencies

all: install migrate loaddata

install:
	@pip install -Ur requirements/base.txt

migrate:
	@python ./manage.py migrate

loaddata:
	@python ./manage.py loaddata $(FIXTURES)
