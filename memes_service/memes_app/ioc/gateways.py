from dishka import AnyOf, Provider, Scope, provide

from memes_app.application.interfaces.meme import (
    MemeDeleter,
    MemeGatewayProtocol,
    MemeReader,
    MemeSaver,
    MemeUpdater,
)
from memes_app.infrastructure.gateways.meme import MemeGateway


class GatewaysProvider(Provider):
    scope = Scope.REQUEST

    meme_gateway = provide(
        MemeGateway,
        provides=AnyOf[
            MemeReader,
            MemeSaver,
            MemeUpdater,
            MemeDeleter,
            MemeGatewayProtocol,
        ],
    )
