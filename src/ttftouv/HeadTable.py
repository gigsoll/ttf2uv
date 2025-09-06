from ttftouv.Table import Table


class HeadTable(Table):
    def __init__(self, table_data: bytes) -> None:
        super().__init__(table_data)
