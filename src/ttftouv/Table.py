class Table:
    def __init__(self, table_data: bytes) -> None:
        self.table_data: bytes = table_data

    def __repr__(self) -> str:
        return f"TableDirectory({self.table_data})"
