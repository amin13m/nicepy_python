
# -------------------------
# Costume Expertions
# -------------------------

class NicePathError(Exception):
    """Base exception for nicepath"""


class PathNotFoundError(NicePathError):
    pass


class NotAFileError(NicePathError):
    pass


class NotADirectoryError(NicePathError):
    pass


class WriteError(NicePathError):
    pass


class DeleteError(NicePathError):
    pass

