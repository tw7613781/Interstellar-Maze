from brownie import NFTFactory
import json

def main():
  with open('./flattened/NFTFactory.json', 'w') as outfile:
    json.dump(NFTFactory.get_verification_info()['standard_json_input'], outfile) 