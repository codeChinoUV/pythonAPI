from extension.wire.others import wire_others
from extension.wire.schemas import wire_schemas
from extension.wire.use_cases import wire_use_cases


def wire(container):
    """
    Wire all the classes need to be injected with dependencies
    :param container: The container to wire
    :return: None
    """
    wire_use_cases(container)
    wire_schemas(container)
    wire_others(container)
