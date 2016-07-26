pretty.svg: apro_acs_a.tsv chart.py
	python chart.py

apro_acs_a.tsv:
	bin/fetch

