_data/datasets : tmp/shedding-hub.zip
	rm -rf tmp/shedding-hub-main
	unzip -d tmp $<
	mkdir -p _data/datasets
	cp tmp/shedding-hub-main/data/*.yaml $@

tmp/shedding-hub.zip :
	mkdir -p tmp
	curl -L -o $@ https://github.com/shedding-hub/shedding-hub/archive/refs/heads/main.zip

clean :
	rm -rf _data/datasets tmp
