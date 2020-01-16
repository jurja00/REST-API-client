import requests
import Chembl as ch
import Pubchem
import constants as CONST


def main():

    pubchem = Pubchem.Pubchem("Bereau_01.csv")

    pubchem.find_data(0, CONST.PUBCHEM["URI"]["SMILES"])


main()