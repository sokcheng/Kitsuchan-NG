# kitsuchan-ng

This bot uses the `rewrite` branch of `discord.py`. Install that and not the regular one.

# How to run
`kitsuchan-ng` reads its config from environment variables. The following key is **mandatory**:

* `OAUTH_TOKEN_DISCORD` - OAuth token for your Discord bot account.

Optionally, you may set the following as well:

* `API_KEY_IBSEARCH` - API key for IbSear.ch. You can get one for free with no registration. The `ibsearch` command will refuse to run without this.
* `COMMAND_PREFIX` - Override the command prefix with anything of your liking.
* `WHITELIST_NSFW` - This contains a list of channel IDs for which NSFW content may be posted.

To run the program, it's suggested you do something like:

`OAUTH_TOKEN_DISCORD=key1 API_KEY_IBSEARCH=key2 python3 kitsuchan.py`

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

# Licensing

`kitsuchan-ng` is released under the Creative Commons CC0 1.0 Universal Public Domain Dedication.
You may find the legal text [here](https://creativecommons.org/publicdomain/zero/1.0/legalcode).
