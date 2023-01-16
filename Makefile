SRC := $(CURDIR)/src
BUILD := $(SRC)/dist
TARBUILD := $(BUILD)/mctl-0.1.0.tar.gz
# TODO: build target file name dynamic

SOURCEFILES := $(shell find $(SRC) -type f -name *.py)

.PHONY: install dependencies uninstall clean

install: $(TARBUILD)
	pipx install $(TARBUILD)

dependencies:
	pip install --user --upgrade pip
	pip install --user --upgrade build pipx

$(TARBUILD): $(SOURCEFILES)
	python3 -m build $(SRC)

uninstall: dependencies
	pipx uninstall mctl

clean:
	rm -r $(BUILD)

docker-image:
	docker build -t mctl:0.1.0 -t mctl:latest .
