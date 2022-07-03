import sys
from pathlib import Path

from opcodes.parser import load_opcodes


class Decoder:
    def __init__(
            self,
            data: bytes,
            address: int
    ):
        self.data = data
        self.address = address
        self.prefixed_instructions, self.instructions = load_opcodes()

    @classmethod
    def create(cls, data: bytes, address: int = 0):
        return cls(
            data=data,
            address=address,
        )

    def read(self, address: int, count: int = 1):
        """
        Reads `count` bytes starting from `address`.
        """
        if 0 <= address + count <= len(self.data):
            v = self.data[address: address + count]
            return int.from_bytes(v, sys.byteorder)
        else:
            raise IndexError(f'{address=}+{count=} is out of range')

    def decode(self, address: int):
        """
        Decodes the instruction at `address`.
        """
        opcode = self.read(address)
        address += 1
        # 0xCB is a special prefix instruction. Read from
        # prefixed_instructions instead and increment address.
        if opcode == 0xCB:
            opcode = self.read(address)
            address += 1
            instruction = self.prefixed_instructions[opcode]
        else:
            instruction = self.instructions[opcode]
        new_operands = []
        for operand in instruction.operands:
            if operand.bytes is not None:
                value = self.read(address, operand.bytes)
                address += operand.bytes
                new_operands.append(operand.copy(value))
            else:
                # No bytes; that means it's not a memory address
                new_operands.append(operand)
        decoded_instruction = instruction.copy(operands=new_operands)
        return address, decoded_instruction

    def disassemble(self, address: int, count: int):
        """
        Disassembles the byte stream from "address" to "address + count" into Instructions and Opcodes
        """
        for _ in range(count):
            try:
                new_address, instruction = self.decode(address)
                print(f'{address:>04X} {instruction}')
                address = new_address
            except IndexError as e:
                print('ERROR - {e!s}')
                break


if __name__ == "__main__":
    decoder = Decoder.create(Path("Tetris.gb").read_bytes())
    decoder.disassemble(0x150, 320)
