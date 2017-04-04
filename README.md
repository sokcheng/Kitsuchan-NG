# kitsuchan-ng

A small, modular Discord bot. There's a lot of stuff that can be improved, but it's easy to add
functions to it.

This bot uses the `rewrite` branch of `discord.py`. Install that and not the regular one.

# Isn't this basically similar in concept to Twentysix26's Red bot? Why not just use that?

It *is* basically similar. In fact, I recommend you use Red instead of `kitsuchan-ng` if you need
something that's actually meant for serious work. Red has a far larger library of extensions, its
codebase is more mature, and it has a good community of people behind it. `kitsuchan-ng` by
contrast is a young, unproven bot with an unstable API and no community.

So, if Red exists, why did I make this bot? Simple, it's for fun. I also made it because I hope to
improve my own coding skills as it's being built. `kitsuchan-ng` is released as open-source for
ideological reasons, and in hopes that perhaps someone else will find it useful, too.

# How to run
To install the `rewrite` branch of `discord.py`, run the following:

```python3 -m pip install -U git+https://github.com/Rapptz/discord.py@rewrite```

Then just run `kitsuchan.py`. On first run, the bot will prompt you for a Discord OAuth token.

# How to configure

`kitsuchan-ng` reads and saves its config to and from the file `config.json`. This file will be
created automatically upon startup. The following parameter in the config is **mandatory**:

* `OAUTH_TOKEN_DISCORD` - OAuth token for your Discord bot account.

Optionally, you may set the following as well:

* `API_KEY_IBSEARCH` - API key for IbSear.ch. You can get one for free with no registration.
  The `ibsearch` command will refuse to run without this.
* `COMMAND_PREFIX` - Override the command prefix with anything of your liking.
* `WHITELIST_NSFW` - This contains a list of channel IDs for which NSFW content may be posted.
  Channel IDs are stored as SHA-512 hashes.
* `EXTENSIONS` - This overrides the bot's default extension list.

In the future, one objective of mine is to implement per-cog settings.

By default, `kitsuchan-ng` uses `kit!` for its prefix where `kit` are the first three letters of
the bot account's username. You can override this with the aforementioned `COMMAND_PREFIX`
parameter.
