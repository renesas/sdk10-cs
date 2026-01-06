.PHONY: FORCE

BUILD_DIR = build
SDK_DIR = sdk

test: $(SDK_DIR) patch FORCE
	bin/sdk10-cs-test --sdk-dir $(SDK_DIR) --build-dir $(BUILD_DIR) cases.yaml

$(SDK_DIR):
	bin/prepare ../build $(SDK_DIR)

patch: FORCE
	bin/patch $(SDK_DIR)

clean: FORCE
	$(RM) -r $(BUILD_DIR) $(SDK_DIR)
