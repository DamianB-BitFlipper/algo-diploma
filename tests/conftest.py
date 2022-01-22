from algopytest import initialize

# Load the smart contracts from this project. The path to find these
# imports is set by the environment variable `$PYTHONPATH`.
from diploma_smart_contract import diploma_program
from clear_program import clear_program

def pytest_configure(config):
    """Initialize algopytest before the pytest tests run."""
    initialize(approval_program=diploma_program, 
               clear_program=clear_program,
               local_bytes=1, global_bytes=1)
