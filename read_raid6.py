#!/usr/bin/env python
from sys import path_hooks

from P_Q_syndrome import recover_all_pt1


def read_raid6():
    paths = ["/home/sheps/PycharmProjects/stderr_challenges/RAID6/part_1/sda",
             "/home/sheps/PycharmProjects/stderr_challenges/RAID6/part_1/sdb",
             "/home/sheps/PycharmProjects/stderr_challenges/RAID6/part_1/sdc",
             "/home/sheps/PycharmProjects/stderr_challenges/RAID6/part_1/sdd"]
    with (open(paths[0], "rb") as sda_file,
          open(paths[1], "rb") as sdb_file,
          open(paths[2], "rb") as sdc_file,
          open(paths[3], "rb") as sdd_file):

        count = 0
        while (len(sda := sda_file.read(16)) +
               len(sdb := sdb_file.read(16)) +
               len(sdc := sdc_file.read(16)) +
               len(sdd := sdd_file.read(16)) != 0):


            # to read the file bytes in the correct order we do (count % 4) such that block1 and block2 always contain
            # the correct bytes in their reading order
            if count % 4 == 0:
                P_block = sdd
                Q_block = sda
                block1 = sdb
                block2 = sdc

            elif count % 4 == 1:
                P_block = sdc
                Q_block = sdd
                block1 = sda
                block2 = sdb

            elif count % 4 == 2:
                P_block = sdb
                Q_block = sdc
                block1 = sdd
                block2 = sda

            else:
                P_block = sda
                Q_block = sdb
                block1 = sdc
                block2 = sdd

            block1, block2 = recover_all_pt1(block1, block2, P_block, Q_block)
            print((block1 + block2).decode("utf-8"), end="")
            count += 1


read_raid6()



