class Message:
    def __init__(self, message_id, message, timestamp, author):
        self._author_name = author
        self._id = message_id
        self._message = message
        self._timestamp = timestamp

    def get_author_name(self):
        return self._author_name

    def get_id(self):
        return self._id

    def get_message(self):
        return self._message

    def get_timestamp(self):
        return self._timestamp
