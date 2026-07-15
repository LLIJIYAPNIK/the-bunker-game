# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Bunker** is a game engine for running sessions of the "Bunker" board game (eventually surfaced via Telegram + a web admin interface, neither of which exists yet). The repository currently contains only the domain/game-engine layer — there is no UI, API, persistence, or Telegram integration code.

The engine's core architectural rule: `app/domain` must never depend on Telegram, Flask, a database, an ORM, or HTTP. All such systems are meant to be adapters built on top of the engine later. See `doc/00-vision.md` for the full rationale and `doc/02-business-rules.md` (BR-S1) for the constraint.

Design/requirements docs live in `doc/`:
- `doc/00-vision.md` — goals, principles, MVP scope
- `doc/01-glossary.md` — domain terminology (Game, Lobby, Round, Voting, Bunker, Character, etc.)
- `doc/02-business-rules.md` — numbered business rules (BR-*), including a section of rules still open for clarification
- `doc/03-state-model.md` — authoritative state machines and transitions for Game, Participant, Character, Voting, Round
- `doc/use_cases/` — per-feature use case specs (lobby: UC-L1..L4, gameplay: UC-G1..G7)

When implementing or changing domain logic, check these docs for the relevant business rule or state transition rather than inferring behavior purely from existing code — the docs are the spec.

## Commands

This project uses `uv` for dependency management.

```bash
uv sync --all-extras --dev       # install dependencies (incl. dev group: pytest, ruff, pyright, pre-commit)

uv run pytest                    # run the full test suite
uv run pytest tests/unit/lobby/test_lobby.py            # run one test file
uv run pytest tests/unit/lobby/test_lobby.py::test_add_participant   # run one test

uv run ruff check .              # lint
uv run ruff check . --fix        # lint with autofix
uv run ruff format .             # format
uv run ruff format --check .     # format check only (used in CI)

uv run pyright                   # type check
```

CI (`.github/workflows/ci.yml`) runs, in order: `ruff check`, `ruff format --check`, `pyright`, `pytest`. Pre-commit (`.pre-commit-config.yaml`) runs `ruff-check --fix`, `ruff-format`, `pyright`, and `pytest` locally on commit — mirror all four before considering a change done.

Ruff line length is 79 chars, target `py313`; lint rules enabled: `E`, `F`, `I` (isort), `UP` (pyupgrade), `B` (bugbear). Pyright runs in `standard` mode over `app` and `tests`.

## Architecture

### Domain module layout

Each subpackage under `app/domain/` follows the same internal shape:
- `entity.py` — the main class(es) with behavior and state transitions
- `state.py` — `Enum`s for the entity's states (`auto()`-valued)
- `exceptions.py` — a package-local error hierarchy rooted at that package's own base error (e.g. `LobbyError`, `GameError`, `VotingError`), which itself extends `app.domain.exceptions.DomainError`
- `__init__.py` — re-exports the public surface via explicit `__all__`; other packages *only* import through this, e.g. `from app.domain import bunker, round` or `from app.domain.game import Game, ParticipantState`, never `from app.domain.game.entity import Game`

When adding a new domain error, put it in that package's `exceptions.py` under the right subclass of the package's base error, and add it to `__init__.py`'s imports and `__all__`.

### Domain packages and how they compose

- `user` — `User` (telegram_id, username), independent of game state.
- `character` — `Character`: a plain dataclass of attributes (age, profession, health, etc.) attached to a participant.
- `game.participant` — `Participant`: wraps a user identifier + `Character`, tracks `ParticipantState` (READY/UNREADY).
- `bunker` — `Bunker[T]` (generic over participant type) holds a `BunkerProfile` (capacity, `Catastrophe`, `Condition`s, `TimeToOutYears`) built via `BunkerProfileBuilder`. Represents where surviving participants end up.
- `voting` — `Voting[T]`: generic ballot over voters/targets for one vote. Tracks `voted`/`votes` dicts and `VotingState` (OPEN → COUNTING → FINISHED, or → REVOTE on a tie via `restart()`). Returns a `VotingResult` when everyone has voted.
- `round` — `Round[T]`: one discussion+voting cycle. Owns a `Voting` instance, exposes `start_voting()` and `cast_vote()`, and returns a `RoundResult` once voting resolves to a single winner (delegating ties back into `Voting.restart()`).
- `lobby` — `Lobby`: pre-game waiting room. Holds participants, enforces `Lobby.MIN_PLAYERS` (currently 4, per official Bunker rules — see BR-003), tracks readiness (`ParticipantState`) and `LobbyState` (WAITING → READY → STARTED, or CLOSED). `start_game(game)` constructs/starts a `Game`; `finish_game()` reads results back off the `Game` once it's FINISHED.
- `game` — `Game`: the aggregate root for an active session (see `doc/01-glossary.md`'s "Aggregate Root"). Owns `active_participants`/`excluded_participants`, the current `active_round`, and the `bunker`. Drives the round loop internally: `start()` kicks off the first `Round`; `cast_vote()` delegates to the active round and, when a round produces a `RoundResult`, moves the eliminated participant into `excluded_participants` and either starts the next round or `_finish()`es the game once the remaining participant count matches the bunker's capacity. `GameState` is WAITING → RUNNING → FINISHED.

Control flow for a full game is therefore: `Lobby` gates entry and readiness → `Lobby.start_game()` creates and starts a `Game` → `Game` creates `Round`s → each `Round` creates a `Voting` → results bubble back up (`VotingResult` → `RoundResult` → participant exclusion in `Game` → eventual `Game._finish()` which populates the `Bunker` with winners) → `Lobby.finish_game()` retrieves winners once `Game.is_finished`.

Several classes (`Bunker`, `Voting`, `Round`) are generic (`class Foo[T]`, PEP 695 syntax, py313+) over the participant type rather than importing `Participant` directly, keeping them reusable independent of the concrete `game.Participant` type.

### Tests

- `tests/unit/<package>/` mirrors `app/domain/<package>/`, one test module per entity (e.g. `tests/unit/lobby/test_lobby.py` for `app/domain/lobby/entity.py`).
- `tests/unit/conftest.py` holds shared fixtures (`players`, `player`, `bunker`) built from `tests/factories/participant.py`'s `make_participant()` factory (which supplies a default `Character`).
- `tests/integration/` exists for cross-aggregate/full-flow tests but is currently empty.
- Tests directly poke `entity.state = SomeState.X` to set up preconditions before asserting on a transition/guard, rather than always driving through the public API — follow this pattern when it's the more direct way to reach a state.
- `pyproject.toml` sets `pythonpath = ["."]`, so tests import via the full `app.domain...` / `tests.factories...` paths.
