from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Callable

from common.domain.aggregate_root import AggregateRoot

# Define a type variable T that is bound to AggregateRoot
T = TypeVar('T', bound=AggregateRoot)


class AggregateRootRepository(ABC, Generic[T]):
    """
    Base abstract repository for managing Aggregate Root entities following
    Domain-Driven Design (DDD) principles. This repository defines the core
    operations required to interact with any underlying storage mechanism,
    such as a database, caching layer, or external persistence service.

    This class provides the contract that all concrete repositories must
    implement, ensuring consistency across all persistence implementations.

    Abstract Methods:
        - exists(_id: str) -> bool
        - find(_id: str) -> T | None
        - find_all(predicate: Callable[[T], bool] | None) -> list[T]
        - find_ids() -> list[str]
        - delete(aggregate: T) -> None
        - delete_all() -> None
        - save(aggregate: T) -> None
        - save_all(aggregates: list[T]) -> None
    """

    def __init__(self, aggregate_type: Type[T]) -> None:
        """
        Initializes the repository with the type of Aggregate Root it manages.

        Parameters:
            aggregate_type (Type[T]):
                The concrete Aggregate Root type handled by this repository.
                Must be a subclass of `AggregateRoot`.

        Raises:
            TypeError:
                - If `aggregate_type` is not a type.
                - If `aggregate_type` is not a subclass of AggregateRoot.
        """
        if not isinstance(aggregate_type, type):
            raise TypeError("aggregate_type must be a type")

        if not issubclass(aggregate_type, AggregateRoot):
            raise TypeError("aggregate_type must be a subclass of AggregateRoot")

        self._aggregate_type = aggregate_type

    @abstractmethod
    def exists(self, _id: str) -> bool:
        """
        Checks whether an Aggregate Root with the given identifier exists.

        Parameters:
            _id (str): Unique identifier of the aggregate.

        Returns:
            bool: True if the aggregate exists, False otherwise.
        """
        pass

    @abstractmethod
    def find(self, _id: str) -> T | None:
        """
        Retrieves an Aggregate Root by its identifier.

        Parameters:
            _id (str): Unique identifier of the aggregate.

        Returns:
            T | None: The aggregate instance if found, otherwise None.
        """
        pass

    @abstractmethod
    def find_all(self, predicate: Callable[[T], bool] = None) -> list[T]:
        """
        Retrieves all stored Aggregate Roots. Optionally applies a predicate
        to filter the results.

        Parameters:
            predicate (Callable[[T], bool], optional):
                Function that receives an aggregate instance and returns True
                if it should be included in the result.

        Returns:
            list[T]: A list of aggregates matching the criteria.
        """
        pass

    @abstractmethod
    def find_ids(self) -> list[str]:
        """
        Returns all identifiers of the aggregates stored in the repository.

        Returns:
            list[str]: A list of aggregate identifiers.
        """
        pass

    @abstractmethod
    def delete(self, aggregate: T) -> None:
        """
        Deletes a specific Aggregate Root from the repository.

        Parameters:
            aggregate (T): The aggregate instance to be deleted.
        """
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """
        Deletes all Aggregate Roots managed by this repository.
        """
        pass

    @abstractmethod
    def save(self, aggregate: T) -> None:
        """
        Saves or updates an Aggregate Root in the repository.

        Parameters:
            aggregate (T): The aggregate instance to be saved.
        """
        pass

    @abstractmethod
    def save_all(self, aggregates: list[T]) -> None:
        """
        Saves or updates multiple Aggregate Roots in the repository.

        Parameters:
            aggregates (list[T]): A list of aggregate instances to be saved.
        """
        pass

