all: build/DA1459x_SDK_10.1.4.104.patch
all: build/SDK_10.1.6.108.patch
all: build/da1459x-sdk10.1.2.86.patch
all: build/SDK_10.0.10.119.1.patch
all: build/SDK_10.0.12.146.1.patch
all: build/SDK_10.0.12.146.2.patch
all: build/SDK_10.0.12.146.3.patch
all: build/SDK_10.0.12.146.patch
all: build/SDK_10.0.16.153.patch
# all: build/SDK_10.0.8.105.patch

%.patch: %.zip
	sha1sum --quiet --check $<.sha1
	patchtree --out $@ $<

%.sha1: %
	sha1sum $< > $@
