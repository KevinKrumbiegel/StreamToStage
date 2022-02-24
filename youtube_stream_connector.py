import logging
import message
import pytchat
import pytchat.core
import requests
import stream_connector
import threading

logger = logging.getLogger(__name__)


class YoutubeStreamConnector(stream_connector.StreamConnector):
    def __init__(self, config):
        super().__init__()
        self._worker = None
        self._video_url = config["videoUrl"]
        self._video_id = get_video_id_from_youtube_url(self._video_url)

        self._video_id = get_video_id_from_youtube_url(self._video_url)
        if self._video_id is None:
            logger.log(logging.ERROR, f"Cannot retrieve video ID of given url: {self._video_url}")
            return

        logger.log(logging.INFO, f"Video ID is: {self._video_id}")

        self._chat = pytchat.create(video_id=self._video_id)
        self._chat.get().sync_items()
        if not self._chat.is_alive():
            logger.log(logging.ERROR, f"Cannot connect to the chat of the given video ID: {self._video_id}")
            self._chat = None

    def connect(self):
        self._worker = self.Worker(self._chat, self._message_callback, super().on_stream_connection_lost)
        self._worker.start()

        logger.log(logging.INFO, f"Connected to Youtube video ID: {self._video_id}")
        super().on_stream_connected()

        return True

    def disconnect(self):
        self._worker.stop()
        logger.log(logging.INFO, f"Disconnected from Youtube video ID: {self._video_id}")

    def _message_callback(self, c):
        m = message.Message(c.id, c.messageEx, c.timestamp, c.author.name)
        super().on_message_received(m)

    class Worker:
        def __init__(self, chat: pytchat.core.PytchatCore, message_callback, connection_lost_callback=None):
            self._chat = chat
            self._connection_lost_callback = connection_lost_callback
            self._message_callback = message_callback
            self._thread = None
            self._stopped = True

        def start(self):
            if self._thread is not None:
                return

            self._stopped = False
            self._thread = threading.Thread(target=self._run)
            self._thread.start()

        def stop(self):
            if self._thread is None:
                return

            self._stopped = True
            self._thread.join()

        def _run(self):
            while self._chat.is_alive() and not self._stopped:
                for c in self._chat.get().sync_items():
                    self._message_callback(c)
            if not self._stopped:
                if self._connection_lost_callback is not None:
                    self._connection_lost_callback()
                self._stopped = True
                self._thread = None


def get_video_id_from_youtube_url(url):
    r = requests.get(url, allow_redirects=True, cookies={"CONSENT": "YES+cb.20210509-17-p0.de+F"})
    param_str = r.url.split("?")[1]
    params = param_str.split("&")
    for param in params:
        k, v = param.split("=")
        if k == "v":
            return v

    return None
