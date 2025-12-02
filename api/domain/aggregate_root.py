class AggregateRoot:
    """
    Base class representing an Aggregate Root within a Domain-Driven Design (DDD)
    context.

    An Aggregate Root serves as the entry point to an aggregate, ensuring
    integrity and enforcing invariants across the entire aggregate structure.

    Concrete domain aggregates should inherit from this class and extend it with
    additional domain-specific state and behavior.
    """

    def __init__(self, _id: str):
        """
        Initialize a new AggregateRoot.

        Args:
            _id (str): Unique identifier of the aggregate root. Internally stored
                       as `_id` but exposed via the `id` property.
        """
        self._id = _id

    @property
    def id(self) -> str:
        """
        Read-only property to access the unique identifier of the aggregate root.

        Returns:
            str: The unique identifier stored in `_id`.
        """
        return self._id
