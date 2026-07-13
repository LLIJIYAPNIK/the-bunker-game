# 01 — Glossary

## Game

A game session that combines participants, gameplay, game state, and related game objects.

---

## Lobby

The waiting phase for players before the start of a session.

---

## Player

A user of the system participating in a specific game session.

The player controls a character, makes decisions, and participates in voting.

---

## Character

An in-game character belonging to a player.

The character contains a game set of characteristics used when making decisions during the session.

---

## Character Attribute

Any characteristic of a character.

For example:

* profession;
* age;
* health;
* hobby;
* item;
* biological traits;
* additional skills.

---

## Card

A game object describing one characteristic of a character or the game world.

---

## Card Template

A description of a game card used when generating characters.

It is part of the game content.

---

## Deck

A set of game cards used by the generator when creating a session.

---

## Bunker

A description of the shelter the players are striving to get into.

It contains parameters that affect the gameplay.

---

## Catastrophe

A global event that led to the need to use the bunker.

Determines the game context of the session.

---

## Round

A completed stage of the game, including discussion, voting, and results processing.

---

## Vote

The process of choosing a player who must be eliminated from the game.

---

## Revote

A repeated vote held when there is no clear result from the previous vote.

---

## Observer

A player eliminated from active gameplay.

An observer does not take part in voting, but can receive information about the progress of the session in accordance with the rules of the game.

---

## Host

The creator of the game room.

Before the start of the session, they have the right to start the game.

---

## Game State

The current state of the game session.

Example states:

* WAITING
* RUNNING
* FINISHED

---

## Vote State

The current state of voting.

Example states:

* CREATED
* OPEN
* FINISHED
* REVOTE

---

## Character State

The current state of the character.

Example states:

* ALIVE
* ELIMINATED

---

## Game Engine

The central business logic of the project.

Manages the game's lifecycle, coordinates game processes, and ensures adherence to the rules.

---

## Game Content

A set of game data used by the engine.

Includes:

* cards;
* professions;
* diseases;
* items;
* characteristics;
* catastrophe scenarios;
* bunker parameters.

---

## Use Case

A system usage scenario describing the achievement of a specific user goal without implementation details.

---

## Aggregate

A group of interconnected domain objects modified as a single unit.

---

## Aggregate Root

The main entity of the aggregate, through which changes to the rest of the aggregate objects are made.

In the game domain, the aggregate is the game session, and its root is `Game`.
