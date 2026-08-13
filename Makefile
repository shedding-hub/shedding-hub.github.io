.PHONY = ^datasets-yaml

DATA_REF ?= main
DATASETS_YAML = $(wildcard _datasets/*.yaml)
DATASETS_MD = ${DATASETS_YAML:.yaml=.md}

# Convert the yaml files to markdown files which we can use in the collection.
_datasets : ${DATASETS_MD}

${DATASETS_MD} : _datasets/%.md : _datasets/%.yaml
	echo "---\n`cat $<`\n---" | sed 's/^url:/source_url:/g' > $@

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

tmp/shedding-hub.zip :
	mkdir -p tmp
	curl -L -o $@ https://github.com/shedding-hub/shedding-hub/archive/refs/heads/${DATA_REF}.zip

clean :
	rm -rf _datasets tmp assets/figures _data/figures.json
