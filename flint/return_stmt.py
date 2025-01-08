# File for return statements

class Return_stmts(Exception):
    def __init__(self, value):
        super().__init__(None)
        self.value = value

    