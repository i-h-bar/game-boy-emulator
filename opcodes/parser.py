import json

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Operand:
    immediate: bool
    name: str
    bytes: int | None = None
    value: int | None = None
    adjust: Literal["+", "-"] | None = None

    def copy(self, value):
        return Operand(
            immediate=self.immediate,
            name=self.name,
            bytes=self.bytes,
            value=value,
            adjust=self.adjust
        )

    def __str__(self):
        if self.adjust is None:
            adjust = ""
        else:
            adjust = self.adjust
        if self.value is not None:
            if self.bytes is not None:
                val = hex(self.value)
            else:
                val = self.value
            v = val
        else:
            v = self.name
        v = v + adjust
        if self.immediate:
            return v
        return f'({v})'


@dataclass
class Instruction:
    opcode: int
    immediate: bool
    operands: list[Operand]
    cycles: list[int]
    bytes: int
    mnemonic: str
    comment: str = ""

    def copy(self, operands):
        return Instruction(
            opcode=self.opcode,
            immediate=self.immediate,
            operands=operands,
            cycles=self.cycles,
            bytes=self.bytes,
            mnemonic=self.mnemonic
        )

    def __str__(self):
        ops = ', '.join(str(op) for op in self.operands)
        s = f"{self.mnemonic:<8} {ops}"
        if self.comment:
            s = s + f" ; {self.comment:<10}"
        return s


def _parse(key: str, value: dict) -> Instruction:
    return Instruction(
        opcode=int(key, base=16),
        immediate=value["immediate"],
        operands=[
            Operand(
                name=operand["name"],
                immediate=operand["immediate"],
                bytes=operand.get("bytes"),
                value=operand.get("value"),
                adjust=operand.get("adjust")
            ) for operand in value["operands"]
        ],
        cycles=value["cycles"],
        bytes=value["bytes"],
        mnemonic=value["mnemonic"],
        comment=value.get("comment", "")
    )


with open("opcodes/opcodes.json") as _in_json:
    _inst_json = json.load(_in_json)

UNPREFIXED = {int(key, base=16): _parse(key, value) for key, value in _inst_json["unprefixed"].items()}
CBPREFIXED = {int(key, base=16): _parse(key, value) for key, value in _inst_json["cbprefixed"].items()}


def load_opcodes() -> tuple[dict[int, Instruction], dict[int, Instruction]]:
    return CBPREFIXED, UNPREFIXED
