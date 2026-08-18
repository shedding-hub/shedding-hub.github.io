.PHONY = ^datasets-yaml hero-trace clean

DATA_REF ?= main
DATASETS_YAML = $(wildcard _datasets/*.yaml)
DATASETS_MD = ${DATASETS_YAML:.yaml=.md}

# Convert the yaml files to markdown files which we can use in the collection.
_datasets : ${DATASETS_MD}

# printf rather than echo: only some shells expand \n in echo, and the ones that
# do not write a literal "---\n" that Jekyll reads as malformed front matter. It
# then drops every dataset from the collection silently, building a site with an
# empty catalog and no error.
${DATASETS_MD} : _datasets/%.md : _datasets/%.yaml
	printf '%s\n' '---' "`cat $<`" '---' | sed 's/^url:/source_url:/g' > $@

# Phony target to download the yaml files. The same archive also carries the
# per-analyte figures, which are built in the data repository by `make figures`
# -- this site has no Python to regenerate them with -- so they are copied out
# here rather than committed a second time. index.json becomes a Jekyll data
# file so the dataset layout can look up an analyte's figures in Liquid.
^_datasets-yaml : tmp/shedding-hub.zip
	rm -rf tmp/shedding-hub-${DATA_REF}
	unzip -d tmp $<
	mkdir -p _datasets
	cp -r tmp/shedding-hub-${DATA_REF}/data/*/*.yaml _datasets
	mkdir -p assets/figures _data
	# Tolerated rather than required: a DATA_REF predating the figures, or a
	# branch that never carried them, should still build a site -- the layout
	# omits the figure block when the data file is absent. Failing the whole
	# build over a missing illustration would take the datasets down with it.
	if [ -d tmp/shedding-hub-${DATA_REF}/figures ]; then \
	  cp -r tmp/shedding-hub-${DATA_REF}/figures/* assets/figures/ ; \
	  mv assets/figures/index.json _data/figures.json ; \
	else \
	  echo "no figures/ in ${DATA_REF}; dataset pages will omit them" ; \
	fi
	# The fitted-parameter catalog the Python package ships. It is the only
	# source of fit parameters, and it lags the figure index because it is
	# rebuilt at release rather than per dataset. Tolerated when absent, like
	# the figures above: the fits page then reports coverage as unavailable
	# rather than failing the build.
	if [ -f tmp/shedding-hub-${DATA_REF}/shedding_hub/data/shedding_catalog.yaml ]; then \
	  cp tmp/shedding-hub-${DATA_REF}/shedding_hub/data/shedding_catalog.yaml _data/shedding_catalog.yaml ; \
	else \
	  echo "no shedding_catalog.yaml in ${DATA_REF}; the fits table will be empty" ; \
	fi

tmp/shedding-hub.zip :
	mkdir -p tmp
	curl -L -o $@ https://github.com/shedding-hub/shedding-hub/archive/refs/heads/${DATA_REF}.zip

# Deliberately not part of the site build: CI has no Python, and the homepage hero
# plots a fixed reference study whose measurements do not change. The generated
# _data/hero_trace.yaml is committed. Run this only to feature a different study
# or change the plot geometry, after `make ^_datasets-yaml`.
hero-trace :
	python tools/make_hero_trace.py

clean :
	rm -rf _datasets tmp assets/figures _data/figures.json _data/shedding_catalog.yaml
