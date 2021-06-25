.PHONY: all compile clean

PYTHON=python3
DIPLOM_SMART_CONTRACT=diplom_smart_contract

all: compile

compile:
	$(PYTHON) ./assets/$(DIPLOM_SMART_CONTRACT).py > ./assets/$(DIPLOM_SMART_CONTRACT).teal

clean:
	rm ./assets/$(DIPLOM_SMART_CONTRACT).teal
