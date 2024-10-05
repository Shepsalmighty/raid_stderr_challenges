def P_syndrome(block1, block2):
    recovered_data = []
    for a, b in zip(block1, block2):
        recovered_data.append(int(a) ^ int(b))

    return bytes(recovered_data)


# def P_recovery(block1, block2, P_block):
#     assert len(P_block) > 0, "P_block empty"
#     if len(block1) == 0 and len(block2) > 0:
#         block1 = P_syndrome(block2, P_block)
#
#     elif len(block2) == 0 and len(block1) > 0:
#         block2 = P_syndrome(block1, P_block)
#
#     return block1, block2

def P_recovery(block1, block2, P_block):
    assert len(P_block) > 0, "P_block empty"
    recovered_data = []
    if len(block1) == 0 and len(block2) > 0:
        # block1 = P_syndrome(block2, P_block)
        for a, b in zip(P_block, block2):
            recovered_data.append(int(a) ^ int(b))

    elif len(block2) == 0 and len(block1) > 0:
        # block2 = P_syndrome(block1, P_block)
        for a, b in zip(block1, P_block):
            recovered_data.append(int(a) ^ int(b))

    return bytes(recovered_data)

def Q_syndrome(block1, block2):
    recovered_data = []
    for a, b in zip(block1, block2):
        a = 2 ** 0 * a
        b = 2 ** 1 * b
        # hex 285 == 0x11D but 285 is easier for me to read
        if a > 255:
            a = a ^ 285
        if b > 255:
            b = b ^ 285
        recovered_data.append((int(a) ^ int(b)))
    return bytes(recovered_data)

# def read_while_data():
#     paths = ["/home/sheps/PycharmProjects/stderr_challenges/RAID6/part_1/sda",
#              "/home/sheps/PycharmProjects/stderr_challenges/RAID6/part_1/sdb",
#              "/home/sheps/PycharmProjects/stderr_challenges/RAID6/part_1/sdc",
#              "/home/sheps/PycharmProjects/stderr_challenges/RAID6/part_1/sdd"]
#     with open(paths[0], "rb") as sda_file, open(paths[1], "rb") as sdb_file, open(paths[2], "rb") as sdc_file, open(paths[3], "wb") as answer:
#
#         count = 0
#         while (len(sda := sda_file.read(1)) > 0 and len(sdb := sdb_file.read(1)) > 0 and len(sdc := sdc_file.read(1)) > 0):
#     #     while ((sda := sda_file.read(1)) and (sdb := sdb_file.read(1)) and (sdc := sdc_file.read(1)):
#
#             if count % 3 == 0:
#                 answer.write(sda + sdb)
#             elif count % 3 == 1:
#                 answer.write(sdb + sdc)
#             else:
#                 answer.write(sdc + sda)
#             count += 1
