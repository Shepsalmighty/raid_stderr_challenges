def P_syndrome(block1, block2):
    recovered_data = []
    for a, b in zip(block1, block2):
        recovered_data.append(int(a) ^ int(b))

    return bytes(recovered_data)


def P_recovery(block1, block2, P_block):
    # assert len(P_block) > 0, "P_block empty"
    if len(block1) == 0 and len(block2) > 0:
        block1 = P_syndrome(block2, P_block)

    elif len(block2) == 0 and len(block1) > 0:
        block2 = P_syndrome(block1, P_block)

    return block1, block2


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


def recover_all(block1, block2, P_block, Q_block):
    #returns block1 and block2 if both have data
    if len(block1) > 0 and len(block2) > 0:
        return block1, block2

    # recovers data from 1 lost drive using P syndrome (XOR)
    #case 1, block1 empty but block2 and P_block have data
    if len(block1) == 0 and len(block2) > 0 and len(P_block) > 0:
        recovered_data = []
        for a, b in zip(P_block, block2):
            recovered_data.append(int(a) ^ int(b))
        block1 = bytes(recovered_data)
        return block1, block2
    #case 2, block2 empty but block1 and P_block have data
    if len(block1) > 0 and len(block2) == 0 and len(P_block) > 0:
        recovered_data = []
        for a, b in zip(P_block, block1):
            recovered_data.append(int(a) ^ int(b))
        block2 = bytes(recovered_data)
        return block1, block2

    #Q_recovery if missing 1 data block and the P block
    #1st case block1 and P_block missing
    if len(block1) == 0 and len(P_block) == 0:
        recovered_data = []
        for a, b in zip(Q_block, block2):
            recovered_data.append(int(a) ^ (2* int(b)))
        return bytes(recovered_data), block2
    #2nd case block2 and P_block missing
    if len(block2) == 0 and len(P_block) == 0:
        recovered_data = []
        for a, b in zip(Q_block, block1):
            recovered_data.append((int(a) ^ int(b)) //2)
        return block1, bytes(recovered_data)

    #if missing both data blocks, we must Q recover D2 (block2) first, and then we can P recover D1 (block1)
    #see also Reed Solomon algorithm https://anadoxin.org/blog/error-recovery-in-raid6.html/
    if len(block1) == 0 and len(block2) == 0:
        recovered_block2 = bytearray()
        recovered_block1 = bytearray()
        for a, b in zip(P_block, Q_block):
            for n in range(0, 256):
                n_xor_2n = Q_syndrome(bytes((n,)), bytes((n,)))
                if n_xor_2n[0] == a ^ b:
                    recovered_block2.append(n)
                    recovered_block1.append(a ^ n)
                    break
            else:
                print("PANIC!!!!")
        return recovered_block1, recovered_block2