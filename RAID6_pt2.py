#!/usr/bin/env python
from sys import path_hooks

from P_Q_syndrome import recover_all_pt2
from P_Q_syndrome import number_missing_drives

def read_file(file_name):
    if not file_name:
        return []

    with open(file_name, "rb") as file:
        content = file.read()
        return content


def read_raid6():

    recovered_data = "/home/sheps/PycharmProjects/XOR_raid6/part_2/recovered_data"
    with open(recovered_data, "wb") as file:

        count = 0
        #INFO: while loop may need to be changed to "while try" for part 3
        while count < 839:
            """/home/sheps/PycharmProjects/XOR_raid6/part_2/sectors"""
            paths = [f"/home/sheps/PycharmProjects/XOR_raid6/part_2/sectors/sda.sector{count:03d}",
                     f"/home/sheps/PycharmProjects/XOR_raid6/part_2/sectors/sdb.sector{count:03d}",
                     f"/home/sheps/PycharmProjects/XOR_raid6/part_2/sectors/sdc.sector{count:03d}",
                     f"/home/sheps/PycharmProjects/XOR_raid6/part_2/sectors/sdd.sector{count:03d}",
                     f"/home/sheps/PycharmProjects/XOR_raid6/part_2/sectors/sde.sector{count:03d}",
                     f"/home/sheps/PycharmProjects/XOR_raid6/part_2/sectors/sdf.sector{count:03d}",
                     f"/home/sheps/PycharmProjects/XOR_raid6/part_2/sectors/sdg.sector{count:03d}",
                     f"/home/sheps/PycharmProjects/XOR_raid6/part_2/sectors/sdh.sector{count:03d}"]


            # with (open(paths[0], "rb") as sda_file,
            #       open(paths[1], "rb") as sdb_file,
            #       open(paths[2], "rb") as sdc_file,
            #       open(paths[3], "rb") as sdd_file,
            #       open(paths[4], "rb") as sde_file,
            #       open(paths[5], "rb") as sdf_file,
            #       open(paths[6], "rb") as sdg_file,
            #       open(paths[7], "rb") as sdh_file,):

            # blocksize = 512

            sda = read_file(paths[0])
            sdb = read_file(paths[1])
            sdc = read_file(paths[2])
            sdd = read_file(paths[3])
            sde = read_file(paths[4])
            sdf = read_file(paths[5])
            sdg = read_file(paths[6])
            sdh = read_file(paths[7])

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

            if count % 8 == 1:
                P_block = sdg
                Q_block = sdh
                block1 = sda
                block2 = sdb
                block3 = sdc
                block4 = sdd
                block5 = sde
                block6 = sdf

            if count % 8 == 2:
                P_block = sdf
                Q_block = sdg
                block1 = sdh
                block2 = sda
                block3 = sdb
                block4 = sdc
                block5 = sdd
                block6 = sde

            if count % 8 == 3:
                P_block = sde
                Q_block = sdf
                block1 = sdg
                block2 = sdh
                block3 = sda
                block4 = sdb
                block5 = sdc
                block6 = sdd

            if count % 8 == 4:
                P_block = sdd
                Q_block = sde
                block1 = sdf
                block2 = sdg
                block3 = sdh
                block4 = sda
                block5 = sdb
                block6 = sdc

            if count % 8 == 5:
                P_block = sdc
                Q_block = sdd
                block1 = sde
                block2 = sdf
                block3 = sdg
                block4 = sdh
                block5 = sda
                block6 = sdb

            if count % 8 == 6:
                P_block = sdb
                Q_block = sdc
                block1 = sdd
                block2 = sde
                block3 = sdf
                block4 = sdg
                block5 = sdh
                block6 = sda

            if count % 8 == 7:
                P_block = sda
                Q_block = sdb
                block1 = sdc
                block2 = sdd
                block3 = sde
                block4 = sdf
                block5 = sdg
                block6 = sdh

            if number_missing_drives(block1, block2, block3, block4, block5, block6) >= 2:
                return count

            block1, block2, block3, block4, block5, block6 = recover_all_pt2(
                block1, block2, block3, block4, block5, block6, P_block, Q_block)

            file.write(block1 + block2 + block3 + block4 + block5 + block6)

                # print((block1 + block2).decode("utf-8"), end="")

            count += 1



read_raid6()



