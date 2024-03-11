from src.function import *
from src.config import *

# Check the balance of Ethereum (ETH) for a given wallet address on the Ethereum blockchain.
test_address_1 = "0x90dBFfA429Ff0cA7A256D261bf7BA97A0DDb17E7"
get_balance(chain="ethereum", coin="eth", address=test_address_1)


# Check the balance of USDC (a stablecoin pegged to the USD) for a given wallet address on the Ethereum blockchain.
test_address_2 = "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"
get_balance(chain="ethereum", coin="usdc", address=test_address_2)

# Get the liquidity pool contract address for a specific token pair (WBNB-USDC) on the Binance Smart Chain (BSC) using Uniswap V2's Factory contract.
rpc = RPC_URLS['bsc']
w3 = Web3(Web3.HTTPProvider(rpc))  # Initialize the Web3 connection using the BSC RPC URL.
factory_address = w3.to_checksum_address("0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73")
wbnb_address = w3.to_checksum_address(CONTRACT_ADDRESSES['bsc']['wbnb'])
usdc_address = w3.to_checksum_address(CONTRACT_ADDRESSES['bsc']['usdc'])

# The call_contract function is used to interact with the Uniswap V2 Factory contract to find the LP contract address for the WBNB-USDC pair.
pair_contract = call_contract(chain='bsc', contract_address=factory_address, function_name='getPair',
                             contract_abi=UNI_FACTORY_ABI, function_input=(wbnb_address, usdc_address))
