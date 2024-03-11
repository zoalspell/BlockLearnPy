from web3 import Web3
from src.config import RPC_URLS, CONTRACT_ADDRESSES, UNI_CONTRACT_ABI

def get_balance(chain: str, coin: str, address: str):
    """
    Fetches the balance of a specified coin/token for a given address on a specified blockchain.

    Parameters:
    - chain (str): The blockchain network name (e.g., 'ethereum', 'bsc').
    - coin (str): The symbol of the coin or token to check the balance of (e.g., 'eth', 'usdc').
    - address (str): The wallet address to check the balance for.

    Returns:
    - float: The balance of the specified coin/token for the given address.
    """
    # Fetch the RPC URL from the configuration based on the specified chain
    rpc = RPC_URLS[chain.lower()]
    w3 = Web3(Web3.HTTPProvider(rpc))  # Initialize the Web3 connection using the RPC URL
    address = w3.to_checksum_address(address)  # Convert the address to checksum format for consistency

    # For native blockchain currencies like Ethereum (ETH) on Ethereum and BNB on BSC
    if (coin == 'eth' and chain == 'ethereum') or (chain == 'bsc' and coin == 'bnb'):
        balance = w3.eth.get_balance(address)  # Fetch the native currency balance
        token_amount = w3.from_wei(balance, 'ether')  # Convert balance from wei to ether
        print(f"{coin.upper()} Balance: {token_amount}")
        return float(token_amount)
    else:
        # For ERC-20 tokens (or equivalent on other chains)
        token_address = w3.to_checksum_address(CONTRACT_ADDRESSES[chain.lower()][coin.lower()])
        contract = w3.eth.contract(address=token_address, abi=UNI_CONTRACT_ABI)  # Load the token contract
        token_amount = contract.functions.balanceOf(address).call()  # Call the balanceOf function for the address
        exponent = 6 if coin.lower() == 'usdc' else 18
        token_amount = token_amount * 10 ** -exponent  # Convert the balance to a human-readable format
        print(f"{coin.upper()} Balance: {token_amount}")
        return float(token_amount)

def call_contract(chain: str, contract_address: str, function_name: str, contract_abi: list,
                  function_input: tuple = None):
    """
    Call a smart contract function on a specified blockchain and return the result.

    Parameters:
    - chain (str): The blockchain network name (e.g., 'ethereum', 'bsc').
    - contract_address (str): The address of the smart contract.
    - function_name (str): The name of the function in the smart contract to call.
    - contract_abi (list): The ABI (Application Binary Interface) of the smart contract, which describes the functions and variables.
    - function_input (tuple, optional): The inputs to the smart contract function, if any.

    Returns:
    - The result of the smart contract function call.
    """
    # Fetch the RPC URL from the configuration based on the specified chain
    rpc = RPC_URLS[chain.lower()]
    # Initialize the Web3 connection using the RPC URL
    w3 = Web3(Web3.HTTPProvider(rpc))
    # Convert the contract address to checksum format for consistency
    contract_address = w3.to_checksum_address(contract_address)
    # Initialize the contract object with the provided address and ABI
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    # If no function inputs are provided, call the function without arguments
    if function_input is None:
        function = contract.functions[function_name]()
    else:
        # If function inputs are provided, unpack them and call the function with arguments
        function = contract.functions[function_name](*function_input)

    # Execute the function call and return the result
    function_call = function.call()
    print(f"Function Call Result: {function_call}")
    return function_call

