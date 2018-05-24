#!/usr/bin/python3
import requests


url = "http://jobfair.tagitsolutions.com/q934dr4/hello-world/?ping=pong"
username = "secret"
password = "tU3kk!?xxx"

sgtin = "300E5E1B8C71C14001B458D1"


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

        self.header_bin = self.pop_from_left(sgtin_bin, 8)
        self.filter_bin = self.pop_from_left(sgtin_bin, 3)
        self.partition_bin = self.pop_from_left(sgtin_bin, 3)

        gs1_size, item_size = self.sizes_dict[int(self.partition_bin, 2)]

        self.gs1_bin = self.pop_from_left(sgtin_bin, gs1_size)
        self.item_bin = self.pop_from_left(sgtin_bin, item_size)
        self.serial_bin = self.pop_from_left(sgtin_bin, 38)

    def binarize_sgtin(self, sgtin):
        sgtin_bin = ''
        for c in sgtin:
            c_bin = bin(int(c, 16))[2:].zfill(4)
            sgtin_bin += c_bin
        return sgtin_bin

    def pop_from_left(self, sgtin_bin, length):
        my_bin = sgtin_bin[:length]
        sgtin_bin = sgtin_bin[length:]
        return my_bin

    def __repr__(self):
        return "SGTIN:\n\
            \tHeader: {}\n\
            \tFilter: {}\n\
            \tPartition: {}\n\
            \tGS1 Company: {}\n\
            \tItem: {}\n\
            \tSerial: {}".format(int(self.header_bin, 2),
                                 int(self.filter_bin, 2),
                                 int(self.partition_bin, 2),
                                 int(self.gs1_bin, 2),
                                 int(self.item_bin, 2),
                                 int(self.serial_bin, 2))


my_sgtin = Sgtin(sgtin)
print(my_sgtin)
# requests.get(url, auth=(username, password))
