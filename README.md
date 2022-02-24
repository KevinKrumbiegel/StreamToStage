# StreamToStage
This project aims to implement a feedback channel from web stream chats (such as YouTube) to those who are acting on a stage.

Therefore, a connection to a web stream chat will be established (so far, only YouTube is supported) and all incoming 
messages will be scanned. 
If special emojis occur in the chat messages, a sound will be played on the local device.

In consequence, this tool can be used to translate the virtual feedback into real feedback that can be
heard by the artists standing on stage.

## Prerequisites
Python3 must be installed. In case, a windows system will be used, the dependencies might not get installed correctly
using only the setup script.

## Usage

Download the code, run the *setup* script to install dependencies and then, run the main file using ``python main.py``.

## Configuration
So far, all configuration must be done before running the actual program.
Therefore, create a ``config.json`` file that should have the following structure:
```json
{
  "audioDatabase": {
    "audioFiles": [
      {
        "id": 0,
        "path": "~/path/to/audio1.mp3"
      },
      {
        "id": 1,
        "path": "~/path/to/audio1.mp3"
      }
    ]
  },
  "audioPlayer": {

  },
  "messageProcessor": {
    "emojis": [
      {
        "id": "\uD83E\uDD23",
        "audioFile": 0
      },
      {
        "id": "\u0001\uF600",
        "audioFile": 0
      },
      {
        "id": "\u0001\uF44F",
        "audioFile": 1
      },
    ]
  },
  "youtubeStreamConnector": {
    "videoUrl": "https://www.youtube.com/watch?v=<YOUR-VIDEO-ID>"
  }
}
```

The id of an audio file is the same number that needs to be associated to an emoji.
In consequence, with any occurrence of the emoji in the chat, the specified sound file will be played.