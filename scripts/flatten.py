from brownie import InterstellarMaze, RebornPiecesTestV2_5
import json

def main():
  with open('./flattened/InterstellarMaze.json', 'w') as outfile:
    json.dump(InterstellarMaze.get_verification_info()['standard_json_input'], outfile)
  with open('./flattened/RebornPiecesTestV2_5.json', 'w') as outfile:
    json.dump(RebornPiecesTestV2_5.get_verification_info()['standard_json_input'], outfile)  