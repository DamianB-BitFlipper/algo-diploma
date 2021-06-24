from pyteal import *

var_registrar = Bytes("registrar")

def diplom_program():
    """
    This stateful smart contract issues students' diplomas
    """
    init_contract = Seq([
        App.globalPut(var_registrar, Txn.sender()),
        Return(Int(1))
    ])

    is_registrar = Txn.sender() == App.globalGet(var_registrar)

    diploma_metadata = Txn.application_args[1]
    issue_diploma = Seq([
        Assert(is_registrar),
        Assert(Txn.application_args.length() == Int(2)),
        App.localPut(Int(1), Bytes("diploma"), diploma_metadata),
        Return(Int(1))
    ])

    new_registrar = Txn.accounts[1]
    reassign_registrar = Seq([
        Assert(is_registrar),
        Assert(Txn.application_args.length() == Int(2)),
        App.globalPut(var_registrar, new_registrar),
        Return(Int(1))
    ])

    program = Cond(
        [Txn.application_id() == Int(0), init_contract],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_registrar)],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(is_registrar)],
        [Txn.on_completion() == OnComplete.CloseOut, Return(Int(1))],
        [Txn.on_completion() == OnComplete.OptIn, Return(Int(1))],
        [Txn.application_args[0] == Bytes("issue_diploma"), issue_diploma],
        [Txn.application_args[0] == Bytes("reassign_registrar"), reassign_registrar]
    )

    return program

if __name__ == "__main__":
    print(compileTeal(diplom_program(), Mode.Application))
