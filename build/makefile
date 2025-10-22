all: DA1459x_SDK_10.1.4.104.patch
all: SDK_10.1.6.108.patch
all: da1459x-sdk10.1.2.86.patch

MKPATCH := ../scripts/mkpatch.py

%.patch: %.zip
	sha1sum -c $<.sha1
	$(MKPATCH) $< > $@

%.sha1: %
	sha1sum $< > $@
