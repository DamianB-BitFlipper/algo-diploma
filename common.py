import base64

from algosdk import mnemonic

# Helper function to compile program source
def compile_program(client, source_code):
    compile_response = client.compile(source_code.decode('utf-8'))
    return base64.b64decode(compile_response['result'])

# Helper function that converts a mnemonic passphrase into a private signing key
def get_private_key_from_mnemonic(mn):
    private_key = mnemonic.to_private_key(mn)
    return private_key

# Helper function that converts a mnemonic passphrase into a public key
def get_public_key_from_mnemonic(mn):
    public_key = mnemonic.to_public_key(mn)
    return public_key

# Helper function that waits for a given txid to be confirmed by the network
def wait_for_confirmation(client, txid):
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation...")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo

# Read user local state
def read_local_state(client, addr, app_id):
    results = client.account_info(addr)
    local_state = results['apps-local-state'][0]
    for index in local_state:
        if local_state[index] == app_id:
            print(f"local_state of account {addr} for app_id {app_id}: ", local_state['key-value'])

# Read app global state
def read_global_state(client, addr, app_id):   
    results = client.account_info(addr)
    apps_created = results['created-apps']
    for app in apps_created:
        if app['id'] == app_id:
            print(f"global_state for app_id {app_id}: ", app['params']['global-state'])
