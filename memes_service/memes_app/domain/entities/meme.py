import datetime as dt
import dataclasses


@dataclasses.dataclass(slots=True)
class MemeEntity:
    id: str
    created_at: dt.datetime
    image_url: str
    title: str
    description: str
