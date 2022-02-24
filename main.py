import json
import logging
import controller
import sys

logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.INFO)


def main():
    try:
        f = open("config.json", "r")
        config = json.load(f)
        f.close()
    except Exception as err:
        logging.log(logging.ERROR, f"Could not load config: {str(err)}")
        return 1

    c = controller.Controller(config)
    c.start()

    while input() != "exit":
        pass

    c.stop()


if __name__ == '__main__':
    sys.exit(main())
