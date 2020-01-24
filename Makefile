FIXTURES = currencies

all: install migrate loaddata client

install:
	@pip install -Ur requirements/base.txt

migrate:
	@python ./manage.py migrate

loaddata:
	@python ./manage.py loaddata $(FIXTURES)

client:
	@cd pizzer-client && npm install && npm run release && cd -
