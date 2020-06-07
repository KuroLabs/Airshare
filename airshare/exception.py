"""Exceptions defined for Airshare."""


__all__ = ["CodeExistsError", "CodeNotFoundError", "IsNotReceiverError",
           "IsNotSenderError"]


class AirshareError(Exception):
    """Base class for all Airshare-related exceptions."""


class CodeExistsError(AirshareError):
    r"""Exception to be raised when Airshare code already exists.

    To be raised when trying to create or serve an Airshare server, but
    one already exists with that identifying code.
    """
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return "CodeExistsError: The Airshare `" + self.code \
               + "` already exists!"


class CodeNotFoundError(AirshareError):
    r"""Exception to be raised when the Airshare code is not found.

    To be raised when trying to download from or upload to an Airshare,
    but none exists with that identifying code.
    """
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return "CodeNotFoundError: The Airshare `" + self.code \
               + "` was not found!"


class IsNotReceiverError(AirshareError):
    r"""Exception to be raised when trying to upload to a non-receiver.

    To be raised when trying to upload to an Airshare when it exists but
    is not a receiver.
    """
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return "IsNotReceiverError: The Airshare `" + self.code \
               + "` is not an Upload Receiver!"


class IsNotSenderError(AirshareError):
    r"""Exception to be raised when trying to receive from a non-sender.

    To be raised when trying to download from an Airshare when it exists but
    is not a sender.
    """
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return "IsNotSenderError: The Airshare `" + self.code \
               + "` is not a Text or File Sender!"
