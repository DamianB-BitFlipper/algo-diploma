import pytest
import algosdk

from algopytest import (
    application_global_state,
    account_balance,
    create_compiled_app,
    update_app,
    delete_app,
    opt_in_app,
    close_out_app,
    clear_app,
)

def test_owner_funded(owner):
    """Test whether the ``owner`` fixture was funded correctly."""
    balance = account_balance(owner)
    assert balance == 1_000_000_000

def test_initialization(owner, smart_contract_id):
    """Test that the initialization logic of the smart contract works correctly."""
    # Read the registrar's address from the application's global state
    state = application_global_state(
        smart_contract_id,
        address_fields=['registrar'],
    )
    
    # Assert that the `registrar` was set properly
    assert state['registrar'] == owner.address

def test_delete_application_from_owner(owner, smart_contract_components):
    """Test that the application is deleteable by its ``owner``."""
    # Unpack the `smart_contract_components`
    approval_program, clear_program, global_schema, local_schema = smart_contract_components
    
    app_id = create_compiled_app(owner, approval_program, clear_program, global_schema, local_schema)
    delete_app(owner, app_id)

def test_delete_application_from_nonowner(user1, smart_contract_id):
    """Test that no non-owner may delete the application."""
    # Expect an exception
    with pytest.raises(algosdk.error.AlgodHTTPError, match=r'transaction .*: transaction rejected by ApprovalProgram'):
        delete_app(user1, smart_contract_id)

def test_update_from_owner(owner, smart_contract_id, smart_contract_components):
    """Test that the owner may update the application."""
    # Unpack the `smart_contract_components`
    approval_program, clear_program, _, _ = smart_contract_components
    
    # Should not raise an exception
    update_app(owner, smart_contract_id, approval_program, clear_program)

def test_update_from_nonowner(user1, smart_contract_id, smart_contract_components):
    """Test that no non-owner may update the application."""
    # Unpack the `smart_contract_components`
    approval_program, clear_program, _, _ = smart_contract_components
    
    # Expect an exception
    with pytest.raises(algosdk.error.AlgodHTTPError, match=r'transaction .*: transaction rejected by ApprovalProgram'):
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
    """Test various combinations of users opting in and out of the application."""
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
    """Test that opting in twice consecutively fails."""
    opt_in_app(owner, smart_contract_id)

    # Expect an exception on the second opt in
    with pytest.raises(algosdk.error.AlgodHTTPError, match=r'transaction .*: account .* has already opted in to app \d+'):
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
    """Test that opting out twice consecutively fails."""
    opt_in_app(owner, smart_contract_id)
    opt_out_fn(owner, smart_contract_id)

    # Expect an exception on the second close out
    with pytest.raises(algosdk.error.AlgodHTTPError, match=r'transaction .*: .*is not.*opted in.*app.*\d+'):
        opt_out_fn(owner, smart_contract_id)
    
