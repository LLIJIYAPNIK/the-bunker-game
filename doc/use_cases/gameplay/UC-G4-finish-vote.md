# UC-G4 — Finish Voting

## Actors
- System

## Preconditions
- Voting has completed.

## Main Scenario
1. The system counts the votes.
2. Determines the player with the most votes.
3. Eliminates the player.
4. Reveals the character.
5. Checks game completion conditions.

## Alternative Scenarios
- A1: Tie → revote.
- A2: End of game → transition to FINISHED.

## Postconditions
- Players are updated.
- Game state is updated.
