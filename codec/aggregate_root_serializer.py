from abc import ABC
from typing import TypeVar, Generic

from api.domain.aggregate_root import AggregateRoot

AggregateType = TypeVar('AggregateType', bound=AggregateRoot)
ReadType = TypeVar('ReadType')


class AggregateRootSerializer(ABC, Generic[AggregateType, ReadType]):
    def serialize(self, aggregate: AggregateType) -> ReadType:
        pass
