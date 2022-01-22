from algopytest import application_global_state

def test_initialization(owner, smart_contract_id):
    # Read the registrar's address from the application's global state
    ret = application_global_state(
        smart_contract_id,
        addresses=[b'registrar'],
    )
    
    # Assert that the registrar was set properly
    assert ret[b'registrar'] == owner.address
