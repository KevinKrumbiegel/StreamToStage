import message


class MessageProcessor:
    def __init__(self, config):
        self._filters = []
        self._emoji_id_audio_file_id_dict = {}

        emoji_list = []
        for e in config["emojis"]:
            emoji_id = e["id"]
            audio_file_id = e["audioFile"]

            emoji_list.append(emoji_id)
            self._emoji_id_audio_file_id_dict[emoji_id] = audio_file_id

        self._filters.append(self.EmojiFilter(emoji_list))

    def process(self, m: message.Message):
        result = None
        for f in self._filters:
            result = f.filter(m)
            if result is None:
                return None

        audio_file = self._emoji_id_audio_file_id_dict[result]
        return audio_file

    class Filter:
        def filter(self, m: message.Message):
            return True

    class EmojiFilter(Filter):
        def __init__(self, emoji_list):
            self._emoji_list = emoji_list

        def filter(self, m: message.Message):
            for o in m.get_message():
                if type(o) is not dict:
                    continue

                if o["id"] in self._emoji_list:
                    return o["id"]

            return None
