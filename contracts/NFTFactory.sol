pragma solidity ^0.8.0;

import '@openzeppelin/contracts/token/ERC721/ERC721.sol';
import '@openzeppelin/contracts/access/Ownable.sol';
import '@openzeppelin/contracts/security/ReentrancyGuard.sol';

contract NFTFactory is ERC721, ReentrancyGuard, Ownable {

  uint private counter;
  constructor()
  ERC721('Interstellar Maze', 'IM') {
    counter = 0;
  }

  function mint() public nonReentrant{
    _safeMint(_msgSender(), counter);
    counter += 1;
  }

  function _baseURI() internal view override returns (string memory) {
      return "https://helloworld.com/";
  }
}