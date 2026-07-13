# 00 — Vision

## Project

**Bunker** is a platform for playing the "Bunker" board game in Telegram with web interface administration capabilities.

The project implements a game engine, game scenario generation, and gameplay management independent of the user interface.

---

# Project Goal

To develop an extensible game engine that allows running "Bunker" game sessions with minimal involvement from a game master.

The system should automatically:

* create game rooms;
* manage the game lifecycle;
* distribute game characteristics;
* conduct voting;
* determine game results;
* provide tools for game content administration.

---

# Core Principles

## Game Engine Independence

Game logic does not depend on Telegram, a web interface, or a database.

Any interface must use the same game engine.

---

## Extensibility

The architecture should allow adding:

* new character characteristics;
* new game modes;
* new voting rules;
* new types of cards;
* new methods for game session analysis.

Without changing existing business logic.

---

## Maintainability

Each module is responsible for only one area of responsibility.

Changes in one subsystem should have minimal impact on others.

---

## Testability

Key business logic must be covered by automated tests.

The game engine must be testable independently of Telegram and the web interface.

---

# Target Audience

The main audience of the project:

* groups of friends;
* organizers of gaming events;
* board game masters;
* educational events;
* gaming communities in Telegram.

---

# Key MVP Features

## Lobby

* creating a game;
* connecting players;
* leaving a game;
* starting a session.

---

## Gameplay

* generation of game characteristics;
* conducting game rounds;
* conducting voting;
* eliminating players;
* completing a session.

---

## Administration

* managing game cards;
* managing characteristics;
* configuring game parameters.

---

# Future Version Features

* player statistics;
* player ratings;
* session history;
* session analysis using LLM;
* recommendations for optimal decisions;
* multiple game modes;
* editor for custom card sets;
* import and export of game sets;
* public REST API.

---

# Architectural Constraints

The game engine must not depend on:

* Telegram API;
* Flask;
* PostgreSQL;
* ORM;
* HTTP.

All external systems are adapters on top of the game engine.

---

# MVP Success Criteria

The project is considered ready for the first version if it allows:

1. creating a game;
2. registering players;
3. automatically assigning characteristics;
4. conducting a full session;
5. determining the winners;
6. completing the game without the participation of a game master.
