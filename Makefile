.PHONY = ^datasets-yaml

DATA_REF ?= main
DATASETS_YAML = $(wildcard _datasets/*.yaml)
DATASETS_MD = ${DATASETS_YAML:.yaml=.md}

# Convert the yaml files to markdown files which we can use in the collection.
_datasets : ${DATASETS_MD}

${DATASETS_MD} : _datasets/%.md : _datasets/%.yaml
	echo "---\n`cat $<`\n---" | sed 's/^url:/source_url:/g' > $@

# Phony target to download the yaml files.
^_datasets-yaml : tmp/shedding-hub.zip
	rm -rf tmp/shedding-hub-${DATA_REF}
	unzip -d tmp $<
	mkdir -p _datasets
	cp -r tmp/shedding-hub-${DATA_REF}/data/*/*.yaml _datasets

tmp/shedding-hub.zip :
	mkdir -p tmp
	curl -L -o $@ https://github.com/shedding-hub/shedding-hub/archive/refs/heads/${DATA_REF}.zip

clean :
	rm -rf _datasets tmp
