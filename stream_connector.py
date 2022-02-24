import logging
import message
import threading

logger = logging.getLogger(__package__)


class StreamConnector:
    def __init__(self):
        self._connected = False
        self._lock = threading.Lock()
        self._on_stream_connected = []
        self._on_stream_connection_lost = []
        self._on_stream_disconnected = []
        self._on_stream_message_received = []

    def subscribe(self, receiver, on_connected=True, on_connection_lost=True, on_disconnected=True,
                  on_message_received=True):
        self._lock.acquire()

        if on_connected and receiver not in self._on_stream_connected:
            self._on_stream_connected.append(receiver)

        if on_connection_lost and receiver not in self._on_stream_connection_lost:
            self._on_stream_connection_lost.append(receiver)

        if on_disconnected and receiver not in self._on_stream_disconnected:
            self._on_stream_disconnected.append(receiver)

        if on_message_received and receiver not in self._on_stream_message_received:
            self._on_stream_message_received.append(receiver)

        self._lock.release()

    def is_connected(self):
        return self._connected

    def on_stream_connected(self):
        logger.log(logging.INFO, "Stream connected")
        self._connected = True
        for s in self._on_stream_connected:
            s.on_stream_connected()

    def on_stream_connection_lost(self):
        logger.log(logging.INFO, "Stream connection lost")
        self._connected = False
        for s in self._on_stream_connection_lost:
            s.on_stream_connection_lost()

    def on_stream_disconnected(self):
        logger.log(logging.INFO, "Stream disconnected")
        self._connected = False
        for s in self._on_stream_disconnected:
            s.on_stream_disconnected()

    def on_message_received(self, m: message.Message):
        logger.log(logging.INFO, "Stream message received")
        for s in self._on_stream_message_received:
            s.on_stream_message_received(m)
