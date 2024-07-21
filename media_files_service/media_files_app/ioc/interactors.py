from dishka import Provider, Scope, provide_all

from media_files_app.application.interactors.file import (
    DownloadFileInteractor,
    UploadFileInteractor,
)


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    interactors = provide_all(
        UploadFileInteractor,
        DownloadFileInteractor,
    )
