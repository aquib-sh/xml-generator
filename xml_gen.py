import os
import pandas
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter.constants import W
from lxml import etree

class App:
    def __init__(self):        
        # Global variables for keys in xml and it's extension
        self.__ROOT_TAG = "properties"
        self.__FILENAME_KEY = "archivo"
        self.__FILEPATH_KEY = "ruta"
        self.__EXTENSION = ".metadata.properties.xml"
        self.__RESERVED_KEYS = [self.__ROOT_TAG, 
                                self.__FILENAME_KEY, 
                                self.__FILEPATH_KEY, 
                                self.__EXTENSION]
        # Get the file from user
        root = tk.Tk()
        root.withdraw() 
        input_file = filedialog.askopenfilename(title = "Select Base file",
            filetypes = (
                ("csv file","*.csv"), 
                ("xlsx file", "*.xlsx"),
                ("all files","*.*")
            )
        )
        self.input_df = self.__read_data(input_file)

    def __read_data(self, filename:str) -> pandas.DataFrame:
        if filename.endswith(".csv"):
            input_df = pandas.read_csv(filename)
        elif filename.endswith(".xlsx"):
            input_df = pandas.read_excel(filename)
        else:
            raise Exception("Unsupported file type")
        return input_df

    def row_to_dict(self, row) -> dict:
        """Converts a dataframe row to dictionary"""
        _dict = {}
        for elem in row.keys():
            _dict[elem] = row[elem]
        return _dict

    def __add_entry(self, root_element, _key, inner_text):
        elem = etree.SubElement(root_element, "entry")
        elem.set("key", _key)
        elem.text = inner_text
        elem.tail = "\n"
        return elem

    def generate_xml(self, row_dict):
        root = etree.Element(self.__ROOT_TAG)
        root.text = "\t\n"

        OUT = os.path.join(row_dict[self.__FILEPATH_KEY], row_dict[self.__FILENAME_KEY])
        OUT += self.__EXTENSION

        for elem in row_dict:
            if elem not in self.__RESERVED_KEYS:
                entry = self.__add_entry(root, elem, str(row_dict[elem]))
                root.append(entry)
                
        tree = etree.ElementTree(root)
        tree.write(OUT)
        print(f"[+] Written to {OUT}")

    def run(self):
        length = len(self.input_df[self.__FILENAME_KEY])
        for i in range(0, length):
            row = self.row_to_dict(self.input_df.loc[i])
            self.generate_xml(row)

    def print_df(self):
        print(self.input_df.keys())


if __name__ == "__main__":
    app = App()
    app.run()
    

