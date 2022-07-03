import struct
from dataclasses import dataclass


class Cartridge:
    FIELDS = [
        (None, "="),  # "Native" endian.
        (None, 'xxxx'),  # 0x100-0x103 (entrypoint)
        (None, '48x'),  # 0x104-0x133 (nintendo logo)
        ("title", '15s'),  # 0x134-0x142 (cartridge title) (0x143 is shared with the cgb flag)
        ("cgb", 'B'),  # 0x143 (cgb flag)
        ("new_licensee_code", 'H'),  # 0x144-0x145 (new licensee code)
        ("sgb", 'B'),  # 0x146 (sgb `flag)
        ("cartridge_type", 'B'),  # 0x147 (cartridge type)
        ("rom_size", 'B'),  # 0x148 (ROM size)
        ("ram_size", 'B'),  # 0x149 (RAM size)
        ("destination_code", 'B'),  # 0x14A (destination code)
        ("old_licensee_code", 'B'),  # 0x14B (old licensee code)
        ("mask_rom_version", 'B'),  # 0x14C (mask rom version)
        ("header_checksum", 'B'),  # 0x14D (header checksum)
        ("global_checksum", 'H'),  # 0x14E-0x14F (global checksum)
    ]

    CARTRIDGE_HEADER = "".join(format_type for _, format_type in FIELDS)
    CARTRIDGE_FIELDS = tuple(field for field, _ in FIELDS if field)

    @dataclass(frozen=True)
    class CartridgeMetadata:
        title: bytes
        cgb: int
        new_licensee_code: int
        sgb: int
        cartridge_type: int
        rom_size: int
        ram_size: int
        destination_code: int
        old_licensee_code: int
        mask_rom_version: int
        header_checksum: int
        global_checksum: int

    def __init__(self, buffer: bytes):
        self.buffer = buffer

    @property
    def metadata(self) -> CartridgeMetadata:
        return self.read_cartridge_metadata()

    def read_cartridge_metadata_as_dict(self, offset: int = 0x100):
        """
        Unpacks the cartridge metadata from `buffer` at `offset` and
        returns a dict.
        """
        data = struct.unpack_from(self.CARTRIDGE_HEADER, self.buffer, offset=offset)
        return dict((key, value) for key, value in zip(self.CARTRIDGE_FIELDS, data))

    def read_cartridge_metadata(self, offset: int = 0x100) -> CartridgeMetadata:
        """
        Unpacks the cartridge metadata from `buffer` at `offset` and
        returns a `CartridgeMetadata` dataclass.
        """
        data = struct.unpack_from(self.CARTRIDGE_HEADER, self.buffer, offset=offset)
        return self.CartridgeMetadata(*data)
