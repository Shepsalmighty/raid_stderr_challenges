from P_Q_syndrome import Q_syndrome


def recover_all(block1, block2, P_block, Q_block):
    #P_recovery
    if len(block1) > 0 and len(block2) > 0:
        return block1, block2
    if len(block1) == 0 and len(block2) > 0 and len(P_block) > 0:
        recovered_data = []
        for a, b in zip(P_block, block2):
            recovered_data.append(int(a) ^ int(b))
        block1 = bytes(recovered_data)
        return block1, block2
    if len(block1) > 0 and len(block2) == 0 and len(P_block) > 0:
        recovered_data = []
        for a, b in zip(P_block, block1):
            recovered_data.append(int(a) ^ int(b))
        block2 = bytes(recovered_data)
        return block1, block2
    #Q_recovery
    if len(block1) == 0 and len(P_block) == 0:
        recovered_data = []
        for a, b in zip(Q_block, block2):
            recovered_data.append(int(a) ^ (2* int(b)))
        return bytes(recovered_data), block2
        # return(Q_block ^ (2* block2))
    if len(block2) == 0 and len(P_block) == 0:
        recovered_data = []
        for a, b in zip(Q_block, block1):
            recovered_data.append((int(a) ^ int(b)) /2)
        return block1, bytes(recovered_data)
    if len(block1) == 0 and len(block2) == 0:
        recovered_block2 = []
        recovered_block1 = []
        for a, b in zip(P_block, Q_block):
            for n in range(0,256):
                Q_syndrome(bytes((n,)),bytes((n,)))
                if Q_syndrome(bytes((n,)),bytes((n,))) == P_block ^ Q_block:
                    recovered_block2.append(n)
                    recovered_block1.append(int(a) ^ int(n))
                    break
        return bytes(recovered_block1), bytes(recovered_block2)

# print(a + 1)