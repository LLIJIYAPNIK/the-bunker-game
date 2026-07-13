# UC-G5 — Eliminate Player

## Actors
- System

## Preconditions
- A player has been selected for elimination.

## Main Scenario
1. The character is marked as ELIMINATED.
2. The player is transferred to OBSERVER.
3. The game state is updated.

## Alternative Scenarios
- A1: The player is already eliminated → ignored.

## Postconditions
- The player no longer participates in the active phase of the game.
