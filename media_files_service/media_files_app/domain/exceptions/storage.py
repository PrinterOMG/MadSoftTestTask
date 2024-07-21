from media_files_app.domain.exceptions.base import CoreError


class StorageError(CoreError): ...


class FileNotFoundInStorageError(StorageError): ...
