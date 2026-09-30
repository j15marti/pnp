.PHONY: test check toy-product-span

test:
	pytest -q

check:
	python scripts/check_research_reports.py

toy-product-span:
	python experiments/product_span/run.py --toy-affine --source-bits 4 --outputs 8 --seed 1
