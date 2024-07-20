from memes_app.domain.exceptions.base import CoreError


class MemeError(CoreError): ...


class MemeNotFoundError(MemeError): ...
