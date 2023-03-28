<img src="https://user-images.githubusercontent.com/10671410/228223613-d171be14-8d8d-4f80-b068-31e1da6244bc.png" width="100">

# mancalapy

Mancala game implemmented in Python.

> "The mancala games are a family of two-player turn-based strategy board games played with small stones, beans, or seeds and rows of holes or pits in the earth, a board or other playing surface. The objective is usually to capture all or some set of the opponent's pieces. Versions of the game date back past the 3rd century and evidence suggests the game existed in Ancient Egypt. It is among the oldest known games to still be widely played today." ([Wikipedia](https://en.wikipedia.org/wiki/Mancala))

## How to start the game

1. Clone this repository.
2. Run `make game/start`.
3. Go to [localhost:8080](http://localhost:8080).

## How to play

Mancala is a two-player board game in which the players take turns to sow seeds (stones) from their pits into the board's pits.  
The goal of the game is to capture more seeds than the opponent.

* The basic game board consists of two rows of six pits, and a Kalah (larger pit) on each end. Each player owns one row of pits and the corresponding Kalah.
* At the beginning of the game, four seeds are placed in each pit.
* In each turn, a player takes all the seeds from any of their pits and sows them counterclockwise (one seed in each pit) into the board's pits. Players alternate turns in a counterclockwise direction.
* If the last seed lands in an empty pit on the player's side, and the opposite pit on the opponent's side has seeds, then the player captures all the seeds from the opponent's pit and adds them to their Kalah.
* Additionally, if the last seed lands in the player Kalah, the player gets an extra turn.
* The game ends when a player can no longer make a move (all of their pits are empty). The remaining seeds on the board are added to each player's Kalah.
* The player with the most seeds in their Kalah at the end of the game wins.

## Project structure

The project is structured in two main folders:
* `server/` -> contains the game logic and the server socket API.
* `web/` -> contains the web application front-end.

## Developer instructions

Each folder is a separately poetry project. You'll find more about the technical implementation in each folder's readme.  
Run `make setup` inside each folder to setup your local development environment.  
This command will also install the pre-commit hooks used to guarantee code standards.  
After that, you can run `poetry shell` to start a shell session with the environment configured.
