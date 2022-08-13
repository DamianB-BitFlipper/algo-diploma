from algopytest import register_smart_contract

# Load the smart contracts from this project. The path to find these
# imports is set by the environment variable `$PYTHONPATH`.
from diploma_smart_contract import diploma_program
from clear_program import clear_program

def pytest_configure(config):
    """Initialize AlgoPytest before the Pytest tests run."""
    register_smart_contract(
        name="diploma_contract",
        approval_program=diploma_program, 
        clear_program=clear_program,
        local_bytes=1,
        global_bytes=1
    )
