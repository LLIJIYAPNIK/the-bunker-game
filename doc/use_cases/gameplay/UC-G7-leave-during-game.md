# UC-G7 — Leave During Game

## Actors
- Player

## Preconditions
- The player is participating in the game.

## Main Scenario
1. The player initiates leaving.
2. The system checks the game phase.
3. Updates the player's status.
4. Transfers to OBSERVER if necessary.

## Alternative Scenarios
- A1: The player left during voting → the vote is annulled.
- A2: The player is the last active one → game finishes.

## Postconditions
- The player is eliminated or transferred to OBSERVER.
