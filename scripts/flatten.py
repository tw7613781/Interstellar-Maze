from brownie import InterstellarMaze
import json

def main():
  with open('./flattened/InterstellarMaze.json', 'w') as outfile:
    json.dump(InterstellarMaze.get_verification_info()['standard_json_input'], outfile) 