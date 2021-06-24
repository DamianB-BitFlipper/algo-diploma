.PHONY: all compile deploy opt-in clean

PYTHON=python3
DIPLOM_SMART_CONTRACT=diplom_smart_contract
DIPLOM_PROGRAM=run_diplom

all: compile

compile:
	$(PYTHON) ./assets/$(DIPLOM_SMART_CONTRACT).py > ./assets/$(DIPLOM_SMART_CONTRACT).teal

deploy:
	$(PYTHON) ./$(DIPLOM_PROGRAM).py deploy

update:
	$(PYTHON) ./$(DIPLOM_PROGRAM).py update

opt-in:
	$(PYTHON) ./$(DIPLOM_PROGRAM).py opt-in

issue-diploma:
	$(PYTHON) ./$(DIPLOM_PROGRAM).py issue-diploma

inspect:
	$(PYTHON) ./$(DIPLOM_PROGRAM).py inspect

clean:
	rm ./assets/$(DIPLOM_SMART_CONTRACT).teal
