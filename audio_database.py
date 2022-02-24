import logging
import pathlib

logger = logging.getLogger(__package__)


class AudioDatabase:
    def __init__(self, config):
        self._files = {}

        for f in config["audioFiles"]:
            if f["id"] in self._files:
                logger.log(logging.WARN, f"Did not add file {f['path']}: ID {f['id']} already exists!")
                continue

            p = pathlib.Path(f["path"])
            if not p.exists():
                logger.log(logging.WARN, f"Did not add file {f['path']}: File not found!")
                continue

            if not p.is_file():
                logger.log(logging.WARN, f"Did not add file {f['path']}: Path does not refer to a file!")
                continue

            self._files[f["id"]] = f["path"]
            logger.log(logging.DEBUG, f"Added file {f['path']} with ID {f['id']}")

    def get_all_files(self):
        return list((file_id, self._files[file_id]) for file_id in self._files)

    def get_path_by_id(self, file_id):
        if file_id in self._files:
            return self._files[file_id]
        else:
            return None
