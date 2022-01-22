.PHONY: all compile clean

PYTHON=python3
DIPLOMA_SMART_CONTRACT=diploma_smart_contract
CLEAR_PROGRAM=clear_program

all: compile

compile:
	$(PYTHON) ./assets/$(DIPLOMA_SMART_CONTRACT).py > ./artifacts/$(DIPLOMA_SMART_CONTRACT).teal
	$(PYTHON) ./assets/$(CLEAR_PROGRAM).py > ./artifacts/$(CLEAR_PROGRAM).teal

clean:
	rm ./artifacts/$(DIPLOMA_SMART_CONTRACT).teal
	rm ./artifacts/$(CLEAR_PROGRAM).teal
