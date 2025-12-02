import attrs


@attrs.define
class AggregateRoot:
    """
    Base class representing an Aggregate Root within a Domain-Driven Design (DDD)
    context. An Aggregate Root serves as the entry point to an aggregate, ensuring
    integrity and enforcing invariants across the entire aggregate structure.

    This class is intentionally minimal and provides only the `id` attribute,
    which uniquely identifies the aggregate within the system. Concrete domain
    aggregates should inherit from this class and extend it with additional
    domain-specific state and behavior.

    Attributes:
        id (str):
            Unique identifier of the aggregate root.
    """
    id: str
