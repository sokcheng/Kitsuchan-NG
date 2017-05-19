#!/usr/bin/env python3


class Wallpapers:

    @commands.command(aliases=["bwp"])
    async def bingwp(self, ctx, number:int=None):
        """Query Bing for a wallpaper. Optional number of wallpapers."""
        logger.info("Querying Bing for wallpaper(s).")
        # The number of wallpapers desired.
        number = 1000
        # Random wallpaper bool.
        random_mode = True
        # If there are arguments...
        if len(args) > 0:
            # See if the last argument can be used as a number.
            if str(args[-1]).isdigit():
                number = int(args[-1])
                # Hard cap the limit at 8, which is the maximum allowed.
                if number > 8:
                    number = 8
                random_mode = False
            if args[-1].lower() == "random":
                pass
            elif args[-1].lower() in ("today", "latest", "current"):
                random_mode = False
                number = 1
        # Query Bing's JSON API.
        url = "https://www.bing.com/HPImageArchive.aspx?" +\
              "format=js&idx=0&n={number}&mkt=en-US" % (number,)
        # Grab the thing.
        async with ctx.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
            else:
                message = "Could not fetch URL."
                raise commands.UserInputError(message)
        # Nonrandom mode.
        if not random_mode:
            quote = []
            for index in range(len(data["images"])):
                url = "https://www.bing.com" + data["images"][index]["url"]
                quote.append(url)
            quote = "\n".join(quote)
        else:
            image = random.choice(data["images"])
            quote = "https://www.bing.com" + image["url"]
        await kitsuchan.say(quote)
