import datetime as dt
import dataclasses


@dataclasses.dataclass(slots=True)
class MemeEntity:
    id: str
    created_at: dt.datetime
    title: str
    description: str
