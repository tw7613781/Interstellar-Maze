from pytest import fixture
import brownie

@fixture
def admin(accounts):
  return accounts[0]

@fixture
def alice(accounts):
  return accounts[1]

@fixture
def nftFactory(NFTFactory, admin):
  return NFTFactory.deploy({'from': admin})

@fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_release_num(nftFactory):
  chain = brownie.network.Chain()
  START_TIME = 1639274400
  DAILY_RELEASE = 333
  ONE_DAY = 86400

  print('\n')
  
  print(f'\tcurrent time: {chain.time()}')
  with brownie.reverts('the minting is not started yet'):
    nftFactory.releasedNum()
  print(f'\trevert: the minting is not started yet\n')
  
  # time travel to the contract start time
  # day 1
  chain.sleep(START_TIME - chain.time() + 1)
  chain.mine(1)
  print(f'\tcurrent time: {chain.time()}')
  released = nftFactory.releasedNum()
  print(f'\treleased nfts: {released}\n')
  assert released == DAILY_RELEASE

  # day 2
  chain.sleep(ONE_DAY)
  chain.mine(1)
  print(f'\tcurrent time: {chain.time()}')
  released = nftFactory.releasedNum()
  print(f'\treleased nfts: {released}\n')
  assert released == DAILY_RELEASE * 2

  # day 3
  chain.sleep(ONE_DAY)
  chain.mine(1)
  print(f'\tcurrent time: {chain.time()}')
  released = nftFactory.releasedNum()
  print(f'\treleased nfts: {released}\n')
  assert released == DAILY_RELEASE * 3

  # day 4
  chain.sleep(ONE_DAY)
  chain.mine(1)
  print(f'\tcurrent time: {chain.time()}')
  released = nftFactory.releasedNum()
  print(f'\treleased nfts: {released}\n')
  assert released == DAILY_RELEASE * 3

def test_mint(nftFactory, admin, alice):
  chain = brownie.network.Chain()
  START_TIME = 1639274400
  DAILY_RELEASE = 333
  ONE_DAY = 86400
  TOTAL_RESERVE_NFTS = 150

  print('\n')
  
  print(f'\tcurrent time: {chain.time()}')
  with brownie.reverts('the minting is not started yet'):
    nftFactory.mint({'from':admin})
  print(f'\trevert: the minting is not started yet\n')

  # time travel to the contract start time
  # day 1
  chain.sleep(START_TIME - chain.time() + 1)
  chain.mine(1)

  # admin mint
  print(f'\tcurrent time: {chain.time()}')
  for i in range(TOTAL_RESERVE_NFTS):
    nftFactory.mint({'from': admin})
    print(f'\tbalance of {admin}: {nftFactory.balanceOf(admin)}')
    print(f'\towner of nft{i}: {nftFactory.ownerOf(i)}')
    print(f'\turl of nft{i}: {nftFactory.tokenURI(i)}\n')
  
  # exceed owner mint limit
  with brownie.reverts('mint more than reserved'):
    nftFactory.mint({'from': admin})
  print(f'\tmint exceed the owner mint limit, got error: mint more than reserved\n')

  # normal user mint
  # day 1
  nftFactory.mint({'from': alice})
  print(f'\talice mint one nft, total {nftFactory.balanceOf(alice)} NTF')
  with brownie.reverts('the address is mint at today'):
    nftFactory.mint({'from': alice})
  print('\tif alice mint again at today, she will got error: the address is mint at today')

  # day 2
  chain.sleep(ONE_DAY)
  chain.mine(1)
  nftFactory.mint({'from': alice})
  print(f'\tif alice mint one day after, she can mint again, total {nftFactory.balanceOf(alice)} NTFs')

  # day 3
  chain.sleep(ONE_DAY)
  chain.mine(1)
  nftFactory.mint({'from': alice})
  print(f'\tif alice mint one day after, she can mint again, total {nftFactory.balanceOf(alice)} NFTs')

  with brownie.reverts('one address can only mint 3 nfts'):
    nftFactory.mint({'from': alice})
  print(f'\tif alice mint again, she will got error: one address can only mint {nftFactory.balanceOf(alice)} nfts')

  # day 4
  chain.sleep(ONE_DAY)
  chain.mine(1)
  with brownie.reverts('one address can only mint 3 nfts'):
    nftFactory.mint({'from': alice})
  print(f'\tif alice mint again at today, she will got error: one address can only mint {nftFactory.balanceOf(alice)} nfts')