from abc import ABC
from typing import TypeVar, Generic

from api.domain.aggregate_root import AggregateRoot

AggregateType = TypeVar('AggregateType', bound=AggregateRoot)
ReadType = TypeVar('ReadType')


class AggregateRootDeserializer(ABC, Generic[ReadType, AggregateType]):
    def deserialize(self, data: ReadType) -> AggregateType:
        pass
