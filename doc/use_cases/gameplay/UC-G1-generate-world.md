# UC-G1 — Generate Game World

## Actors
- System

## Preconditions
- The game is in the `RUNNING` state.

## Main Scenario
1. The system selects a bunker.
2. The system selects a catastrophe.
3. The system generates a set of characteristics.
4. The system creates characters for players.
5. The system saves the game context.

## Alternative Scenarios
- A1: Insufficient content → generation is aborted.

## Postconditions
- Characters are created.
- Bunker is created.
- GameContext is created.
