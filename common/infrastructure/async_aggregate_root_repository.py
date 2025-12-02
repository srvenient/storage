from abc import ABC
from typing import TypeVar, Callable, Any, Coroutine

from trio import to_thread, CapacityLimiter

from common.domain.aggregate_root import AggregateRoot
from common.infrastructure.aggregate_root_repository import AggregateRootRepository

# Define a type variable T that is bound to AggregateRoot
T = TypeVar('T', bound=AggregateRoot)


class AsyncAggregateRootRepository(AggregateRootRepository[T], ABC):
    """
    Asynchronous extension of `AggregateRootRepository` that provides async
    wrappers around all synchronous repository operations. This allows
    non-blocking execution of I/O-bound repository methods by running them
    inside worker threads using Trio's `to_thread.run_sync`.

    This class does not implement repository logic itself; it delegates to
    the synchronous methods defined in the parent class while exposing async
    equivalents for use in asynchronous workflows.

    Features:
        - Offloads synchronous repository calls to worker threads.
        - Uses a `CapacityLimiter` to control the maximum number of concurrent
          thread executions.
        - Provides async versions of all repository operations such as:
          `exists_async`, `find_async`, `find_all_async`, `save_async`, etc.
    """

    def __init__(self, aggregate_type: type[T], max_threads: int = 5) -> None:
        """
        Initializes the asynchronous repository.

        Parameters:
            aggregate_type (type[T]):
                The concrete Aggregate Root type handled by the repository.
                Must be a subclass of `AggregateRoot`.

            max_threads (int, optional):
                Maximum number of worker threads allowed for async execution.
                Defaults to 5.

        Notes:
            A `CapacityLimiter` is used to ensure controlled concurrency when
            offloading synchronous repository calls to worker threads.
        """
        super().__init__(aggregate_type)
        self._thread_limiter = CapacityLimiter(max_threads)

    async def exists_async(self, _id: str) -> Coroutine[Any, Any, bool]:
        """
        Asynchronously checks whether an Aggregate Root with the given ID exists.

        Parameters:
            _id (str): Unique identifier of the aggregate.

        Returns:
            Coroutine[Any, Any, bool]:
                A coroutine resolving to True if the aggregate exists,
                False otherwise.
        """
        return to_thread.run_sync(
            super().exists,
            _id,
            limiter=self._thread_limiter,
        )

    async def find_async(self, _id: str) -> Coroutine[Any, Any, T | None]:
        """
        Asynchronously retrieves an Aggregate Root by its identifier.

        Parameters:
            _id (str): Unique identifier of the aggregate.

        Returns:
            Coroutine[Any, Any, T | None]:
                A coroutine resolving to the aggregate instance if found,
                otherwise None.
        """
        return to_thread.run_sync(
            super().find,
            _id,
            limiter=self._thread_limiter,
        )

    async def find_all_async(self, predicate: Callable[[T], bool] = None) -> Coroutine[Any, Any, list[T]]:
        """
        Asynchronously retrieves all stored Aggregate Roots. Optionally applies
        a predicate function to filter results.

        Parameters:
            predicate (Callable[[T], bool], optional):
                A function that receives an aggregate instance and returns True
                if it should be included in the result.

        Returns:
            Coroutine[Any, Any, list[T]]:
                A coroutine resolving to a list of aggregates.
        """
        return to_thread.run_sync(
            super().find_all,
            predicate,
            limiter=self._thread_limiter,
        )

    async def find_ids_async(self) -> Coroutine[Any, Any, list[str]]:
        """
        Asynchronously retrieves all aggregate identifiers stored in the repository.

        Returns:
            Coroutine[Any, Any, list[str]]:
                A coroutine resolving to a list of aggregate IDs.
        """
        return to_thread.run_sync(
            super().find_ids,
            args=(),
            limiter=self._thread_limiter,
        )

    async def delete_async(self, aggregate: T) -> Coroutine[Any, Any, None]:
        """
        Asynchronously deletes the provided Aggregate Root instance.

        Parameters:
            aggregate (T): The aggregate instance to delete.

        Returns:
            Coroutine[Any, Any, None]
        """
        return to_thread.run_sync(
            super().delete,
            aggregate,
            limiter=self._thread_limiter,
        )

    async def delete_all_async(self) -> Coroutine[Any, Any, None]:
        """
        Asynchronously deletes all Aggregate Roots stored in the repository.

        Returns:
            Coroutine[Any, Any, None]
        """
        return to_thread.run_sync(
            super().delete_all,
            args=(),
            limiter=self._thread_limiter,
        )

    async def save_async(self, aggregate: T) -> Coroutine[Any, Any, None]:
        """
        Asynchronously saves or updates an Aggregate Root instance.

        Parameters:
            aggregate (T): The aggregate instance to save.

        Returns:
            Coroutine[Any, Any, None]
        """
        return to_thread.run_sync(
            super().save,
            aggregate,
            limiter=self._thread_limiter,
        )
