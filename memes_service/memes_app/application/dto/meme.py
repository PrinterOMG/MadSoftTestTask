import dataclasses


@dataclasses.dataclass(slots=True)
class NewMemeDTO:
    title: str
    description: str


@dataclasses.dataclass(slots=True)
class UpdateMemeDTO:
    id: str
    title: str
    description: str
