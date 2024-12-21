alias t := test
alias c := cover
alias h := cover-html

# run tests
test:
	poetry run pytest tests/

# run test with coverage
cover:
	poetry run pytest --cov=picsort tests/

# run test with coverage in html
cover-html:
	poetry run pytest --cov=picsort --cov-report html tests/
