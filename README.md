# Kitsuchan-NG

A small, modular, extensible Discord bot written in Python 3. There's a lot of stuff that can be
improved, but it's easy to add functions to it.

# How to run
You'll need Python 3.5 or higher, as Kitsuchan-NG is not compatible with Python 3.4 and below.
There are no plans to add support for older Python versions, as this would be a hassle for me.

You'll need the `rewrite` branch of `discord.py`, as Kitsuchan-NG does not support the stable
`async` version. Use `venv` if you need both branches installed at once. To install `rewrite`,
run the following command:

```python3 -m pip install -U git+https://github.com/Rapptz/discord.py@rewrite```

Then just run `kitsuchan.py`. On first run, the bot will prompt you for a Discord OAuth token.

# How to configure

Kitsuchan-NG reads and saves its config to and from the file `config.json`. This file will be
created automatically upon startup. The following parameter in the config is **mandatory**:

* `OAUTH_TOKEN_DISCORD` - OAuth token for your Discord bot account.

Optionally, you may set the following as well:

* `API_KEY_IBSEARCH` - API key for IbSear.ch. You can get one for free with no registration.
  The `ibsearch` command will refuse to run without this.
* `COMMAND_PREFIX` - Override the command prefix with anything of your liking.
* `EXTENSIONS` - This overrides the bot's default extension list.

For your convenience, a `config.json.example` file is provided. In the future, one objective of
mine is to implement per-cog settings.

By default, Kitsuchan-NG responds to mentions as its default command prefix. You can override this
with the aforementioned `COMMAND_PREFIX` parameter.
