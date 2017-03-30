# kitsuchan-ng
A fairly good Discord bot, hopefully.

# How to set up
Set up the following environment variables:

* `API_KEY_DISCORD_KITSUCHAN` - This is the OAuth token for your bot's account.
* `API_KEY_IBSEARCH_KITSUCHAN` - This is the API key for IbSear.ch. You can easily get one for
  free with no registration needed, so there's no excuse for you not to get one.
* `WHITELIST_ADMINS_KITSUCHAN` - This contains a list of user IDs that can restart and halt the bot.

Optionally, set up the following as well:

* `WHITELIST_NSFW_KITSUCHAN` - This contains a list of channel IDs for which NSFW content may be
  posted.

Once you have these set up, simply run `kitsuchan.py` and the bot will wake up. The program will
*not run* unless the first three variables are set up.

# How to use
By default, `kitsuchan-ng` uses `kit!` for its prefix where `kit` are the first three letters of
the bot account's username.

# Supported commands

* `help` - Display help information.
* `info me` - Display info about the bot itself.
* `info server` - Display info about the current server.
* `info channnel` - Display info about the current channel.
* `info user <mention>` - Display info about the mentioned user.
* `duckduckgo <list of terms>` - Fetch Instant Answer from DuckDuckGo.
* `ibsearch <list of tags>` - Search IbSear.ch for anime pictures.
* `halt` - Halt the bot. The user who issues the command must have their ID listed in
  `WHITELIST_ADMINS_KITSUCHAN`.
* `restart` - Restart the bot. The user who issues the command must have their ID listed in
  `WHITELIST_ADMINS_KITSUCHAN`.
