DATA_REF ?= main

_data/datasets : tmp/shedding-hub.zip
	rm -rf tmp/shedding-hub-${DATA_REF}
	unzip -d tmp $<
	mkdir -p $@
	cp -r tmp/shedding-hub-${DATA_REF}/data/*/*.yaml $@

tmp/shedding-hub.zip :
	mkdir -p tmp
	curl -L -o $@ https://github.com/shedding-hub/shedding-hub/archive/refs/heads/${DATA_REF}.zip

clean :
	rm -rf _data/datasets tmp
