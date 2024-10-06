from sys import path_hooks

from P_Q_syndrome import recover_all


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

    #TODO move the if blocks into 1 function and modulo the P/Q/1/2 blocks as args

            if count % 4 == 0:
                P_block = sdd
                Q_block = sda
                block1 = sdb
                block2 = sdc

                #recover with P syndrome
                #checking for 1 failed drive to P recover
                # if sum(len(elm) > 0 for elm in [block1, block2, P_block, Q_block]) == 3:
                #     block1, block2 = P_recovery(P_block, block1, block2)
                #     print((block1 + block2).decode("utf-8"), end="")
                # #checking for 2 failed drives to Q recover
                # if sum(len(elm) > 0 for elm in [block1, block2, P_block, Q_block]) == 2:
                #     # pass #recover Q syndrome
                #     drives_with_data = [elm for elm in [block1, block2, P_block, Q_block] if len(elm) > 0]
                #     block1 = Q_syndrome(drives_with_data[0], drives_with_data[1])
                block1, block2 = recover_all(block1, block2, P_block, Q_block)
                print((block1 + block2).decode("utf-8"), end="")
            elif count % 4 == 1:
                P_block = sdc
                Q_block = sdd
                block1 = sda
                block2 = sdb

                #recover with P syndrome
                #checking that P block has data if it does recover with XOR
                # if len(P_block) > 0:
                # if sum(len(elm) > 0 for elm in [block1, block2, P_block, Q_block]) == 3:
                #     # if can_use_P(P_block, Q_block, block1, block2):
                #     block1, block2 = P_recovery(P_block, block1, block2)
                #     print((block1 + block2).decode("utf-8"), end="")
                # # elif number_of_drives(P_block, Q_block, block1, block2) == 2:
                # else:
                #     # recover Q syndrome
                #     drives_with_data = [elm for elm in [block1, block2, P_block, Q_block] if len(elm) > 0]
                #     block1= Q_syndrome(drives_with_data[0], drives_with_data[1])
                #     # print(block1.decode("utf-8"), end="")
                block1, block2 = recover_all(block1, block2, P_block, Q_block)
                print((block1 + block2).decode("utf-8"), end="")


                # print((block1 + block2).decode("utf-8"), end="")
            elif count % 4 == 2:
                P_block = sdb
                Q_block = sdc
                block1 = sdd
                block2 = sda
                #
                # if sum(len(elm) > 0 for elm in [block1, block2, P_block, Q_block]) == 3:
                #     block1 = P_recovery(P_block, block1, block2)
                #     print((block1 + block2).decode("utf-8"), end="")
                # else:
                #     # recover Q syndrome
                #     drives_with_data = [elm for elm in [block1, block2, P_block, Q_block] if len(elm) > 0]
                #     block1, block2 = Q_syndrome(drives_with_data[0], drives_with_data[1])
                block1, block2 = recover_all(block1, block2, P_block, Q_block)
                print((block1 + block2).decode("utf-8"), end="")
            else:
                P_block = sda
                Q_block = sdb
                block1 = sdc
                block2 = sdd

                # if sum(len(elm) > 0 for elm in [block1, block2, P_block, Q_block]) == 3:
                #     block1, block2 = P_recovery(P_block, block1, block2)
                # else:
                #     # recover Q syndrome
                #     drives_with_data = [elm for elm in [block1, block2, P_block, Q_block] if len(elm) > 0]
                #     Q_syndrome(drives_with_data[0], drives_with_data[1])
                block1, block2 = recover_all(block1, block2, P_block, Q_block)
                print((block1 + block2).decode("utf-8"), end="")

            count += 1

read_raid6()



