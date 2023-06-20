class Pagination:
    """
    Class for pagination management
    """
    total: int
    skip: int
    limit: int

    def __init__(self, total: int, skip: int, limit: int):
        self.total = total
        self.skip = skip
        self.limit = limit
