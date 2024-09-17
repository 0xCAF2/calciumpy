class AssignmentNotSupportedError(Exception):
    def __init__(self, message: str, ref: str, key: str):
        super().__init__(message)
        self.ref = ref
        self.key = key


class InvalidBreakError(Exception):
    pass


class InvalidContinueError(Exception):
    pass


class InvalidModuleNameError(Exception):
    def __init__(self, message: str, name: str):
        super().__init__(message)
        self.name = name


class InvalidReturnError(Exception):
    pass


class KeyNotContainedError(Exception):
    def __init__(self, message: str, ref: str, key: str, value: str):
        super().__init__(message)
        self.ref = ref
        self.key = key
        self.value = value


class NameNotFoundError(Exception):
    def __init__(self, message: str = "", name: str = ""):
        super().__init__(message + f" Name {name} is not defined")
        self.name = name


class OperatorNotSupportedError(Exception):
    pass


class OutOfRangeError(Exception):
    def __init__(self, message: str, ref: str, index: str, value: str):
        super().__init__(message)
        self.ref = ref
        self.index = index
        self.value = value
