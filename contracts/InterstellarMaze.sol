// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";


contract InterstellarMaze is ERC721, ReentrancyGuard, Ownable {
  uint256 public constant TOTAL_SUPPLY = 6999;
  mapping(uint256 => bytes32) public tokenIdToHash;
  mapping(address => uint256) public whitelisted;
  uint256 public tokenId = 1;

  event Mint(uint256 tokenId, address owner, bytes32 hash);
  constructor() ERC721("Interstellar Maze", "IM") {}

  function mint() public nonReentrant returns (uint256){
    
    uint256 _newId = tokenId;
    require(_newId <= TOTAL_SUPPLY, "Already sold out");
    
    if(whitelisted[msg.sender] > 0) {
      require(balanceOf(msg.sender) < whitelisted[msg.sender], "Out of allowable range");
    } else {
      require(balanceOf(msg.sender) < 1, "You already have one");
    }

    _safeMint(msg.sender, _newId);
    bytes32 _hash = _getHash(_newId, msg.sender);
    tokenIdToHash[_newId] = _hash;
    emit Mint(_newId, msg.sender, _hash);
    tokenId ++;
    return _newId;
  }

  function addWhitelist(address _addr, uint256 _incNum) public onlyOwner {
    require(_addr != address(0), "Address zero is not allowed");
    require(_incNum != 0, "Please allow at lease 1 token");
    whitelisted[_addr] += _incNum;
  }

  function _baseURI() internal pure override returns (string memory) {
    return "https://www.btcart.cn/api/nft/";
  }

  function _getHash(uint256 _counter, address _sender) internal view returns (bytes32) {
    return keccak256(abi.encodePacked(name(), _counter, block.number, _sender));
  }
}
