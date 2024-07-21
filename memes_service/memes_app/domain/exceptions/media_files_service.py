from memes_app.domain.exceptions.base import CoreError


class MediaFileServiceError(CoreError): ...


class FileNotFoundInMediaFilesServiceError(MediaFileServiceError): ...
