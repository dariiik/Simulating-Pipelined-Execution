'''
MIPS-32 Instruction Level Simulatr

CSE261 UNIST
parse.py
'''

import util
import initialize
import ctypes


def parse_instr(buffer, index):
    instr = util.instruction()

    # Implement parsing logic here
    instr.value = util.fromBinary(buffer)
    instr.opcode = (instr.value >> 26) & 0x3F
    instr.rs = (instr.value >> 21) & 0x1F
    instr.rt = (instr.value >> 16) & 0x1F
    instr.rd = (instr.value >> 11) & 0x1F
    instr.shamt = (instr.value >> 6) & 0x1F
    instr.func_code = instr.value & 0x3F
    instr.imm = instr.value & 0xFFFF
    instr.target = instr.value & 0x3FFFFFF

    # Use mem_write to store the instruction in the simulated memory
    util.mem_write(util.MEM_TEXT_START + index * util.BYTES_PER_WORD, instr.value)
    
    return instr

def parse_data(buffer, index):
    # Implement parsing logic for data
    data_value = util.fromBinary(buffer)
    mem_address = util.MEM_DATA_START + index * util.BYTES_PER_WORD
    util.mem_write(mem_address, data_value)


def print_parse_result(INST_INFO):
    print("Instruction Information")

    for i in range(initialize.text_size//4):
        print("INST_INFO[%d].value : %x"% (i,INST_INFO[i].value))
        print("INST_INFO[%d].opcode : %d"% (i,INST_INFO[i].opcode))

        # TYPE I
        # 0xa: (0b001010)SLTI
        # 0x8: (0b001000)ADDI
        # 0x9: (0b001001)ADDIU
        # 0xc: (0b001100)ANDI
        # 0xf: (0b001111)LUI
        # 0xd: (0b001101)ORI
        # 0xb: (0b001011)SLTIU
        # 0x23: (0b100011)LW
        # 0x2b: (0b101011)SW
        # 0x4: (0b000100)BEQ
        # 0x5: (0b000101)BNE
        if INST_INFO[i].opcode == 0xa or \
            INST_INFO[i].opcode == 0x8 or \
            INST_INFO[i].opcode == 0x9 or \
            INST_INFO[i].opcode == 0xc or \
            INST_INFO[i].opcode == 0xf or \
            INST_INFO[i].opcode == 0xd or \
            INST_INFO[i].opcode == 0xb or \
            INST_INFO[i].opcode == 0x23 or \
            INST_INFO[i].opcode == 0x2b or \
            INST_INFO[i].opcode == 0x4 or \
            INST_INFO[i].opcode == 0x5:
            print("INST_INFO[%d].rs : %d"% (i,INST_INFO[i].rs))
            print("INST_INFO[%d].rt : %d"% (i,INST_INFO[i].rt))
            print("INST_INFO[%d].imm : %d"% (i,INST_INFO[i].imm))
            
        # TYPE R
        # 0x0: (0b000000)ADD, SLT, ADDU, AND, NOR, OR, SLTU, SLL, SRL, SUBU  if JR
        elif INST_INFO[i].opcode == 0x0:
            print("INST_INFO[%d].func_code : %d"% (i,INST_INFO[i].func_code))
            print("INST_INFO[%d].rs : %d"% (i,INST_INFO[i].rs))
            print("INST_INFO[%d].rt : %d"% (i,INST_INFO[i].rt))
            print("INST_INFO[%d].rd : %d"% (i,INST_INFO[i].rd))
            print("INST_INFO[%d].shamt : %d"% (i,INST_INFO[i].shamt))

        # TYPE J
        # 0x2: (0b000010)J
        # 0x3: (0b000011)JAL
        elif INST_INFO[i].opcode == 0x2 or INST_INFO[i].opcode == 0x3:
            print("INST_INFO[%d].target : %d"% (i,INST_INFO[i].target))
        else:
            print("Not available instruction")

    print("Memory Dump - Text Segment")
    for i in range(0, initialize.text_size, 4):
        print("text_seg[%d] : %x"% (i,util.mem_read(util.MEM_TEXT_START + i)))
    for i in range(0, initialize.data_size, 4):
        print("data_seg[%d] : %x"% (i,util.mem_read(util.MEM_DATA_START + i)))
    print("Current PC: %x" % util.CURRENT_STATE.PC)
