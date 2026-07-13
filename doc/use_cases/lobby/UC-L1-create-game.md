# UC-L1 — Create Game

## Actors
- Player (Host)

## Preconditions
- The player is not currently in an active game.

## Main Scenario
1. The player initiates game creation.
2. The system creates a game session.
3. The system assigns the player as the host.
4. The system transitions the game to the `WAITING` state.
5. The system generates a lobby code.
6. The system returns the game data.

## Alternative Scenarios
- A1: The player is already in a game → creation denied.
- A2: Error generating lobby code → retry attempt.

## Postconditions
- Game object is created.
- Host is assigned.
- State: `WAITING`.
