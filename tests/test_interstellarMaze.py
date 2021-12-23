from pytest import fixture
from brownie import chain, reverts

@fixture
def admin(accounts):
  return accounts[0]

@fixture
def alice(accounts):
  return accounts[1]

@fixture
def interstellarMaze(InterstellarMaze, admin):
  return InterstellarMaze.deploy({'from': admin})

@fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_set_startTime(interstellarMaze, admin, alice):
  ONE_DAY = 86400
  START_TIME = chain.time() + ONE_DAY
  WRONG_START_TIME = chain.time() - ONE_DAY

  with reverts('Can only set future timestamp'):
    interstellarMaze.setStartTime(WRONG_START_TIME, {'from':admin})
  
  with reverts('Ownable: caller is not the owner'):
    interstellarMaze.setStartTime(START_TIME, {'from':alice})
  
  interstellarMaze.setStartTime(START_TIME, {'from':admin})


def test_release_num(interstellarMaze, admin):
  DAILY_RELEASE = 333
  ONE_DAY = 86400
  START_TIME = chain.time() + ONE_DAY

  interstellarMaze.setStartTime(START_TIME, {'from':admin})

  print('\n')
  
  print(f'\tcurrent time: {chain.time()}')
  with reverts('The minting is not started yet'):
    interstellarMaze.releasedNum()
  print(f'\trevert: The minting is not started yet\n')
  
  # time travel to the contract start time
  # day 1
  chain.mine(timedelta=ONE_DAY + 1)
  print(f'\tcurrent time: {chain.time()}')
  released = interstellarMaze.releasedNum()
  print(f'\treleased nfts: {released}\n')
  assert released == DAILY_RELEASE

  # day 2
  chain.mine(timedelta=ONE_DAY)
  print(f'\tcurrent time: {chain.time()}')
  released = interstellarMaze.releasedNum()
  print(f'\treleased nfts: {released}\n')
  assert released == DAILY_RELEASE * 2

  # day 3
  chain.mine(timedelta=ONE_DAY)
  print(f'\tcurrent time: {chain.time()}')
  released = interstellarMaze.releasedNum()
  print(f'\treleased nfts: {released}\n')
  assert released == DAILY_RELEASE * 3

  # day 4
  chain.mine(timedelta=ONE_DAY)
  print(f'\tcurrent time: {chain.time()}')
  released = interstellarMaze.releasedNum()
  print(f'\treleased nfts: {released}\n')
  assert released == DAILY_RELEASE * 3

def test_mint(interstellarMaze, admin, alice):
  ONE_DAY = 86400
  TOTAL_RESERVE_NFTS = 150
  START_TIME = chain.time() + ONE_DAY

  interstellarMaze.setStartTime(START_TIME, {'from':admin})

  print('\n')
  
  print(f'\tcurrent time: {chain.time()}')
  with reverts('The minting is not started yet'):
    interstellarMaze.mint({'from':admin})
  print(f'\trevert: The minting is not started yet\n')

  # time travel to the contract start time
  # day 1
  chain.mine(timedelta=ONE_DAY + 1)
  # admin mint
  print(f'\tcurrent time: {chain.time()}')
  for i in range(TOTAL_RESERVE_NFTS):
    interstellarMaze.mint({'from': admin})
    print(f'\tbalance of {admin}: {interstellarMaze.balanceOf(admin)}')
    print(f'\towner of nft{i}: {interstellarMaze.ownerOf(i)}')
    print(f'\turl of nft{i}: {interstellarMaze.tokenURI(i)}')
    print(f'\thash of nft{i}: {interstellarMaze.tokenIdToHash(i)}\n')
  
  # exceed owner mint limit
  with reverts('Mint more than reserved for owner'):
    interstellarMaze.mint({'from': admin})
  print(f'\tmint exceed the owner mint limit, got error: Mint more than reserved for owner\n')

  # normal user mint
  # day 1
  interstellarMaze.mint({'from': alice})
  print(f'\talice mint one nft, total {interstellarMaze.balanceOf(alice)} NTF')
  with reverts('The address has minted today'):
    interstellarMaze.mint({'from': alice})
  print('\tif alice mint again at today, she will got error: The address is minted at today')

  # day 2
  chain.mine(timedelta=ONE_DAY)
  interstellarMaze.mint({'from': alice})
  print(f'\tif alice mint one day after, she can mint again, total {interstellarMaze.balanceOf(alice)} NTFs')

  # day 3
  chain.mine(timedelta=ONE_DAY)
  interstellarMaze.mint({'from': alice})
  print(f'\tif alice mint one day after, she can mint again, total {interstellarMaze.balanceOf(alice)} NFTs')

  with reverts('One address can only mint 3 NFTs'):
    interstellarMaze.mint({'from': alice})
  print(f'\tif alice mint again, she will got error: One address can only mint {interstellarMaze.balanceOf(alice)} NFTs')

  # day 4
  chain.mine(timedelta=ONE_DAY)
  with reverts('One address can only mint 3 NFTs'):
    interstellarMaze.mint({'from': alice})
  print(f'\tif alice mint again at today, she will got error: One address can only mint {interstellarMaze.balanceOf(alice)} NFTs')

def test_mint_event(interstellarMaze, admin, alice):
  ONE_DAY = 86400
  START_TIME = chain.time() + ONE_DAY

  interstellarMaze.setStartTime(START_TIME, {'from':admin})

  print('\n')
  
  # time travel to the contract start time
  # day 1
  chain.mine(timedelta=ONE_DAY + 1)
  # admin mint
  tx = interstellarMaze.mint({'from': admin})
  print(f'\ttx events {tx.events}')
  assert tx.events['Mint']['owner'] == admin

  tx = interstellarMaze.mint({'from': alice})
  print(f'\ttx events {tx.events}')
  assert tx.events['Mint']['owner'] == alice