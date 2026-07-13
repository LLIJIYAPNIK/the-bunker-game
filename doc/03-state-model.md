# 03 — State Model

## Purpose

The document describes the lifecycle of the main domain entities and the valid transitions between their states.

The State Model defines:

* valid states of entities;
* permitted transitions between states;
* events that initiate transitions.

---

# Game

## Description

Game manages the lifecycle of the game session.

## States

| State     | Description                                           |
| --------- | ----------------------------------------------------- |
| WAITING   | Waiting for players. The game has not yet started.    |
| RUNNING   | The game is active. Game rounds are being played.     |
| FINISHED  | The game is finished. State changes are not possible. |

## Transitions

| From    | To       | Event                             |
| ------- | -------- | --------------------------------- |
| WAITING | RUNNING  | Host starts the game              |
| RUNNING | FINISHED | Game completion condition met     |
| WAITING | FINISHED | Lobby is forcibly closed          |

---

# Game Participant

## Description

Game Participant reflects a user's participation in a specific game session.

A single user can participate in only one active game.

## States

| State     | Description                                                   |
| --------- | ------------------------------------------------------------- |
| ACTIVE    | Participating in the game.                                    |
| OBSERVER  | Observing the game after elimination or leaving.              |
| LEFT      | Has completely left the game session.                         |

## Transitions

| From     | To       | Event                                     |
| -------- | -------- | ----------------------------------------- |
| ACTIVE   | OBSERVER | Elimination based on voting results       |
| ACTIVE   | LEFT     | Voluntary exit before the game starts     |
| OBSERVER | LEFT     | Observer exit                             |

---

# Character

## Description

Character represents a player's in-game character.

## States

| State      | Description                             |
| ---------- | --------------------------------------- |
| ALIVE      | The character is participating in the game. |
| ELIMINATED | The character is eliminated from the game.  |

## Transitions

| From  | To         | Event               |
| ----- | ---------- | ------------------- |
| ALIVE | ELIMINATED | Voting completes    |

---

# Voting

## Description

Voting manages the process of selecting a player for elimination.

## States

| State    | Description                            |
| -------- | -------------------------------------- |
| OPEN     | Accepting player votes.                |
| COUNTING | Votes are being counted.               |
| REVOTE   | A repeated vote has been scheduled.    |
| FINISHED | Voting is completed.                   |

## Transitions

| From     | To       | Event                                                      |
| -------- | -------- | ---------------------------------------------------------- |
| OPEN     | COUNTING | All players have voted or the voting time has ended        |
| COUNTING | REVOTE   | A tie has been recorded                                    |
| COUNTING | FINISHED | The player to be eliminated has been determined            |
| REVOTE   | OPEN     | A repeated vote has started                                |

---

# Round

## Description

Round represents a single game cycle.

Each round consists of discussion and voting.

## States

| State      | Description                        |
| ---------- | ---------------------------------- |
| DISCUSSION | Players discuss the situation.     |
| VOTING     | Voting is open.                    |
| FINISHED   | The round is completed.            |

## Transitions

| From       | To       | Event               |
| ---------- | -------- | ------------------- |
| DISCUSSION | VOTING   | Voting begins       |
| VOTING     | FINISHED | Voting is completed |

---

# Bunker

## Description

Within the MVP, the Bunker object is immutable.

After generation, its state does not change.

---

# Character Profile

## Description

Character Profile represents a set of character characteristics.

The profile is created before the start of the game and remains unchanged until it ends.

Within the MVP, changes to character characteristics are not provided for.

---

# State Diagrams

```text
Game

WAITING
    │
    ▼
RUNNING
    │
    ▼
FINISHED
```

```text
Game Participant

ACTIVE
   │
   ├──────────────► LEFT
   │
   ▼
OBSERVER
   │
   ▼
LEFT
```

```text
Character

ALIVE
   │
   ▼
ELIMINATED
```

```text
Voting

OPEN
   │
   ▼
COUNTING
   │
   ├──────────────► FINISHED
   │
   ▼
REVOTE
   │
   ▼
OPEN
```

```text
Round

DISCUSSION
      │
      ▼
VOTING
      │
      ▼
FINISHED
```

---

# General Constraints

* An entity cannot be in multiple states simultaneously.
* Any transition between states must be validated by the game engine.
* Invalid transitions must result in a domain logic error.
* After reaching a final state (`FINISHED`, `ELIMINATED`, `LEFT`), a reverse transition is impossible unless otherwise specified by business rules.

---

# Require Clarification

* Can a participant reconnect to an already running game after a connection loss.
* Is the game administrator allowed to cancel a vote.
* Is a separate `PAUSED` state required for the game.
* Can there be multiple consecutive votes within a single round.
