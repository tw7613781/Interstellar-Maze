const { ethers, Contract } = require('ethers');
const reborn = require('../build/contracts/RebornPiecesTestV2_5.json')

const nodeHttpUrl = 'https://rpc-mumbai.maticvigil.com/';

const provider = new ethers.providers.JsonRpcProvider(nodeHttpUrl);

async function main() {
  const network = await provider.getNetwork();
  if (!network) {
    console.log('failed to connect network');
  } else {
    console.log(`connected with ${network.name} and id ${network.chainId}`);
  }

  const nftAddr = '0xdc9e8faDe38eE9E2Eb43761f1553CD2360ecAEac';
  const nft = new Contract(nftAddr, reborn.abi, provider);

  // 列出Mint event所有的历史事件,但是因为rpc server的原因,只能返回最近1000个blocks的events
  // const _mintEventsFilter = nft.filters.Mint(null);
  // const _mintEvents = await nft.queryFilter(_mintEventsFilter, 23767420);
  // console.log(_mintEvents[0].args.tokenId.toString(), _mintEvents[0].args.owner, _mintEvents[0].args.hash);

  console.log('Listen on event Mint ...')
  nft.on('Mint', (tokenId, owner, hash) => {
    console.log(`TokenId: ${tokenId.toString()} - Owner: ${owner} - Hash: ${hash}`);
  })
}

main();
