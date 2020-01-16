import requests
import xml.etree.ElementTree as ET
import json
import constants as const
import csv
import urllib.parse



class Pubchem(object):

    def __init__(self, path, delimiter = ";"):
        self.header = []
        self.data = self.openFile(path, delimiter)
        self.rowCount = len(self.data)
        self.url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"
        self.session = requests.Session()



    def openFile(self, filename, delimiter):
        with open(filename) as file:
           data = file.readlines()
           
        data = [x.strip() for x in data];
        result = []

        for i in range(len(data)):
            if i == 0:
                head =  data[0].split(delimiter)
                for x in head:
                    self.header.append(x)
                continue

            result.append(data[i].split(delimiter));
       
        return result;



    def find_data(self, id_col, uri = const.PUBCHEM["URI"]["INCHI"]):
        uri_suffix = "/property/" + const.PUBCHEM["PROPERTIES"] + "/JSON"
        uri = uri + "/"

        self.header.append("Pubchem ID")
        self.header.append("Name")
        self.header.append("LogP")
        self.header.append("MW")
        self.header.append("Formula")


        for i, row in enumerate(self.data):
            id  = row[id_col]
            encoded_id = urllib.parse.quote(id)
            name  = row[1]
            length = len(row)

            print("---- ROW: ", i+1, "/", self.rowCount, " ----")

            if id == "":
                continue

            URL = self.url + uri + encoded_id + uri_suffix

            #print(URL);

            result = requests.get(URL)

            #print(result.content)

            if not result:
                continue

            data = json.loads(result.content);

            data = data["PropertyTable"]["Properties"][0]

            if data["CID"] == 0:
                continue;

            new_name = data["IUPACName"] if data["IUPACName"] else ""
            logP = data["XLogP"] if data["XLogP"] else ""
            MW = data["MolecularWeight"] if data["MolecularWeight"] else ""
            formula = data["MolecularFormula"] if data["MolecularFormula"] else ""
            pubchem_id = data["CID"] if data["CID"] else ""

            row.append(pubchem_id)
            row.append(new_name)
            row.append(logP)
            row.append(MW)
            row.append(formula)

            print("ID: ", id,  "--Name: ", new_name, "--LogP: ", logP, "--MW: ", MW,"--Formula: ", formula, "--pubchem_id: ", pubchem_id)
            print("")

        with open("modified.csv", "w") as output:
            writer = csv.writer(output, delimiter =";",quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.header)
            writer.writerows(self.data)

        output.close()

