import sys
import yaml

from algosdk.future import transaction
from algosdk import account
from algosdk.v2client import algod

import common

CONFIG_FILE = "config.yml"

algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# Declare application state storage (immutable)
local_ints = 0
local_bytes = 1
global_ints = 0
global_bytes = 1
global_schema = transaction.StateSchema(global_ints, global_bytes)
local_schema = transaction.StateSchema(local_ints, local_bytes)

# Create new application
def create_app(client, private_key, 
               approval_program, clear_program, 
               global_schema, local_schema): 
    print("Creating new app")

    # Define sender as creator
    sender = account.address_from_private_key(private_key)

    # Declare on_complete as NoOp
    on_complete = transaction.OnComplete.NoOpOC.real

    # Get node suggested parameters
    params = client.suggested_params()
    params.flat_fee = True
    params.fee = 1000

    # Create unsigned transaction
    txn = transaction.ApplicationCreateTxn(
        sender, params, on_complete, \
        approval_program, clear_program, \
        global_schema, local_schema)

    # Sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # Send transaction
    client.send_transactions([signed_txn])

    # Await confirmation
    common.wait_for_confirmation(client, tx_id)

    # Display results
    transaction_response = client.pending_transaction_info(tx_id)
    app_id = transaction_response['application-index']
    print("Created new app-id: ", app_id)

    return app_id

# Opt-in to application
def opt_in_app(client, private_key, index): 
    # Declare sender
    sender = account.address_from_private_key(private_key)
    print("Opt-in from account: ", sender)

    # Get node suggested parameters
    params = client.suggested_params()
    params.flat_fee = True
    params.fee = 1000

    # Create unsigned transaction
    txn = transaction.ApplicationOptInTxn(sender, params, index)

    # Sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # Send transaction
    client.send_transactions([signed_txn])

    # Await confirmation
    common.wait_for_confirmation(client, tx_id)

    # Display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("Opt-in to app-id: ", transaction_response['txn']['txn']['apid'])    

# Call application
def call_app(client, private_key, index, app_args, accounts): 
    # Declare sender
    sender = account.address_from_private_key(private_key)
    print("Call from account: ", sender)

    # Get node suggested parameters
    params = client.suggested_params()
    params.flat_fee = True
    params.fee = 1000

    # Create unsigned transaction
    txn = transaction.ApplicationNoOpTxn(sender, params, index, app_args, accounts)

    # Sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # Send transaction
    client.send_transactions([signed_txn])

    # Await confirmation
    common.wait_for_confirmation(client, tx_id)

    # Display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("Called app-id: ", transaction_response['txn']['txn']['apid'])

    if "global-state-delta" in transaction_response :
        print("Global State updated :\n", transaction_response['global-state-delta'])
    if "local-state-delta" in transaction_response :
        print("Local State updated :\n", transaction_response['local-state-delta'])

# Update existing application
def update_app(client, private_key, app_id, approval_program, clear_program): 
    print("Updating existing app")

    # Declare sender
    sender = account.address_from_private_key(private_key)

    # Get node suggested parameters
    params = client.suggested_params()
    params.flat_fee = True
    params.fee = 1000

    # Create unsigned transaction
    txn = transaction.ApplicationUpdateTxn(sender, params, app_id, \
                                            approval_program, clear_program) #, app_args)

    # Sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # Send transaction
    client.send_transactions([signed_txn])

    # Await confirmation
    common.wait_for_confirmation(client, tx_id)

    # Display results
    transaction_response = client.pending_transaction_info(tx_id)
    app_id = transaction_response['txn']['txn']['apid']
    print("Updated existing app-id: ", app_id)

# Delete application
def delete_app(client, private_key, index): 
    print("Deleting app")

    # Declare sender
    sender = account.address_from_private_key(private_key)

    # Get node suggested parameters
    params = client.suggested_params()
    params.flat_fee = True
    params.fee = 1000

    # Create unsigned transaction
    txn = transaction.ApplicationDeleteTxn(sender, params, index)

    # Sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # Send transaction
    client.send_transactions([signed_txn])

    # Await confirmation
    common.wait_for_confirmation(client, tx_id)

    # Display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("Deleted app-id: ",transaction_response['txn']['txn']['apid'])    

# Close out from application
def close_out_app(client, private_key, index): 
    # Declare sender
    sender = account.address_from_private_key(private_key)
    print("Closing out app for account: ", sender)

    # Get node suggested parameters
    params = client.suggested_params()
    params.flat_fee = True
    params.fee = 1000

    # Create unsigned transaction
    txn = transaction.ApplicationCloseOutTxn(sender, params, index)

    # Sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # Send transaction
    client.send_transactions([signed_txn])

    # Await confirmation
    common.wait_for_confirmation(client, tx_id)

    # Display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("Closed out from app-id: ",transaction_response['txn']['txn']['apid'])

# Clear application
def clear_app(client, private_key, index): 
    # Declare sender
    sender = account.address_from_private_key(private_key)
    print("Clearing app for account: ", sender)

    # Get node suggested parameters
    params = client.suggested_params()
    params.flat_fee = True
    params.fee = 1000

    # Create unsigned transaction
    txn = transaction.ApplicationClearStateTxn(sender, params, index)

    # Sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # Send transaction
    client.send_transactions([signed_txn])

    # Await confirmation
    common.wait_for_confirmation(client, tx_id)

    # Display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("Cleared app-id: ",transaction_response['txn']['txn']['apid'])    

def parse_config():
    err_msg = """Malformed configuration file: """

    registrar = None
    accounts = {}
    APP_ID = None
    
    # Parse the configuration file to extract the `registrar`, `accounts` and `APP_ID`
    with open(CONFIG_FILE, 'r') as cfile:
        config = yaml.safe_load(cfile)

        for k, v in config.items():
            if k == 'APP_ID':
                if type(v) == int:
                    APP_ID = v
                else:
                    raise ValueError(err_msg + "APP_ID must be an int")

            elif k == 'registrar':
                if type(v) == str:
                    registrar = v
                else:
                    raise ValueError(err_msg + "registrar must be a string")

            else: 
                # This must be an account
                if 'mnemonic' in v and type(v['mnemonic']) == str:
                    accounts[k] = v['mnemonic']
                else:
                    raise ValueError(err_msg + "account must be a string of mnemonic keywords")

    # Make sure all of the return items have been set
    if registrar == None or accounts == {} or APP_ID == None:
        raise ValueError(err_msg + "Missing one of registrar, accounts or APP_ID")

    # Make sure that the `registrar` is a supplied account
    if registrar not in accounts:
        raise ValueError(err_msg + "registrar account mnemonic not supplied")

    # Return the parsed values
    return registrar, accounts, APP_ID

def main():
    help_msg = """Available commands:
        deploy: Deploy this smart contract for the first time
        update: Update this smart contract with new TEAL code
        opt-in <account-name>: Opt-in an account into this smart contract
        close-out <account-name>: Close-out an account from this smart contract
        delete: Delete this smart contract
        clear <account-name>: Clear this smart contract
        issue-diploma <account-name> <diploma-metadata>: Issue a degree to an account
        revoke-diploma <account-name>: Nullify the diploma of an account
        inspect <account-name>: Inspect an account's diploma on the Algorand blockchain
        inspect-global <creator-name>: Inspect this smart contract's global state
        reassign-registrar <account-name>: Assign an account to be the current registrar
        help: Print this help message""" 

    if len(sys.argv) < 2:
        print("Must supply at least command argument")
        print(help_msg)
        return

    try:
        registrar, accounts, APP_ID = parse_config()
    except ValueError as e:
        # There was an error
        print(e)
        return

    # Initialize an `AlgodClient`
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # Define the public and private keys
    pub_keys = {name: common.get_public_key_from_mnemonic(mnemonic) for (name, mnemonic) in accounts.items()}
    priv_keys = {name: common.get_private_key_from_mnemonic(mnemonic) for (name, mnemonic) in accounts.items()}

    if sys.argv[1] == "deploy" or sys.argv[1] == "update":
        # The `deploy` and `update` commands take no additional arguments
        if len(sys.argv) != 2:
            print(help_msg)
            return

        # Read the smart contract source files
        smart_contract_file = open("./assets/diplom_smart_contract.teal", "rb")
        smart_contract_source = smart_contract_file.read()
        smart_contract_program = common.compile_program(algod_client, smart_contract_source)

        clear_program_file = open("./assets/clear_program.teal", "rb")
        clear_program_source = clear_program_file.read()
        clear_program = common.compile_program(algod_client, clear_program_source)

        # If this is a first time deploy
        if sys.argv[1] == "deploy":
            # Create the diploma application
            app_id = create_app(algod_client, priv_keys[registrar], smart_contract_program, clear_program, global_schema, local_schema)

            print("Record the APP_ID {} in {}".format(app_id, CONFIG_FILE))
        elif sys.argv[1] == "update":
            # This is a update to the smart contract
            update_app(algod_client, priv_keys[registrar], APP_ID, smart_contract_program, clear_program)

        # Clean up the source files
        smart_contract_file.close()
        clear_program_file.close()

    elif sys.argv[1] == "opt-in":
        # The `opt-in` command takes one additional argument
        if len(sys.argv) != 3:
            print(help_msg)
            return

        account = sys.argv[2]

        # Opt-in to the `account`
        opt_in_app(algod_client, priv_keys[account], APP_ID)

    elif sys.argv[1] == "close-out":
        # The `close-out` command takes one additional arguments
        if len(sys.argv) != 3:
            print(help_msg)
            return

        account = sys.argv[2]

        # Close out the `account`
        close_out_app(algod_client, priv_keys[account], APP_ID)

    elif sys.argv[1] == "delete":
        # The `delete` command takes no additional arguments
        if len(sys.argv) != 2:
            print(help_msg)
            return

        delete_app(algod_client, priv_keys[registrar], APP_ID)

    elif sys.argv[1] == "clear":
        # The `clear` command takes one additional arguments
        if len(sys.argv) != 3:
            print(help_msg)
            return

        account = sys.argv[2]
        clear_app(algod_client, priv_keys[account], APP_ID)

    elif sys.argv[1] == "issue-diploma":
        # The `issue-diploma` command takes two additional arguments
        if len(sys.argv) != 4:
            print(help_msg)
            return

        student = sys.argv[2]
        diploma_metadata = sys.argv[3]

        app_args = [b'issue_diploma', bytes(diploma_metadata, 'utf-8')]
        accounts = [pub_keys[student]]

        print("Issuing diploma for {}: {}".format(student, diploma_metadata))

        # Call application with the relevant arguments
        call_app(algod_client, priv_keys[registrar], APP_ID, app_args, accounts)

    elif sys.argv[1] == "revoke-diploma":
        # The `revoke-diploma` command takes one additional argument
        if len(sys.argv) != 3:
            print(help_msg)
            return

        student = sys.argv[2]

        app_args = [b'revoke_diploma']
        accounts = [pub_keys[student]]

        print("Revoking diploma for {}".format(student))

        # Call application with the relevant arguments
        call_app(algod_client, priv_keys[registrar], APP_ID, app_args, accounts)

    elif sys.argv[1] == "inspect":
        # The `inspect` command takes one additional argument
        if len(sys.argv) != 3:
            print(help_msg)
            return

        # Inspect an account supplied by name
        account = sys.argv[2]
        common.read_local_state(algod_client, pub_keys[account], APP_ID)

    elif sys.argv[1] == "inspect-global":
        # The `inspect-global` command takes one additional argument
        if len(sys.argv) != 3:
            print(help_msg)
            return

        # Inspect this app by its `creator`
        creator = sys.argv[2]
        common.read_global_state(algod_client, pub_keys[creator], APP_ID)

    elif sys.argv[1] == "reassign-registrar":
        # The `reassign-registrar` command takes one additional argument
        if len(sys.argv) != 3:
            print(help_msg)
            return

        new_registrar = sys.argv[2]

        app_args = [b'reassign_registrar']
        accounts = [pub_keys[new_registrar]]

        print("Reassigning the registrar to be {}".format(new_registrar))

        # Call application with the relevant arguments
        call_app(algod_client, priv_keys[registrar], APP_ID, app_args, accounts)

    elif sys.argv[1] == "help":
        print(help_msg)

    else:
        print("Invalid command and arguments: {}".format(sys.argv[1:]))
        print(help_msg)

    # TODO: Handle multiple diplomas

if __name__ == '__main__':
    main()
