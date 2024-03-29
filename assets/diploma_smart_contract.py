# This example is provided for informational purposes only and has not been audited for security.
from pyteal import *

var_registrar = Bytes("registrar")
var_diploma = Bytes("diploma")
var_degree_duration = Bytes("degree_duration")

def diploma_program():
    """
    This stateful smart contract issues students' diplomas.
    """
    # Code block invoked during contract initialization. Sets the
    # `registrar` to be the sender (creator) of this smart contract
    init_contract = Seq([
        App.globalPut(var_registrar, Txn.sender()),
        Return(Int(1))
    ])

    # Checks if the sender of the current transaction invoking this
    # smart contract is the current registrar
    is_registrar = Txn.sender() == App.globalGet(var_registrar)

    # Code block invoked during diploma issuance. Only the registrar
    # may invoke this block with three arguments and one account supplied.
    # The first argument was "issue_diploma" used by the control flow 
    # below. The second argument is the diploma metadata which is
    # set to the local storage of the supplied account (Int(1)). The
    # third argument is the duration in years that the degree took.
    diploma_metadata = Txn.application_args[1]
    degree_duration = Txn.application_args[2]
    issue_diploma = Seq([
        # Sanity checks
        Assert(is_registrar),
        Assert(Txn.application_args.length() == Int(3)),
        Assert(Txn.accounts.length() == Int(1)),
        
        App.localPut(Int(1), var_diploma, diploma_metadata),
        App.localPut(Int(1), var_degree_duration, Btoi(degree_duration)),
        Return(Int(1))
    ])

    # Code block invoked during diploma revocation. Only the registrar
    # may invoke this block with one argument and one account supplied.
    # The first argument was "revoke_diploma" used by the control flow 
    # below. The local storage containing the diploma metadata of the 
    # supplied account (Int(1)) is deleted.
    revoke_diploma = Seq([
        # Sanity checks
        Assert(is_registrar),
        Assert(Txn.application_args.length() == Int(1)),
        Assert(Txn.accounts.length() == Int(1)),
        
        App.localDel(Int(1), var_diploma),
        App.localDel(Int(1), var_degree_duration),
        Return(Int(1))
    ])

    # Code block invoked during registrar reassignment. Only the registrar
    # may invoke this block with one argument and one account supplied.
    # The first argument was "reassign_registrar" used by the control
    # flow below. The global variable containing the current registrar
    # is set to the supplied account (Txn.accounts[1])
    new_registrar = Txn.accounts[1]
    reassign_registrar = Seq([
        # Sanity checks
        Assert(is_registrar),
        Assert(Txn.accounts.length() == Int(1)),
        
        Assert(Txn.application_args.length() == Int(1)),
        App.globalPut(var_registrar, new_registrar),
        Return(Int(1))
    ])

    # Control flow logic of the smart contract
    program = Cond(
        [Txn.application_id() == Int(0), init_contract],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_registrar)],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(is_registrar)],
        [Txn.on_completion() == OnComplete.OptIn, Return(Int(1))],
        [Txn.on_completion() == OnComplete.CloseOut, Return(Int(1))],
        [Txn.application_args[0] == Bytes("issue_diploma"), issue_diploma],
        [Txn.application_args[0] == Bytes("revoke_diploma"), revoke_diploma],
        [Txn.application_args[0] == Bytes("reassign_registrar"), reassign_registrar]
    )

    return program

if __name__ == "__main__":
    print(compileTeal(diploma_program(), Mode.Application, version=5))
