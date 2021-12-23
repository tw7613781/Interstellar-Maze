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

def test_mint(interstellarMaze, admin, alice):

  print('\n')
  
  tx = interstellarMaze.mint({'from':alice})
  assert interstellarMaze.balanceOf(alice) == 1
  assert tx.events['Mint']['owner'] == alice
  assert tx.events['Mint']['tokenId'] == 1

  with reverts('You already have one'):
    interstellarMaze.mint({'from':alice})

  with reverts('Ownable: caller is not the owner'):
    interstellarMaze.addWhitelist(admin, 2, {'from': alice})

  interstellarMaze.addWhitelist(admin, 2, {'from': admin})

  tx = interstellarMaze.mint({'from':admin})
  assert interstellarMaze.balanceOf(admin) == 1
  assert tx.events['Mint']['owner'] == admin
  assert tx.events['Mint']['tokenId'] == 2

  tx = interstellarMaze.mint({'from':admin})
  assert interstellarMaze.balanceOf(admin) == 2
  assert tx.events['Mint']['owner'] == admin
  assert tx.events['Mint']['tokenId'] == 3
  
  with reverts('Out of allowable range'):
    tx = interstellarMaze.mint({'from':admin})

  interstellarMaze.addWhitelist(admin, 1, {'from': admin})
  tx = interstellarMaze.mint({'from':admin})
  assert interstellarMaze.balanceOf(admin) == 3
  assert tx.events['Mint']['owner'] == admin
  assert tx.events['Mint']['tokenId'] == 4
