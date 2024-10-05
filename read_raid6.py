from sys import path_hooks
from P_Q_syndrome import P_syndrome
from P_Q_syndrome import Q_syndrome
from P_Q_syndrome import P_recovery


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
        while (len(sda := sda_file.read(16)) > 0 and
               len(sdb := sdb_file.read(16)) > 0 and
               len(sdc := sdc_file.read(16)) > 0 and
               len(sdd := sdd_file.read(16)) > 0):

    #TODO move the if blocks into 1 function and modulo the P/Q/1/2 blocks as args

            if count % 4 == 0:
                P_block = sdd
                Q_block = sda
                block1 = sdb
                block2 = sdc

                #recover with P syndrome
                #checking P block has data, if greater than 0 data exists and we recover
                if len(P_block) > 0:
                    P_recovery(P_block, block1, block2)
                else:
                    pass #recover Q syndrome
                    # drives_with_data = [elm for elm in [block1, block2, P_block, Q_block] if len(elm) > 0]
                    # Q_syndrome(drives_with_data[0], drives_with_data[1])

                print((block1 + block2).decode("utf-8"), end="")
            elif count % 4 == 1:
                P_block = sdc
                Q_block = sdd
                block1 = sda
                block2 = sdb

                #recover with P syndrome
                #checking that P block has data if it does recover with XOR
                if len(P_block) > 0:
                    if len(block1) == 0 and len(block2) > 0:
                        block1 = P_syndrome(block2, P_block)
                    elif len(block2) == 0 and len(block1) > 0:
                        block2 = P_syndrome(block1, P_block)
                else: pass
                    # recover Q syndrome

                print((block1 + block2).decode("utf-8"), end="")
            elif count % 4 == 2:
                P_block = sdb
                Q_block = sdc
                block1 = sdd
                block2 = sda

                if len(P_block) > 0:
                    if len(block1) == 0 and len(block2) > 0:
                        block1 = P_syndrome(block2, P_block)
                    elif len(block2) == 0 and len(block1) > 0:
                        block2 = P_syndrome(block1, P_block)
                else:
                    pass  # recover Q syndrome

                print((block1 + block2).decode("utf-8"), end="")
            else:
                P_block = sda
                Q_block = sdb
                block1 = sdc
                block2 = sdd

                if len(P_block) > 0:
                    if len(block1) == 0 and len(block2) > 0:
                        block1 = P_syndrome(block2, P_block)
                    elif len(block2) == 0 and len(block1) > 0:
                        block2 = P_syndrome(block1, P_block)
                else:
                    pass  # recover Q syndrome

                print((block1 + block2).decode("utf-8"), end="")
            count += 1

read_raid6()



