from pyteal import *

def clear_program():
    """A clear program that always approves."""
    return Return(Int(1))

if __name__ == "__main__":
    print(compileTeal(clear_program(), Mode.Application, version=5))
