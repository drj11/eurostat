pretty.svg: apro_acs_a.tsv chart.py
	python3 chart.py

apro_acs_a.tsv:
	bin/fetch

