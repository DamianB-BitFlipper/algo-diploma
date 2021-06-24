import sys

from algosdk.future import transaction
from algosdk import account
from algosdk.v2client import algod

import common

registrar_mnemonic = "candy eager deal flush pull elite job second art divorce task market cattle term write reform month sphere scissors fluid pumpkin feed issue abstract aunt"
student_mnemonic = "learn cable switch safe increase maze garage museum royal nature dance pair uncle neither become practice bench ball giant curious fabric indicate token able release"

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

def main():
    # TODO: Write this to artifacts file
    APP_ID = 11

    help_msg = """Available commands:
        deploy: Deploy this smart contract for the first time
        update: Update this smart contract with new TEAL code
        opt-in: Opt-in the registrar and student to this smart contract
        issue-diploma: Issue an MIT degree to Damian
        inspect: Inspect Damian's MIT degree on the Algorand blockchain
        """ 

    if len(sys.argv) < 2:
        print(help_msg)
        return

    # Initialize an algodClient
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # Define the public keys
    registrar_public_key = common.get_public_key_from_mnemonic(registrar_mnemonic)
    student_public_key = common.get_public_key_from_mnemonic(student_mnemonic)

    # Define the private keys
    registrar_private_key = common.get_private_key_from_mnemonic(registrar_mnemonic)
    student_private_key = common.get_private_key_from_mnemonic(student_mnemonic)

    if sys.argv[1] == "deploy" or sys.argv[1] == "update":
        # Read the smart contract source files
        smart_contract_file = open("./assets/diplom_smart_contract.teal", "rb")
        smart_contract_source = smart_contract_file.read()
        smart_contract_program = common.compile_program(algod_client, smart_contract_source)

        clear_program_file = open("./assets/clear_program.teal", "rb")
        clear_program_source = clear_program_file.read()
        clear_program = common.compile_program(algod_client, clear_program_source)

        # If this is a first time deploy
        if sys.argv[1] == "deploy":
            # TODO: Save the `app_id` to some ./artifacts JSON file
            #
            # Create the diploma application
            app_id = create_app(algod_client, registrar_private_key, smart_contract_program, clear_program, global_schema, local_schema)
        elif sys.argv[1] == "update":
            # This is a update to the smart contract
            update_app(algod_client, registrar_private_key, APP_ID, smart_contract_program, clear_program)

        # Clean up the source files
        smart_contract_file.close()
        clear_program_file.close()

    elif sys.argv[1] == "opt-in":
        # Opt-in both the registrar and the student
        opt_in_app(algod_client, registrar_private_key, 11)
        opt_in_app(algod_client, student_private_key, 11)

    elif sys.argv[1] == "issue-diploma":
        app_args = [b'issue_diploma', b'Damian Barabonkov,MIT,2020,BSc,Computer Science and Engineering']
        accounts = [student_public_key]

        # Call application with the relevant arguments
        call_app(algod_client, registrar_private_key, APP_ID, app_args, accounts)

    elif sys.argv[1] == "inspect":
        # TODO: Make the inspect more human readable
        common.read_local_state(algod_client, registrar_public_key, APP_ID)

    # TODO: Handle registrar reassignment
    # TODO: Handle diploma revocation
    # TODO: Handle multiple diplomas
    # TODO: Handle smart contract deletion

if __name__ == '__main__':
    main()
