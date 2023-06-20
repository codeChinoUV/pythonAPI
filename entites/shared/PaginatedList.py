from dataclasses import dataclass

from entites.shared.Pagination import Pagination


@dataclass
class PaginatedList:
    """
    Class for management of paginated results
    """
    pagination: Pagination
    results: list

    def __init__(self, total: int, offset: int, limit: int, results: list):
        self.pagination = Pagination(total, offset, limit)
        self.results = results
