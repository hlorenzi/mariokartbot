# mariokartbot

This is a [discord.py](https://github.com/Rapptz/discord.py) Discord bot
that simulates Mario Kart items and lets users hit one another for complete
chaos!

## Running

Create a `config.json` file in the same directory as the `main.py` file.
Place the following inside, and replace `None` values with your user-specific
strings. Check out the `config.py` file for other available settings.

```
{
    "bot_token": None,

    "emoji_yoshi": None,
    "emoji_itembox": None,
    "emoji_greenshell": None,
    "emoji_redshell": None,
    "emoji_banana": None
}
```

Run it as:

```
python3 main.py
```

## The Game

Each player has a set number of itemboxes, that work like currency.
They can spend some itemboxes to spawn an item to attack, or to
hold it behind their karts for protection. Itemboxes then regenerate
with time automatically.

Attack other players to lower their VR (Versus Rating). In the future,
the game will be able to display leaderboards of all active players.

Currently, the following commands are available:

- `=use ITEM` Use/Throw/Place down the given item. You must have enough
itemboxes in order to spawn the item! Substitute `ITEM` for one of the
following:
  - `b` **Banana Peel**: It's placed down on the track. When someone tries to
use a command or just merely messages the channel, there's a chance that
they will slip on scattered banana peels.
  - `gs` **Green Shell**: It's an immediate-hit attack item. It targets any
one of the users that messaged the channel recently, with the most recent
one being more likely to be targeted. Though, the shell's not very accurate,
and can miss its target, or even hit you back in the face!
  - `rs` **Red Shell**: It's a delayed-hit attack item. It targets the most
recent user that messaged the channel (that's not yourself). It only reaches
its target after a set amount of time, giving a chance for wary players to
defend themselves by holding an item behind their karts.

- `=hold ITEM` Holds the given item behind your kart for safety. Use the
same item codes from above. You must have enough itemboxes in order to
spawn the item!

- `=drop` Drops the currently-held item, activating its effect.

Currently, the bot can itself be target of items (mainly for testing
purposes). If you'd like the bot to hold a Banana Peel, use the debug
command `=bothold`.