import pytest

from algopytest import (
    application_local_state,
    call_app, 
    opt_in_app,
    close_out_app,
)

def opt_in_user(user, smart_contract_id):
    """Opt-in the ``user`` to the ``smart_contract_id`` application."""
    opt_in_app(user, smart_contract_id)

    # The test runs here    
    yield user
    
    # Clean up by closing out of the application    
    close_out_app(user, smart_contract_id)

@pytest.fixture()
def owner_in(owner, smart_contract_id):
    """Create an ``owner`` fixture that has already opted in to ``smart_contract_id``."""
    yield from opt_in_user(owner, smart_contract_id)

@pytest.fixture()
def user1_in(user1, smart_contract_id):
    """Create an ``user1`` fixture that has already opted in to ``smart_contract_id``."""
    yield from opt_in_user(user1, smart_contract_id)

@pytest.fixture()
def user2_in(user2, smart_contract_id):
    """Create an ``user2`` fixture that has already opted in to ``smart_contract_id``."""
    yield from opt_in_user(user2, smart_contract_id)

@pytest.fixture()
def user3_in(user3, smart_contract_id):
    """Create an ``user3`` fixture that has already opted in to ``smart_contract_id``."""
    yield from opt_in_user(user3, smart_contract_id)

@pytest.fixture()
def user4_in(user4, smart_contract_id):
    """Create an ``user4`` fixture that has already opted in to ``smart_contract_id``."""
    yield from opt_in_user(user4, smart_contract_id)    
    
@pytest.mark.parametrize(
    "users",
    [
        # Issue a single diploma
        ["user1_in"],
        # Issue multiple diplomas
        ["user1_in", "user2_in", "user3_in", "user4_in"],
    ]
)
def test_issue_diplomas(request, owner_in, users, smart_contract_id):
    for user in users:
        user_in = request.getfixturevalue(user)
        diploma_metadata = "Damian Barabonkov :: MIT :: BSc Computer Science and Engineering :: 2020"

        # The application arguments and account to be passed in to 
        # the smart contract as it expects
        app_args = ['issue_diploma', diploma_metadata, 4]

        # Issue the `diploma_metadata` to the recipient `user`
        call_app(owner_in, smart_contract_id, app_args=app_args, accounts=[user_in])

        # Check that the diploma was issued
        state = application_local_state(smart_contract_id, user_in)
        assert state['diploma'] == diploma_metadata
        assert state['degree_duration'] == 4

def test_issue_many_diplomas(request, owner_in, create_user, smart_contract_id):
    diploma_metadata = "Damian Barabonkov :: MIT :: BSc Computer Science and Engineering :: 2020"
    
    num_users = 8
    users = []
    for i in range(num_users):
        user = create_user()
        users.append(user)
        opt_in_app(user, smart_contract_id)

        # Do some funky business to capture the `user` of this
        # local scope for every iteration of the loop
        def opt_out_fn(user):
            def _wrapper():
                close_out_app(user, smart_contract_id)
            return _wrapper

        # Opt out each `user` upon completion of this test, pass or fail
        request.addfinalizer(opt_out_fn(user))

        # The application arguments and account to be passed in to 
        # the smart contract as it expects
        app_args = ['issue_diploma', diploma_metadata, 4]

        # Issue the `diploma_metadata` to the recipient `user`
        call_app(owner_in, smart_contract_id, app_args=app_args, accounts=[user])

    for user in users:
        # Check that the diploma was issued to `user`
        state = application_local_state(smart_contract_id, user)
        assert state['diploma'] == diploma_metadata
        assert state['degree_duration'] == 4
