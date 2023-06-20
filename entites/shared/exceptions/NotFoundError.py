class NotFoundError(Exception):
    """
    Custom exception not found for the validation if an item exists in a collection
    """
    item_id: str
    message: str
    collection_name: str

    def __init__(self, item_id: str, collection_name: str):

        self.message = "Not found the item"
        self.item_id = item_id
        self.collection_name = collection_name
        super().__init__(self.message)
