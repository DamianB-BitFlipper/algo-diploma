import pytest
import algosdk

from algopytest import (
    application_global_state,
    create_app,
    update_app,
    delete_app,
    opt_in_app,
    close_out_app,
    clear_app,
)

def test_initialization(owner, smart_contract_id):
    # Read the registrar's address from the application's global state
    ret = application_global_state(
        smart_contract_id,
        address_fields=['registrar'],
    )
    
    # Assert that the `registrar` was set properly
    assert ret['registrar'] == owner.address

def test_delete_application_from_owner(owner, smart_contract_components):
    # Unpack the `smart_contract_components`
    approval_program, clear_program, global_schema, local_schema = smart_contract_components
    
    app_id = create_app(owner, approval_program, clear_program, global_schema, local_schema)
    delete_app(owner, app_id)

def test_delete_application_from_nonowner(user1, smart_contract_id):
    # Expect an exception
    with pytest.raises(algosdk.error.AlgodHTTPError):
        delete_app(user1, smart_contract_id)

def test_update_from_owner(owner, smart_contract_id, smart_contract_components):
    # Unpack the `smart_contract_components`
    approval_program, clear_program, _, _ = smart_contract_components
    
    # Should not raise an exception
    update_app(owner, smart_contract_id, approval_program, clear_program)

def test_update_from_nonowner(user1, smart_contract_id, smart_contract_components):
    # Unpack the `smart_contract_components`
    approval_program, clear_program, _, _ = smart_contract_components
    
    # Expect an exception
    with pytest.raises(algosdk.error.AlgodHTTPError):
        update_app(user1, smart_contract_id, approval_program, clear_program)

@pytest.mark.parametrize(
    "users", 
    [
        ['owner'],
        ['owner', 'user1'],
        ['user1'], # Test a non-owner opt in
        ['user1', 'owner'], # Test when a non-owner opts in before the owner
        ['user1', 'owner', 'user2'],
    ],
)
@pytest.mark.parametrize(
    "opt_out_fn",
    [
        close_out_app,
        clear_app,
    ]
)
def test_opt_in_out(request, users, opt_out_fn, smart_contract_id):
    # Convert the string fixture names to the actual fixtures
    users = list(map(lambda user: request.getfixturevalue(user), users))

    # Opt in going forward through `users`
    for user in users:
        opt_in_app(user, smart_contract_id)

    # Close out going backwards through `users`
    for user in reversed(users):
        opt_out_fn(user, smart_contract_id)

@pytest.mark.parametrize(
    "opt_out_fn",
    [
        close_out_app,
        clear_app,
    ]
)
def test_opt_in_twice_out(owner, opt_out_fn, smart_contract_id):
    opt_in_app(owner, smart_contract_id)

    # Expect an exception on the second opt in
    with pytest.raises(algosdk.error.AlgodHTTPError):
        opt_in_app(owner, smart_contract_id)

    opt_out_fn(owner, smart_contract_id)

@pytest.mark.parametrize(
    "opt_out_fn",
    [
        close_out_app,
        clear_app,
    ]
)
def test_opt_in_out_twice(owner, opt_out_fn, smart_contract_id):
    opt_in_app(owner, smart_contract_id)
    opt_out_fn(owner, smart_contract_id)

    # Expect an exception on the second close out
    with pytest.raises(algosdk.error.AlgodHTTPError):
        opt_out_fn(owner, smart_contract_id)
    
