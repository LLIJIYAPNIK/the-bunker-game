# UC-L4 — Start Game

## Actors
- Host

## Preconditions
- The game is in the `WAITING` state.
- There are enough players to start.

## Main Scenario
1. The Host starts the game.
2. The system checks the start conditions.
3. The system fixes the roster of players.
4. The system transitions the game to `RUNNING`.
5. The system initiates game world generation.

## Alternative Scenarios
- A1: Not enough players.
- A2: The game is already running.
- A3: The initiator does not have permissions.

## Postconditions
- The game is active.
- The roster of players is fixed.
