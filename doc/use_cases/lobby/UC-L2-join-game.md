# UC-L2 — Join Game

## Actors
- Player

## Preconditions
- The game exists.
- The game is in the `WAITING` state.

## Main Scenario
1. The player enters the lobby code.
2. The system finds the game.
3. The system checks if it is possible to join.
4. The system adds the player to the game.
5. The system updates the participant list.

## Alternative Scenarios
- A1: Lobby not found.
- A2: Game has already started.
- A3: Lobby is full.
- A4: Player is already in the game.

## Postconditions
- The player is added to GameParticipants.
