
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


class FileAlreadyExists(FileExistsError):

    def __init__(self, file):
        self.message = f"File {file} already exists."
        super().__init__(self.message)


class FileNotFound(FileNotFoundError):

    def __init__(self, file):
        _message = f"File {file} not found."
        super().__init__(_message)

