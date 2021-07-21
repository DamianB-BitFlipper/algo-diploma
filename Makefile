.PHONY: all compile clean

PYTHON=python3
DIPLOMA_SMART_CONTRACT=diploma_smart_contract

all: compile

compile:
	$(PYTHON) ./assets/$(DIPLOMA_SMART_CONTRACT).py > ./assets/$(DIPLOMA_SMART_CONTRACT).teal

clean:
	rm ./assets/$(DIPLOMA_SMART_CONTRACT).teal
