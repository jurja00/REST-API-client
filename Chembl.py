import requests
import xml.etree.ElementTree as ET

class Chembl(object):

    def __init__(self, path, delimiter = ";"):
        self.data = self.openFile(path, delimiter)
        self.url = "https://www.ebi.ac.uk/chembl/api/data"



    def openFile(self, filename, delimiter):
        with open(filename) as file:
           data = file.readlines();
           
        data = [x.strip() for x in data];
        result = [];

        for i in range(len(data)):
            if i == 0:
                continue

            result.append(data[i].split(delimiter));
       
        return result;


    def find_data(self, id_col, search_data = None):
        uri = "/molecule/"

        for row in self.data:
            id  = row[id_col]

            if id == "":
                continue

            result = requests.get(self.url + uri + id)

            if not result:
                continue

            root = ET.fromstring(result.content)

            print(root.tag)
