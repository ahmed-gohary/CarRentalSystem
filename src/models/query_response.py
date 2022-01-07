

class InsertResponse:

    def __init__(self, entry_id, error_msg: str):
        self.entry_id = entry_id
        self.error_msg = error_msg


class UpdateResponse:

    def __init__(self, entry_id, error_msg: str):
        self.entry_id = entry_id
        self.error_msg = error_msg
