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
        if a > 0xFF:
            a = a ^ 0x11D
        if b > 0xFF:
            b = b ^ 0x11D
        recovered_data.append((int(a) ^ int(b)))
    return bytes(recovered_data)


def multiply(var, byte):
    #INFO: hex 255 == 0xFF and hex 285 == 0x11D
    if var == 1:
        return byte
    if var == 2:
        result = byte * 2
        if result > 0xFF:
           result = result ^ 0x11D
        return result
    if var == 3:
        result = byte * 2
        if result > 0xFF:
            result = result ^ 0x11D
        return result ^ byte
    if var == 4:
        result = byte * 2
        if result > 0xFF:
            result = result ^ 0x11D
        result = result * 2
        if result > 0xFF:
           result = result ^ 0x11D
        return result
    if var == 5:
        result = byte * 2
        if result > 0xFF:
            result = result ^ 0x11D
        result = result * 2
        if result > 0xFF:
           result = result ^ 0x11D
        result = result ^ byte
        return result
    if var == 6:
        result = byte * 2
        if result > 0xFF:
            result = result ^ 0x11D
        result = result ^ byte
        result = result * 2
        if result > 0xFF:
            result = result ^ 0x11D
        return result

def divide(var1, var2):
    #drive 1 divides by 1, redundant but keeping it for consistency
    for n in range(256):
        if multiply(var2, n) == var1:
            return n


def P_syndrome_pt2(block):
    recovered_data = []
    for a, b, c, d, e, f in zip(block[0], block[1], block[2], block[3], block[4], block[5]):
        recovered_data.append((int(a) ^ int(b) ^ int(c) ^ int(d) ^ int(e) ^ int(f)))
    return bytes(recovered_data)


def Q_syndrome_pt2(block):
    recovered_data = []
    for a, b, c, d, e, f in zip(block[0], block[1], block[2], block[3], block[4], block[5]):
        a = multiply(1, a)
        b = multiply(2, b)
        c = multiply(3, c)
        d = multiply(4, d)
        e = multiply(5, e)
        f = multiply(6, f)


        recovered_data.append((int(a) ^ int(b) ^ int(c) ^ int(d) ^ int(e) ^ int(f)))
    return bytes(recovered_data)


def recover_all_pt1(block1, block2, P_block, Q_block):
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




def recover_all_pt2(block, P_block, Q_block):

    missing_data = []  # list of indexes in block where data is missing
    for d in range(len(block)):
        if len(block[d]) == 0:
            missing_data.append(d)

    #returns all blocks if they have data
    if len(block[0]) > 0 and\
            len(block[1]) > 0 and\
            len(block[2]) > 0 and\
            len(block[3]) > 0 and\
            len(block[4]) > 0 and\
            len(block[5]) > 0:
        return block[0], block[1], block[2], block[3], block[4], block[5]

    # recovers data from 1 lost drive using P syndrome (XOR)
    #case 1, block[0 empty but remaining blocks and P_block have data
    if len(P_block) > 0:
        if len(block[0]) == 0 and\
            len(block[1]) > 0 and\
            len(block[2]) > 0 and\
            len(block[3]) > 0 and\
            len(block[4]) > 0 and\
            len(block[5]) > 0:
            recovered_data = []
            for a, b, c, d, e, f in zip(P_block, block[1], block[2], block[3], block[4], block[5]):
                recovered_data.append(int(a) ^ int(b) ^ int(c) ^ int(d) ^ int(e) ^ int(f))
            block[0] = bytes(recovered_data)
            return block[0], block[1], block[2], block[3], block[4], block[5]

        # case 2, block[1 empty but remaining blocks and P_block have data
        elif len(block[1]) == 0 and\
            len(block[0]) > 0 and\
            len(block[2]) > 0 and\
            len(block[3]) > 0 and\
            len(block[4]) > 0 and\
            len(block[5]) > 0:
            recovered_data = []
            for a, b, c, d, e, f in zip(P_block, block[0], block[2], block[3], block[4], block[5]):
                recovered_data.append(int(a) ^ int(b) ^ int(c) ^ int(d) ^ int(e) ^ int(f))
            block[1] = bytes(recovered_data)
            return block[0], block[1], block[2], block[3], block[4], block[5]

            # case 3, block[2 empty but remaining blocks and P_block have data
        elif len(block[2]) == 0 and \
             len(block[0]) > 0 and \
             len(block[1]) > 0 and \
             len(block[3]) > 0 and \
             len(block[4]) > 0 and \
             len(block[5]) > 0:
            recovered_data = []
            for a, b, c, d, e, f in zip(P_block, block[0], block[1], block[3], block[4], block[5]):
                recovered_data.append(int(a) ^ int(b) ^ int(c) ^ int(d) ^ int(e) ^ int(f))
            block[2] = bytes(recovered_data)
            return block[0], block[1], block[2], block[3], block[4], block[5]

            # case 4, block[3 empty but remaining blocks and P_block have data
        elif len(block[3]) == 0 and \
                len(block[0]) > 0 and \
                len(block[1]) > 0 and \
                len(block[2]) > 0 and \
                len(block[4]) > 0 and \
                len(block[5]) > 0:
            recovered_data = []
            for a, b, c, d, e, f in zip(P_block, block[0], block[1], block[2], block[4], block[5]):
                recovered_data.append(int(a) ^ int(b) ^ int(c) ^ int(d) ^ int(e) ^ int(f))
            block[3] = bytes(recovered_data)
            return block[0], block[1], block[2], block[3], block[4], block[5]

            # case 5, block[4 empty but remaining blocks and P_block have data
        elif len(block[4]) == 0 and \
             len(block[0]) > 0 and \
             len(block[1]) > 0 and \
             len(block[2]) > 0 and \
             len(block[3]) > 0 and \
             len(block[5]) > 0:
            recovered_data = []
            for a, b, c, d, e, f in zip(P_block, block[0], block[1], block[2], block[3], block[5]):
                recovered_data.append(int(a) ^ int(b) ^ int(c) ^ int(d) ^ int(e) ^ int(f))
            block[4] = bytes(recovered_data)
            return block[0], block[1], block[2], block[3], block[4], block[5]

            # case 6, block[5 empty but remaining blocks and P_block have data
        elif len(block[5]) == 0 and \
                len(block[0]) > 0 and \
                len(block[1]) > 0 and \
                len(block[2]) > 0 and \
                len(block[3]) > 0 and \
                len(block[4]) > 0:
            recovered_data = []
            for a, b, c, d, e, f in zip(P_block, block[0], block[1], block[2], block[3], block[4]):
                recovered_data.append(int(a) ^ int(b) ^ int(c) ^ int(d) ^ int(e) ^ int(f))
            block[5] = bytes(recovered_data)
            return block[0], block[1], block[2], block[3], block[4], block[5]


    #Q_recovery if missing 1 data block and the P block
    #1st case block[0 and P_block missing
    if len(block[0]) == 0 and len(P_block) == 0:
        block[0] = [0 for _ in range(len(Q_block))]
        not_really_Q = Q_syndrome_pt2(block)
        recovered_data = []
        for a, b in zip(not_really_Q, Q_block):
            recovered_data.append(divide((a ^ b), 1))
        return bytes(recovered_data), block[1], block[2], block[3], block[4], block[5]
        # recovered_data = []
        # for a, b, c, d, e, f in zip(P_block, block[0, block[1, block[2, block[3, block[4):
        #     recovered_data.append(int(a) ^ (2* int(b) ^(3*int(c)) ^(4*int(d)) ^(5*int(e)) ^(6*(int(f)))))
        # for a, b, c, d, e, f in zip(Q_block, block[1, block[2, block[3, block[4, block[5):

        # return bytes(recovered_data), block[1, block[2, block[3, block[4, block[5
    #2nd case block[1 and P_block missing
    if len(block[1]) == 0 and len(P_block) == 0:
        block[1] = [0 for _ in range(len(Q_block))]
        not_really_Q = Q_syndrome_pt2(block)
        recovered_data = []
        for a, b in zip(not_really_Q, Q_block):
            recovered_data.append(divide((a ^ b), 2))
        return block[0], bytes(recovered_data), block[2], block[3], block[4], block[5]

    # 3rd case block[2 and P_block missing
    if len(block[2]) == 0 and len(P_block) == 0:
        block[2] = [0 for _ in range(len(Q_block))]
        not_really_Q = Q_syndrome_pt2(block)
        recovered_data = []
        for a, b in zip(not_really_Q, Q_block):
            recovered_data.append(divide((a ^ b), 3))
        return block[0], block[1], bytes(recovered_data), block[3], block[4], block[5]

    # 4th case block[3 and P_block missing
    if len(block[3]) == 0 and len(P_block) == 0:
        block[3] = [0 for _ in range(len(Q_block))]
        not_really_Q = Q_syndrome_pt2(block)
        recovered_data = []
        for a, b in zip(not_really_Q, Q_block):
            recovered_data.append(divide((a ^ b), 4))
        return block[0], block[1], block[2], bytes(recovered_data), block[4], block[5]

    # 5th case block[4 and P_block missing
    if len(block[4]) == 0 and len(P_block) == 0:
        block[4] = [0 for _ in range(len(Q_block))]
        not_really_Q = Q_syndrome_pt2(block)
        recovered_data = []
        for a, b in zip(not_really_Q, Q_block):
            recovered_data.append(divide((a ^ b), 5))
        return block[0], block[1], block[2], block[3], bytes(recovered_data), block[5]

    # 6th case block[5 and P_block missing
    if len(block[5]) == 0 and len(P_block) == 0:
        block[5] = [0 for _ in range(len(Q_block))]
        not_really_Q = Q_syndrome_pt2(block)
        recovered_data = []
        for a, b in zip(not_really_Q, Q_block):
            recovered_data.append(divide((a ^ b), 6))
        return block[0], block[1], block[2], block[3], block[4] , bytes(recovered_data)

    # for a,b,c,d,e,f in zip(block1, block2, block[2, block4, block5, block[5):

    #TODO: make this function not fucking suck



    #if missing both data blocks, we must Q recover D2 (block2) first, and then we can P recover D1 (block1)
    #see also Reed Solomon algorithm https://anadoxin.org/blog/error-recovery-in-raid6.html/
    # if len(block1) == 0 and len(block2) == 0:
    #     recovered_block2 = bytearray()
    #     recovered_block1 = bytearray()
    #     for a, b in zip(P_block, Q_block):
    #         for n in range(0, 256):
    #             n_xor_2n = Q_syndrome(bytes((n,)), bytes((n,)))
    #             if n_xor_2n[0] == a ^ b:
    #                 recovered_block2.append(n)
    #                 recovered_block1.append(a ^ n)
    #                 break
    #         else:
    #             print("PANIC!!!!")
    #     return recovered_block1, recovered_block2

    #TODO: delete this
    # missing_data = []  # list of indexes in block where data is missing
    # for d in range(len(block)):
    #     if len(block[d]) == 0:
    #         missing_data.append(d)

    if len(missing_data) == 2:

        block[missing_data[0]] = [0 for _ in range(len(Q_block))]
        block[missing_data[1]] = [0 for _ in range(len(Q_block))]

        not_P = P_syndrome_pt2(block)  # not_P is P ^ block[missing[0]] ^ block[missing[1]]
        not_Q = Q_syndrome_pt2(block)  # not_Q is Q if the missing data were 0s

        recovered_block2 = bytearray()
        recovered_block1 = bytearray()


        for a, b, c, d in zip(P_block, not_P, Q_block, not_Q,):
            for n in range(0, 256):
                # a ^ b = the xor of our 2 missing data blocks
                m = a ^ b ^ n

                recovered_n = multiply(missing_data[0]+1, n)
                recovered_m = multiply(missing_data[1]+1, m)

                if c ^ d == recovered_m ^ recovered_n:
                    recovered_block2.append(m)
                    recovered_block1.append(n)
                    break
            else:
                print("PANIC!!!!")
        block[missing_data[0]] = recovered_block1
        block[missing_data[1]] = recovered_block2

        return block

def number_missing_drives(block):
    stripe_count = 0
    count = 0
    if len(block[0]) == 0:
        count += 1
    if len(block[1]) == 0:
        count += 1
    if len(block[2]) == 0:
        count += 1
    if len(block[3]) == 0:
        count += 1
    if len(block[4]) == 0:
        count += 1
    if len(block[5]) == 0:
        count += 1

    return count