from solcx import compile_files
import os
import logging

logger = logging.getLogger(__name__)


def compile_contract(file_path):
    compiled_sol_from_file = compile_files([file_path, ], output_values=["abi", "bin"])
    return compiled_sol_from_file


def get_contract_interfaces(compiled_contracts, smart_contract: str):
    #
    # To identify the main contract
    contract_interfaces, scid = {}, ""

    while True:
        try:
            _id, _interface = compiled_contracts.popitem()
            contract_interfaces[_id] = _interface

            if smart_contract.lower() in _id.lower():
                scid = _id

        except KeyError as exc:  # this is expected
            break

    return contract_interfaces, scid


def get_abi_bytecode(file_path):
    # Compile the files
    compiled_sol = compile_contract(file_path)

    # Extract the main contract
    class_name = str(file_path).split("/")[-1].replace(".sol", "")
    interfaces, _id = get_contract_interfaces(compiled_sol, class_name)

    # Extract bytecode and abi for the main contract only
    bytecode = interfaces[_id]["bin"]
    abi = interfaces[_id]["abi"]

    return abi, bytecode

def maybe_install_compiler(path_to_contracts):
    # This is a dummy contract
    file_name = "TestInstall.sol"
    file_path = os.path.join(path_to_contracts, file_name)

    try:
        compile_contract(file_path)

    except Exception as exc:
        logger.info(f"Installing Solidity compiler...")
        from solcx import install_solc
        install_solc()
        logger.info(f"Done.")
