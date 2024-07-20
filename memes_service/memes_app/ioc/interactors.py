from dishka import Provider, Scope, provide_all

from memes_app.application.interactors.meme import (
    CreateMemeInteractor,
    DeleteMemeInteractor,
    GetAllMemesInteractor,
    GetMemeByIdInteractor,
    UpdateMemeInteractor,
)


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    interactors = provide_all(
        GetAllMemesInteractor,
        GetMemeByIdInteractor,
        CreateMemeInteractor,
        UpdateMemeInteractor,
        DeleteMemeInteractor,
    )
