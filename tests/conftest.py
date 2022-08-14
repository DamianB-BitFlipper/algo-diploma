from pytest import fixture
from algopytest import register_smart_contract, compile_program
from pyteal import Mode

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


@fixture
def diploma_program_compiled():
    return compile_program(diploma_program, mode=Mode.Application, version=5)

@fixture
def clear_program_compiled():
    return compile_program(clear_program, mode=Mode.Application, version=5)
