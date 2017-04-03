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
