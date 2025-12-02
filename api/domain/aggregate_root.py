import attrs


@attrs.define
class AggregateRoot:
    """
    Base class for Aggregate Roots in Domain-Driven Design (DDD).

    Attributes:
        id (str): Unique identifier for the aggregate root.

    Notes:
        - Intended to be inherited by concrete domain aggregates.
        - Provides a simple base with an identifier, while concrete aggregates
          can add domain-specific attributes and behavior.
        - By default, `id` can be modified after creation. Use `frozen=True`
          in @attrs.define if you want it to be immutable.
    """
    id: str = attrs.field(init=True)
