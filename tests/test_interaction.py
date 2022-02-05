import pytest

from algopytest import (
    call_app, 
    opt_in_app,
    close_out_app,
)

@pytest.fixture
def owner_in(owner, smart_contract_id):
    """Create an ``owner`` fixture that has already opted in to ``smart_contract_id``."""
    opt_in_app(owner, smart_contract_id)
    
    # The test runs here
    yield owner

    # Clean up by closing out of the application
    close_out_app(owner, smart_contract_id)

@pytest.fixture
def user1_in(user1, smart_contract_id):
    """Create a ``user1`` fixture that has already opted in to ``smart_contract_id``."""
    opt_in_app(user1, smart_contract_id)

    # The test runs here
    yield user1

    # Clean up by closing out of the application
    close_out_app(user1, smart_contract_id)

def test_issue_diploma(owner_in, user1_in, smart_contract_id):
    diploma_metadata = "Damian Barabonkov :: MIT :: BSc Computer Science and Engineering :: 2020"

    # The application arguments and account to be passed in to 
    # the smart contract as it expects
    app_args = ['issue_diploma', diploma_metadata]
    accounts = [user1_in.address]

    # Issue the `diploma_metadata` to the recipient `user1`
    call_app(owner_in, smart_contract_id, app_args=app_args, accounts=accounts)
