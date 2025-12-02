from typing import TypeVar, Callable

from api.domain.aggregate_root import AggregateRoot
from api.infrastructure.aggregate_root_repository import AggregateRootRepository

# Define a type variable T that is bound to AggregateRoot
T = TypeVar('T', bound=AggregateRoot)


class InMemoryAggregateRootRepository(AggregateRootRepository[T]):
    """
    In-memory implementation of `AggregateRootRepository` intended primarily for
    testing, prototyping, or lightweight applications that do not require
    persistent storage.

    This repository stores Aggregate Root instances in a simple Python
    dictionary, allowing fast access without external dependencies. It fully
    adheres to the repository interface defined by the parent class while
    avoiding any I/O or database operations.

    Characteristics:
        - Fast and lightweight storage mechanism.
        - No persistence beyond process lifetime.
        - Useful for unit tests, mocks, and simple applications.
    """

    def __init__(self, aggregate_type: type[T]) -> None:
        """
        Initializes the in-memory repository.

        Parameters:
            aggregate_type (type[T]):
                The concrete Aggregate Root type managed by this repository.
                Must be a subclass of `AggregateRoot`.

        Notes:
            The repository uses an internal dictionary mapping aggregate IDs
            (strings) to aggregate instances.
        """
        super().__init__(aggregate_type)
        self._storage: dict[str, T] = {}

    def exists(self, _id: str) -> bool:
        return _id in self._storage

    def find(self, _id: str) -> T | None:
        return self._storage.get(_id)

    def find_all(self, predicate: Callable[[T], bool] = None) -> list[T]:
        if predicate is None:
            return list(self._storage.values())
        return [agg for agg in self._storage.values() if predicate(agg)]

    def find_ids(self) -> list[str]:
        return list(self._storage.keys())

    def delete(self, aggregate: T) -> None:
        if aggregate.id in self._storage:
            del self._storage[aggregate.id]

    def delete_all(self) -> None:
        self._storage.clear()

    def save(self, aggregate: T) -> None:
        self._storage[aggregate.id] = aggregate

    def save_all(self, aggregates: list[T]) -> None:
        for aggregate in aggregates:
            self._storage[aggregate.id] = aggregate
