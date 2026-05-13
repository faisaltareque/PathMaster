.PHONY: test test-cov test-verbose lint clean install

test:
	python3 -m pytest tests/ -v

test-cov:
	python3 -m pytest tests/ -v --cov=pathmaster --cov-report=html

test-verbose:
	python3 -m pytest tests/ -vv -s

lint:
	python3 -m flake8 pathmaster/ tests/ --max-line-length=120

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ *.egg-info .eggs

install-test:
	pip3 install -r requirements-test.txt

install:
	pip3 install -e .
	make install-test
