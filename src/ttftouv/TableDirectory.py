from ttftouv.cmap.CMapTable import CMapTable
from ttftouv.glyf.GlyfTable import GlyfTable
from ttftouv.HeadTable import HeadTable
from ttftouv.Table import Table


class TableDirectoryFactory:
    @staticmethod
    def create_table(tag: str, table_data: bytes) -> Table:
        match tag:
            case "cmap":
                return CMapTable(table_data)
            case "glyf":
                return GlyfTable(table_data)
            case "head":
                return HeadTable(table_data)
            case _:
                raise NotImplementedError("This table type is not supported")
