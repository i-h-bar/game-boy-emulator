from pathlib import Path

from cartridge.reader import Cartridge


def test_cartridge_meta_data():
    cartridge = Cartridge(Path("Tetris.gb").read_bytes())
    metadata_class = cartridge.read_cartridge_metadata()
    metadata_dict = cartridge.read_cartridge_metadata_as_dict()

    for key in metadata_dict:
        assert metadata_dict[key] == metadata_class.__getattribute__(key)
