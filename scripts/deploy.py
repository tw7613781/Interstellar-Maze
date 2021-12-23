from brownie import InterstellarMaze
### Third-Party Packages ###
from brownie.network import accounts, Chain
from brownie.network.gas.strategies import ExponentialScalingStrategy
from eth_account.account import Account, ValidationError
from yaml import safe_load

TERM_RED  = '\033[1;31m'
TERM_NFMT = '\033[0;0m'

def main():
  ### Load Account to use ###
  acct: Account = None
  chain: Chain  = Chain()
  print(f'Network Chain-ID: { chain }')

  file_name = 'wallet.personal_1.yml' 
  ### Load Mnemonic from YAML File ###
  try:
    with open(file_name) as f:
      content = safe_load(f)
      ### Read Mnemonic ###
      privkey = content.get('privkey', None)
      acct = accounts.add(privkey)
  except FileNotFoundError:
    print(f'{TERM_RED}Cannot find wallet mnemonic file defined at `{file_name}`.{TERM_NFMT}')
    return
  except ValidationError:
    print(f'{TERM_RED}Invalid address found in wallet mnemonic file.{TERM_NFMT}')
    return


  print(f'Account: {acct}')
  balance = acct.balance()
  print(f'Account Balance: {balance}')
  if balance == 0:
    return # If balance is zero, exits


  ### Set Gas Price ##
  gas_strategy = ExponentialScalingStrategy('3.5 gwei', '10 gwei')

  ### Deployment ###
  interstellarMaze = InterstellarMaze.deploy({ 'from': acct, 'gas_price': gas_strategy })
  print(f'InterstellarMaze: { interstellarMaze }\n\n')

  # set start time