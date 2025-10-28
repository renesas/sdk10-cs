all: build/DA1459x_SDK_10.1.4.104.patch
all: build/SDK_10.1.6.108.patch
all: build/da1459x-sdk10.1.2.86.patch

%.patch: %.zip
	sha1sum --quiet --check $<.sha1
	patchtree --out $@ $<

%.sha1: %
	sha1sum $< > $@
