import logging
import threading

import audio_player
import audio_database
import message_processor
import youtube_stream_connector
import time

logger = logging.getLogger(__package__)


class Controller:
    def __init__(self, config):
        self._db = audio_database.AudioDatabase(config["audioDatabase"])
        self._player = audio_player.AudioPlayer(config["audioPlayer"])
        self._proc = message_processor.MessageProcessor(config["messageProcessor"])
        self._con = youtube_stream_connector.YoutubeStreamConnector(config["youtubeStreamConnector"])
        self._con.subscribe(self)
        self._preload_audio_files()
        self._stopped = True
        self._thread = None

    def start(self):
        logger.log(logging.INFO, "Controller starting...")
        if self._thread is not None:
            return

        self._stopped = False
        self._thread = threading.Thread(target=self._run)
        self._thread.start()
        logger.log(logging.INFO, "Controller started")

    def stop(self):
        logger.log(logging.INFO, "Controller terminating...")
        if self._thread is None:
            return

        self._stopped = True
        self._thread.join()
        self._thread = None
        logger.log(logging.INFO, "Controller terminated")

    def _run(self):
        self._con.connect()
        while not self._stopped:
            time.sleep(1)

        self._con.disconnect()

    def _preload_audio_files(self):
        errors = 0
        files = self._db.get_all_files()
        for file_id, file_path in files:
            if not self._player.load(file_id, file_path):
                errors += 1

        logger.log(logging.INFO, f"Successfully loaded {(len(files) - errors)} of {len(files)} audio files.")

    def on_stream_connected(self):
        logger.log(logging.INFO, "Stream connected.")
        print("Stream connected")

    def on_stream_connection_lost(self):
        logger.log(logging.INFO, "Stream connection lost.")
        print("Stream connection lost")

    def on_stream_disconnected(self):
        logger.log(logging.INFO, "Stream disconnected.")
        print("Stream disconnected")

    def on_stream_message_received(self, m):
        logger.log(logging.DEBUG, f"From {m.get_author_name()}: {m.get_message()}")

        audio_id = self._proc.process(m)
        if audio_id is None:
            return

        print(f"Playing {audio_id}. Triggered by: " + str(m.get_message()))
        logger.log(logging.DEBUG, f"Emoji matched! Playing audio file id {audio_id}")
        self._player.play(audio_id)

