from pytest import fixture
from algopytest import (
    create_app,
    compile_program,
    opt_in_app,
    close_out_app,
)
from algosdk.future import transaction
from pyteal import Mode

# Load the smart contracts from this project. The path to find these
# imports is set by the environment variable `$PYTHONPATH`.
from diploma_smart_contract import diploma_program
from clear_program import clear_program

@fixture
def smart_contract_components():
    diploma_program_compiled = compile_program(diploma_program(), mode=Mode.Application, version=5)
    clear_program_compiled = compile_program(clear_program(), mode=Mode.Application, version=5)
    global_schema = transaction.StateSchema(num_uints=0, num_byte_slices=1)
    local_schema = transaction.StateSchema(num_uints=0, num_byte_slices=1)    
    
    return (
        diploma_program_compiled,
        clear_program_compiled,
        global_schema,
        local_schema,
    )

@fixture
def smart_contract_id(owner):
    with create_app(
            owner,
            approval_program=diploma_program(), 
            clear_program=clear_program(),
            local_bytes=1,
            local_ints=1,
            global_bytes=1,        
    ) as app_id:
        yield app_id

def opt_in_user(user, smart_contract_id):
    """Opt-in the ``user`` to the ``smart_contract_id`` application."""
    opt_in_app(user, smart_contract_id)

    # The test runs here    
    yield user
    
    # Clean up by closing out of the application    
    close_out_app(user, smart_contract_id)

@fixture
def owner_in(owner, smart_contract_id):
    """Create an ``owner`` fixture that has already opted in to ``smart_contract_id``."""
    yield from opt_in_user(owner, smart_contract_id)

@fixture
def user1_in(user1, smart_contract_id):
    """Create an ``user1`` fixture that has already opted in to ``smart_contract_id``."""
    yield from opt_in_user(user1, smart_contract_id)

@fixture
def user2_in(user2, smart_contract_id):
    """Create an ``user2`` fixture that has already opted in to ``smart_contract_id``."""
    yield from opt_in_user(user2, smart_contract_id)

@fixture
def user3_in(user3, smart_contract_id):
    """Create an ``user3`` fixture that has already opted in to ``smart_contract_id``."""
    yield from opt_in_user(user3, smart_contract_id)

@fixture
def user4_in(user4, smart_contract_id):
    """Create an ``user4`` fixture that has already opted in to ``smart_contract_id``."""
    yield from opt_in_user(user4, smart_contract_id)    
    
        
