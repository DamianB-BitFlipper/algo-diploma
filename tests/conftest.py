from pytest import fixture
from algopytest import compile_program, deploy_smart_contract
from algosdk.future import transaction
from pyteal import Mode

# Load the smart contracts from this project. The path to find these
# imports is set by the environment variable `$PYTHONPATH`.
from diploma_smart_contract import diploma_program
from clear_program import clear_program

@fixture
def smart_contract_components():
    diploma_program_compiled = compile_program(diploma_program, mode=Mode.Application, version=5)
    clear_program_compiled = compile_program(clear_program, mode=Mode.Application, version=5)
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
    with deploy_smart_contract(
            owner,
            approval_program=diploma_program, 
            clear_program=clear_program,
            local_bytes=1,
            global_bytes=1,        
    ) as app_id:
        yield app_id
