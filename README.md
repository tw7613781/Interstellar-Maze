# Interstellar Maze

是一个可以铸造ERC721 NFT的合约

## 铸造逻辑
 
1. 一共6999个NFT
 
2. 每个地址可以mint一个

3. 支持白名单，而且白名单可以设置指定地址可以锻造次数

同时每一个NTF在铸造的时候会生成一串32个bytes的hash,可以用于p5js生成NFT图像.

## 其他方的工作(这里没有实现)

### 前端
跟合约的mint()函数交互,让终端用户能够铸造NFT

### 后端
监听合约Mint事件,如果有新的NFT被铸造,利用tokenIdToHash(_tokenId)或者从Mint事件中获取此NFT的hash,生成NFT图以及相应的meta data.

Mint事件的数据例子

```
'Mint': [OrderedDict([('tokenId', 0), ('owner', '0x66aB6D9362d4F35596279692F0251Db635165871'), ('hash', 0x67b5cc15bdaa50795d11ef90a66a2deb52d8a8a3339e1d596a881bbb85370010)])]}
```

## 讨论

### NFT的hash

此hash要求每一个tokenId的NFT有一个独特的hash
```
function _getHash(uint _counter, address _sender) internal view returns (bytes32) {
  return keccak256(abi.encodePacked(name(), _counter, block.number, _sender));
}
```
使用合约名字,tokenId,块高度和铸造地址来保证它的独特性.