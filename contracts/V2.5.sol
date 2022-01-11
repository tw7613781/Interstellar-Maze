// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract RebornPiecesTestV2_5 is ERC721, ReentrancyGuard, Ownable {
    uint256 public constant TOTAL_SUPPLY = 999;
    uint256 public mintForDev = 0;
    uint256 public endTime;
    uint256 public mintPrice = 11 ether;
    uint256 private whiteListNum = 0;

    mapping(uint256 => bytes32) public tokenIdToHash;
    mapping(address => bool) public iswhitelisted;
    mapping(address => uint256) whiteList;

    uint256 public tokenId = 1;

    event Mint(uint256 tokenId, address owner, bytes32 hash);
    event SetWhitelist(address _toAddr, uint256 _mintNum);

    constructor(uint256 _endTime) ERC721("RebornPiecesTest", "tRP") {
        endTime = _endTime;
    }

    function mint() external payable nonReentrant returns (uint256) {
        if (block.timestamp <= endTime) {
            /**======================1.WHITELIST======================**/
            require (
                iswhitelisted[msg.sender] && whiteList[msg.sender] == 0,
                "ERROR : You are not a whitelisted user or you have already claimed it, please wait for the activity to start"
              );
            whiteList[msg.sender] = 1;
        
        } else {
            /**======================2.SALE===========================**/
            require(msg.value >= mintPrice, "Not enough tokens to pay");
        }

        return _mintSafe(msg.sender);
    }

    function _mintSafe(address _to) internal returns (uint256) {
        uint256 _newId = tokenId;
        require(_newId <= TOTAL_SUPPLY, "Already sold out");
        _safeMint(_to, _newId);
        bytes32 _hash = _getHash(_newId, _to);
        tokenIdToHash[_newId] = _hash;
        emit Mint(_newId, _to, _hash);
        tokenId++;
        return _newId;
    }

    function mintToDev(address _devAddress)
        external
        onlyOwner
        returns (uint256)
    {
        require(mintForDev < 100, "completed");
        mintForDev++;
        return _mintSafe(_devAddress);
    }

    function addWhitelistMul(address[] calldata _addrs) public onlyOwner {
        require((whiteListNum + _addrs.length) <= 100, "only 100");
        for (uint256 i = 0; i < _addrs.length; i++) {
            if (!iswhitelisted[_addrs[i]]) {
                iswhitelisted[_addrs[i]] = true;
                whiteList[_addrs[i]] = 0;
                whiteListNum++;
            }
        }
    }

    function getWhitelistLength() external view returns (uint256) {
        return whiteListNum;
    }

    function _baseURI() internal pure override returns (string memory) {
        return "http://test.shardsrespawn.com/api/nft/";
    }

    function _getHash(uint256 _counter, address _sender)
        internal
        view
        returns (bytes32)
    {
        return
            keccak256(
                abi.encodePacked(name(), _counter, block.number, _sender)
            );
    }

    function withdraw(address payable _addr) external onlyOwner {
        _addr.transfer(address(this).balance);
    }

    function setEndeTime(uint256 _time) external onlyOwner{
        endTime = _time;
    }
}