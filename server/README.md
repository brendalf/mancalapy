# mancalapy - backend

Backend written in Python 3.11 with Flask for the mancalapy game.  
The server runs in the post `8000` and to start only the server you can run `make start` inside this folder.

The backend has of two main parts, the `core` and the `api`.  
* The `core` package represents the core logic for a mancala game. It's composed of three classes.
  * The `Board` class which represents the board of the game.
  * The `PitReference` class, which is used to represent a reference to a specific pit in the board.
  * The `MancalaGame` class that represents the game itself.
* The `api` side represents the SocketIO API that manages users sessions and their interactions with a game. It's composed of:
  * A session controller that translates the API events in actions in a given game.
  * The events that the server is listening for.
  * The server also exposes a `/healthcheck` endpoint where we can check the list of players connected and the active games.

The image below describes how both parts interact together:  

<img width="700" alt="image" src="https://user-images.githubusercontent.com/10671410/229759616-44ae1147-785a-43c8-b030-8fb0556b50dc.jpg">

## Structure
`mancala_backend/`: source code folder.  
-- `core/`: the mancala game core logic.  
-- `models/`: the api classes.  
-- `events.py`: all the events the server is listening for.  
-- `server.py`: helper functions to create the server routes.  
-- `controller.py`: the controller that translates events into in-game actions.

The image below describes how these parts interact together:

<img width="700" alt="image" src="https://user-images.githubusercontent.com/10671410/229940497-d9c99aef-f8fe-4e65-b8dc-a22928a51f81.jpg">
