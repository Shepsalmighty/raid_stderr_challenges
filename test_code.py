if count % 4 == 0:
    P_block = sdd
    Q_block = sda
    block1 = sdb
    block2 = sdc

    # recover with P syndrome
    # checking P block has data, if greater than 0 data exists and we recover
    if len(P_block) > 0:
        if len(block1) == 0 and len(block2) > 0:
            block1 = P_syndrome(block2, P_block)
        elif len(block2) == 0 and len(block1) > 0:
            block2 = P_syndrome(block1, P_block)
    else:
        # recover Q syndrome
        drives_with_data = [elm for elm in [block1, block2, P_block, Q_block] if len(elm) > 0]
        if sum(len(elm) == 0 for elm in [block1, block2, P_block, Q_block]) <= 2:

            [len(elm) == 0 for elm in [block1, block2, P_block, Q_block] if len(elm) > 0]
            # [elm for elm in [block1, block2, P_block, Q_block] if len(elm) > 0]

            # for thing in [block1, block2, P_block, Q_block]:
            #     drives = []
            #     if thing == 0:
            #         drives.append(thing)
            #     return drives




