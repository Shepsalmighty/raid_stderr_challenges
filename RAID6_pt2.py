#!/usr/bin/env python
from sys import path_hooks

from P_Q_syndrome import recover_all_pt2


def read_raid6():

    """~/PycharmProjects/XOR_raid6/part_2/sectors"""
    paths = ["~/PycharmProjects/XOR_raid6/part_2/sectors/sda",
             "~/PycharmProjects/XOR_raid6/part_2/sectors/sdb",
             "~/PycharmProjects/XOR_raid6/part_2/sectors/sdc",
             "~/PycharmProjects/XOR_raid6/part_2/sectors/sdd",
             "~/PycharmProjects/XOR_raid6/part_2/sectors/sde",
             "~/PycharmProjects/XOR_raid6/part_2/sectors/sdf",
             "~/PycharmProjects/XOR_raid6/part_2/sectors/sdg",
             "~/PycharmProjects/XOR_raid6/part_2/sectors/sdh"]

    with (open(paths[0], "rb") as sda_file,
          open(paths[1], "rb") as sdb_file,
          open(paths[2], "rb") as sdc_file,
          open(paths[3], "rb") as sdd_file,
          open(paths[4], "rb") as sde_file,
          open(paths[5], "rb") as sdf_file,
          open(paths[6], "rb") as sdg_file,
          open(paths[7], "rb") as sdh_file,):

        blocksize = 512
        count = 0

        while (len(sda := sda_file.read(blocksize)) +
               len(sdb := sdb_file.read(blocksize)) +
               len(sdc := sdc_file.read(blocksize)) +
               len(sdd := sdd_file.read(blocksize)) +
               len(sde := sde_file.read(blocksize)) +
               len(sdf := sdf_file.read(blocksize)) +
               len(sdg := sdg_file.read(blocksize)) +
               len(sdh := sdh_file.read(blocksize)) != 0):

            #TODO: use arrays to shorten redundant code in the if/elif block
            # files = [sda, sdb, sdc, sdd, sde, sdf, sdg, sdh]
            # blocks = [None, None, None, None, None, None, None]
            # to read the file bytes in the correct order we do (count % 8) such that the P and Q syndrome are known

            # for P in range(8):
            #     if P % count ==
            if count % 8 == 0:
                P_block = sdh
                Q_block = sda
                block1 = sdb
                block2 = sdc
                block3 = sdd
                block4 = sde
                block5 = sdf
                block6 = sdg

            elif count % 8 == 1:
                P_block = sdg
                Q_block = sdh
                block1 = sda
                block2 = sdb
                block3 = sdc
                block4 = sdd
                block5 = sde
                block6 = sdf

            elif count % 8 == 2:
                P_block = sdf
                Q_block = sdg
                block1 = sdh
                block2 = sda
                block3 = sdb
                block4 = sdc
                block5 = sdd
                block6 = sde

            elif count % 8 == 3:
                P_block = sde
                Q_block = sdf
                block1 = sdg
                block2 = sdh
                block3 = sda
                block4 = sdb
                block5 = sdc
                block6 = sdd

            elif count % 8 == 4:
                P_block = sdd
                Q_block = sde
                block1 = sdf
                block2 = sdg
                block3 = sdh
                block4 = sda
                block5 = sdb
                block6 = sdc

            elif count % 8 == 5:
                P_block = sdc
                Q_block = sdd
                block1 = sde
                block2 = sdf
                block3 = sdg
                block4 = sdh
                block5 = sda
                block6 = sdb

            elif count % 8 == 6:
                P_block = sdb
                Q_block = sdc
                block1 = sdd
                block2 = sde
                block3 = sdf
                block4 = sdg
                block5 = sdh
                block6 = sda

            elif count % 8 == 7:
                P_block = sda
                Q_block = sdb
                block1 = sdc
                block2 = sdd
                block3 = sde
                block4 = sdf
                block5 = sdg
                block6 = sdh

            block1, block2, block3, block4, block5, block6 = recover_all_pt2(
                block1, block2, block3, block4, block5, block6, P_block, Q_block)
            # print((block1 + block2).decode("utf-8"), end="")
            count += 1


read_raid6()



