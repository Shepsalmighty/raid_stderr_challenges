#!/usr/bin/env python
from sys import path_hooks

from P_Q_syndrome import recover_all_pt2
from P_Q_syndrome import number_missing_drives

def read_file(file_name):
    try:
        with open(file_name, "rb") as file:
            content = file.read()
            return content
    except FileNotFoundError as e:
        return []


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
            #TODO: probably read_file(Path(paths[0])) etc
            sd = []
            for num in range(8):
                sd.append(read_file(paths[num]))

            # ordered_blocks = sd[count % 8:] + sd[:count % 8]

                #TODO: use arrays to shorten redundant code in the if/elif block
                # files = [sda, sdb, sdc, sdd, sde, sdf, sdg, sdh]
                # blocks = [None, None, None, None, None, None, None]
                # to read the file bytes in the correct order we do (count % 8) such that the P and Q syndrome are known

            P_index = 7 - (count%8)
            Q_index = (P_index + 1) % 8
            data1_index = (Q_index + 1) % 8
            block = []
            for d in range(6):
                block.append(sd[(data1_index + d) % 8])
            P_block = sd[P_index]
            Q_block = sd[Q_index]


            # P_block, Q_block, block1, block2, block3, block4, block5, block6 = ordered_blocks

            # if number_missing_drives(block1, block2, block3, block4, block5, block6) >= 2:
            #     return count
            if number_missing_drives(block) > 2:
                return count

            block = recover_all_pt2(block, P_block, Q_block)

            # block1, block2, block3, block4, block5, block6 = recover_all_pt2(
            #     block1, block2, block3, block4, block5, block6, P_block, Q_block)

            # file.write(block1 + block2 + block3 + block4 + block5 + block6)
            for b in block:
                file.write(b)

                # print((block1 + block2).decode("utf-8"), end="")

            count += 1



read_raid6()



