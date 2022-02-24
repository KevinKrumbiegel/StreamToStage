import logging
import pygame

logger = logging.getLogger(__package__)


class AudioPlayer:
    def __init__(self, config):
        pygame.mixer.init()
        self._loaded_sounds: dict[any, pygame.mixer.Sound] = {}

    def load(self, file_id, file_path):
        if file_id in self._loaded_sounds:
            return False

        sound = pygame.mixer.Sound(file_path)
        logger.log(logging.INFO, f"Loaded file {file_path}.")
        self._loaded_sounds[file_id] = sound
        return True

    def play(self, file_id):
        if file_id not in self._loaded_sounds:
            logger.log(logging.WARN, f"Cannot play sound with ID f{file_id}. Load the file first!")

        sound = self._loaded_sounds[file_id]
        sound.play()
