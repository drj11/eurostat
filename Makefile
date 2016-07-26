pretty.svg: apro_acs_a.tsv.gz
	python chart.py

apro_acs_a.tsv.gz:
	bin/fetch

