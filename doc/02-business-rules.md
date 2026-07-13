# 02 — Business Rules

## General System Rules

### BR-001 — Single Active Game
A player can participate in only one active game at a time.

---

### BR-002 — Game States
The game can only be in one of the following states:
- WAITING
- RUNNING
- FINISHED

Transitions between states must be validated by the system.

---

### BR-003 — Minimum Number of Players
The game cannot be started if the number of players is less than a specified minimum.

(The value is determined by the game configuration)

---

### BR-004 — Starting a Game
The game can only be started from the WAITING state.

---

## Lobby

### BR-L1 — Joining a Game
A player can only join a game in the WAITING state.

---

### BR-L2 — Participant Uniqueness
A single player can only be added to a game once.

---

### BR-L3 — Entry Prohibition After Start
After the game transitions to RUNNING, new players cannot join.

---

### BR-L4 — Host Permissions
Only the Host can start the game.

---

### BR-L5 — Loss of Host
If the Host leaves the game before it starts:
- the Host role is transferred to another player
- or the game is terminated (the decision is deferred to the implementation of a configuration rule)

---

## Gameplay

### BR-G1 — World Generation
The game world (bunker, catastrophe, characters) is generated only once per game.

---

### BR-G2 — Character Belongs to Game
A Character exists only in the context of a specific Game.

---

### BR-G3 — Character Reveal
After a player is eliminated, their character is fully revealed to all participants.

---

### BR-G4 — Irrevocability
An eliminated player cannot return to the active game.

---

## Voting

### BR-V1 — One Vote
A player can only cast one vote per voting round.

---

### BR-V2 — Prohibition of Self-Voting
A player cannot vote for themselves.

---

### BR-V3 — Immutability of Vote (MVP)
After submission, a vote cannot be changed.

---

### BR-V4 — End of Voting
Voting ends when:
- all living players have voted
OR
- the timer has expired (if included in the configuration)

---

### BR-V5 — Result Determination
The player with the maximum number of votes is eliminated.

---

### BR-V6 — Tie
In the event of a tie:
- a revote is initiated (REVOTE)

---

### BR-V7 — Inability to Vote Outside of Phase
Voting is only possible in the OPEN voting state.

---

## Player Elimination

### BR-E1 — Finality of Elimination
The elimination of a player is irreversible.

---

### BR-E2 — Transfer to Observers
An eliminated player becomes an OBSERVER.

---

### BR-E3 — Observer Activity
An Observer cannot participate in voting.

---

## Game Completion

### BR-F1 — Completion Condition
The game is completed when:
- the minimum number of players remains
OR
- the bunker's victory scenario is fulfilled

---

### BR-F2 — Final State
After transitioning to FINISHED, the game becomes immutable.

---

## Content Generation

### BR-C1 — Content Source
All characteristics (professions, diseases, bunkers) are taken from the Game Content.

---

### BR-C2 — No Generation "Out of Thin Air"
The system cannot create characteristics outside of the predefined content.

---

### BR-C3 — Character Uniqueness
Each Character within a single game must be unique in their set of key characteristics (if balance mode is enabled).

---

## System Constraints

### BR-S1 — Engine Independence
The game engine does not depend on:
- Telegram
- Web API
- Database
- ORM

---

### BR-S2 — Atomicity of Changes
Any change to the game state must be atomic.

---

### BR-S3 — Game History
All key game events must be recorded (event log / audit trail).

---

## Open Rules (Require Clarification)

### BR-O1 — Behavior upon Host Departure during Game
Not defined:
- role transfer
- or game termination

---

### BR-O2 — Voting Timer
Not defined:
- whether a timer is used by default

---

### BR-O3 — Displaying Characteristics to Players
Not defined:
- whether all characteristics are visible immediately
- or are revealed gradually

---

### BR-O4 — Game Modes
Not defined:
- one standard mode
- or several game modifiers
