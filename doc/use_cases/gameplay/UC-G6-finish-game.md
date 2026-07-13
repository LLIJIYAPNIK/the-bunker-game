# UC-G6 — Finish Game

## Actors
- System

## Preconditions
- The game completion condition is met.

## Main Scenario
1. The system determines the remaining players.
2. Forms the results.
3. Transitions the game to FINISHED.
4. Closes active processes.

## Alternative Scenarios
- A1: All players left → forced completion.

## Postconditions
- The game is finished.
- Statistics are saved.
