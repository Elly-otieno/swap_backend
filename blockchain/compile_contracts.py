import os
import json
from solcx import compile_files, install_solc

def compile_contracts():
    print("Installing solc 0.8.20...")
    install_solc('0.8.20')

    contract_dir = 'blockchain/contracts'
    abi_dir = 'blockchain/abis'
    os.makedirs(abi_dir, exist_ok=True)

    contracts = [
        os.path.join(contract_dir, 'UserRegistry.sol'),
        os.path.join(contract_dir, 'SIMSwapManager.sol'),
        os.path.join(contract_dir, 'AccessControl.sol')
    ]

    print(f"Compiling contracts: {contracts}")
    compiled_sol = compile_files(
        contracts,
        output_values=['abi', 'bin'],
        solc_version='0.8.20'
    )

    for contract_id, compiled in compiled_sol.items():
        contract_name = contract_id.split(':')[-1]
        abi = compiled['abi']
        bytecode = compiled['bin']

        abi_file = os.path.join(abi_dir, f"{contract_name}.json")
        with open(abi_file, 'w') as f:
            json.dump(abi, f, indent=2)

        print(f"Generated ABI for {contract_name} in {abi_file}")

        # Also save bytecode for deployment if needed
        bytecode_file = os.path.join(abi_dir, f"{contract_name}_bytecode.txt")
        with open(bytecode_file, 'w') as f:
            f.write(bytecode)

if __name__ == "__main__":
    compile_contracts()
