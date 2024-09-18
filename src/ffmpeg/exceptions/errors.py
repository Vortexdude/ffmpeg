class BaseExc(Exception):
    MESSAGE: str

    def __init__(self):
        super().__init__(self.MESSAGE)


class ChapterAlreadyExistsException(BaseExc):
    MESSAGE = "Chapter already already Exists"


class NoChapterProvided(BaseExc):
    MESSAGE = "No chapter Provided"


class NoChapterFound(BaseExc):
    MESSAGE = "No chapter is found in the video file"


class NoStreamFound(BaseExc):
    MESSAGE = "No Stream found in the video file"


class InvalidCommand(BaseExc):
    MESSAGE = "Error with the command"


class ProtocolNotDefined(BaseExc):
    MESSAGE = "Only Support HTTP protocol"


class URLStreamError(BaseExc):
    MESSAGE = "Only Support the m3u8 HLS stream"


class InvalidOptionError(ValueError):
    def __init__(self, options: str, optional_values=None):
        message = f"The option '{options}' is invalid. "
        if optional_values:
            message += f"only possible values are {optional_values}"

        super().__init__(message)


class FileAlreadyExists(FileExistsError):

    def __init__(self, file):
        self.message = f"File '{file}' already exists."
        super().__init__(self.message)


class InvalidTypeError(ValueError):
    message: str = f"Option type Error"

    def __init__(self, arg):
        super().__init__(self.message)


class FileNotFound(FileNotFoundError):

    def __init__(self, file):
        _message = f"File {file} not found."
        super().__init__(_message)
