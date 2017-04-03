# kitsuchan-ng

A small, modular Discord bot. There's a lot of stuff that can be improved, but it's easy to add
functions to it.

This bot uses the `rewrite` branch of `discord.py`. Install that and not the regular one.

# How to run
Just run `kitsuchan.py`. On first run, the bot will prompt you for a Discord OAuth token.

`kitsuchan-ng` reads and saves its config to and from the file config.json.
This file will be created upon startup. The following parameter is MANDATORY:

* `OAUTH_TOKEN_DISCORD` - OAuth token for your Discord bot account.

Optionally, you may set the following as well:

* `API_KEY_IBSEARCH` - API key for IbSear.ch. You can get one for free with no registration.
  The `ibsearch` command will refuse to run without this.
* `COMMAND_PREFIX` - Override the command prefix with anything of your liking.
* `WHITELIST_NSFW` - This contains a list of channel IDs for which NSFW content may be posted.
* `EXTENSIONS` - This overrides the bot's default extension list.

# How to use
By default, `kitsuchan-ng` uses `kit!` for its prefix where `kit` are the first three letters of
the bot account's username. You can override this.

# Supported commands (not complete)

* `help` - Display help information.
* `info` - Display info about the bot itself.
* `guildinfo` - Display info about the current guild.
* `channnelinfo` - Display info about the current channel.
* `userinfo <mention>` - Display info about the mentioned user.
* `echo <text>` - Repeat the user's text back at them.
* `duckduckgo <list of terms>` - Fetch Instant Answer from DuckDuckGo. This is probably the most
  useful command the bot has right now, due to the high versatility of the Instant Answers API.
* `ibsearch <list of tags>` - Search IbSear.ch for anime pictures.
* `halt` - Halt the bot. Only the bot's owner can do this.
* `restart` - Restart the bot. Only the bot's owner can do this.
