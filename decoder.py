#!/usr/bin/python3
import requests


class Sgtin:
    sizes_dict = {
        0: (40, 4),
        1: (37, 7),
        2: (34, 10),
        3: (30, 14),
        4: (27, 17),
        5: (24, 20),
        6: (20, 24),
    }

    def __init__(self, sgtin_in):
        sgtin_bin = self.binarize_sgtin(sgtin_in)

        self.header, sgtin_bin = self.extract_information(sgtin_bin, 8)
        self.filter, sgtin_bin = self.extract_information(sgtin_bin, 3)
        self.partition, sgtin_bin = self.extract_information(sgtin_bin, 3)

        gs1_size, item_size = self.sizes_dict[self.partition]

        self.gs1, sgtin_bin = self.extract_information(sgtin_bin, gs1_size)
        self.item, sgtin_bin = self.extract_information(sgtin_bin, item_size)
        self.serial, sgtin_bin = self.extract_information(sgtin_bin, 38)

    def binarize_sgtin(self, sgtin):
        sgtin_bin = ''
        for c in sgtin:
            c_bin = bin(int(c, 16))[2:].zfill(4)
            sgtin_bin += c_bin
        return sgtin_bin

    def extract_information(self, sgtin_bin, length):
        my_bin = sgtin_bin[:length]
        sgtin_bin = sgtin_bin[length:]
        return int(my_bin, 2), sgtin_bin

    def __repr__(self):
        return "SGTIN:\n\
            \tHeader: {}\n\
            \tFilter: {}\n\
            \tPartition: {}\n\
            \tGS1 Company: {}\n\
            \tItem: {}\n\
            \tSerial: {}".format(self.header,
                                 self.filter,
                                 self.partition,
                                 self.gs1,
                                 self.item,
                                 self.serial)


username = "secret"
password = "tU3kk!?xxx"

sgtin = str(input())

my_sgtin = Sgtin(sgtin)
url = "http://jobfair.tagitsolutions.com/q934dr4/{}/{}".format(my_sgtin.gs1, my_sgtin.item)

resp = requests.get(url, auth=(username, password))
data = resp.json()

print("Item name: {}".format(data['itemName']))
print("Item reference: {}".format(data['itemReference']))
print("Item serial: {}".format(my_sgtin.serial))
print("Item manufacturer: {}".format(data['company']['companyName']))
print("Manufacturer prefix: {}".format(data['company']['companyPrefix']))