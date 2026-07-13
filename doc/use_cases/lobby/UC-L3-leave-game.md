# UC-L3 — Leave Game

## Actors
- Player

## Preconditions
- The player is in a game.

## Main Scenario
1. The player initiates leaving.
2. The system removes the player from the game.
3. The system updates the lobby state.
4. The system checks the impact on the game.

## Alternative Scenarios
- A1: The player is the Host → requires processing role transfer or game termination.
- A2: The game has already started → the player becomes an observer.

## Postconditions
- The player is removed or transferred to OBSERVER.
