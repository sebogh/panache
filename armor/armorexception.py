class ArmorException(Exception):

    def __init__(self, message: str, code: int = 0):
        self.code = code
        self.message = message

