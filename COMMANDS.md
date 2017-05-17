# List of commands
* Note 1: Some of these commands are in the [Kitsuchan-NG-cogs](https://github.com/n303p4/Kitsuchan-NG-cogs) repo.
* Note 2: This file was automatically generated and may look bad.

## 8ball
### Aliases: eightball
Ask the Magic 8-Ball a question.

* question - The question to ask. Must end in a ?

## anagram
Find possible anagrams of a phrase.

* text = The message to find an anagram for.

## antigravity
Fetch the antigravity comic from xkcd.

## archnews
### Aliases: anews
Fetch the latest Arch Linux news.

## atbash
Convert text using a reversed alphabet.

* text = The message to be encoded.

## avatar
Display a user's avatar.
Defaults to displaying the avatar of the user who invoked the command.

* user - A member who you can mention for avatar.

## ban
Ban all users mentioned by this command.

Requires both the user and bot to have `ban_members` to execute.

## base64
Convert a phrase into Base64.

* text = The text to convert.

## block
Blocking commands (e.g. block user).

Only the bot owner can use this.

## boots
Boots!

## c2f
Convert temperature in Celsius to Fahrenheit.

* temperature - An integer representing temperature in Celsius.

## catgirl
### Aliases: neko, nekomimi
Find a random cat-eared person.

## censor
### Aliases: clean
Delete the bot's previous message(s). Bot owner only.

* times - Number of message to delete. Defaults to 1.

## cgames
### Aliases: games
List all games currently being played in the current guild.

* page_number - Optional parameter if there are too many pages.

## channelinfo
### Aliases: cinfo
Display information about a channel channel.
Defaults to the current channel.

* channel - Optional argument. A specific channel to get information about.

## choose
Choose between one of various supplied things.

Syntax:

* choose x, y, z - Choose between x, y, and z.

## coin
### Aliases: cflip, coinflip
Flip a coin.

## cry
Cry!

## cuddle
### Aliases: snuggle
Cuddle a member!

* member - The member to be cuddled.

## danbooru
### Aliases: dbooru, db
Shortcut command to search Danbooru through IbSear.ch.

* tags - A list of tags to be used in the search criteria.

## dead
### Aliases: rip
Dead!

## define
Define a word.

* word - A word to be looked up.

## didsay
Checks if a user said a particular phrase.

* user - A member to mention.
* phrase - A phrase to check against. Leave blank to show all instances.

## discrim
### Aliases: discriminator
Find all users in the current guild with a given discriminator.

* discriminator - A discriminator to search for.

## echo
### Aliases: say
Repeat the user's text back at them. Bot owner only.

* text - A string to be echoed back.

## eval
Evaluate a Python expression. Bot owner only.

## f2c
Convert temperature in Fahrenheit to Celsius.

* temperature - An integer representing temperature in Fahrenheit.

## fdesk
### Aliases: facedesk
Facedesk!

## fortune
Produce a random fortune. :3

## foxgirl
### Aliases: kitsune, kitsunemimi
Find a random fox-eared person.

## from
Subcommands that decode plaintext. (e.g. from binary)

## gelbooru
### Aliases: gbooru, gb
Shortcut command to search Gelbooru through IbSear.ch.

* tags - A list of tags to be used in the search criteria.

## ghelp
Generate a file listing currently loaded commands. Bot owner only.

## glomp
### Aliases: tacklehug, tackle
Glomp!

## google
### Aliases: g
Search Google. Optional image and news arguments.

Example queries:

* google A cat - Search Google for a cat.
* google image A cat - Search Google for an image of a cat.

## guildinfo
### Aliases: ginfo, serverinfo, sinfo
Display information about the current guild, such as owner, region, emojis, and roles.

## halt
### Aliases: shutdown, kys
Halt the bot. Only the bot owner can use this.

## help
### Aliases: commands
Shows this message.

## hug
Hug a member!

* member - The member to be hugged.

## ibsearch
### Aliases: ib, ibs
Fetch a randomized anime image from IbSear.ch, optional tags.

* tags - A list of tags to be used in the search criteria.

This command accepts common imageboard tags and keywords. Here are a few examples:

* ib red_hair armor - Search for images tagged with `red_hair` and `armor`.
* ib red_hair | armor - Search for images tagged with `red_hair` or `armor`.
* ib red_hair -armor - Search for images tagged with `red_hair` and not `armor`.
* ib 1280x1024 - Search for images that are 1280x1024.
* ib 5:4 - Search for images in 5:4 aspect ratio.
* ib random: - You don't care about what you get.

## idk
### Aliases: idek
IDK!

## info
### Aliases: botinfo, binfo, about
Display bot info, e.g. library versions.

## invite
Generate an invite link for this bot.

## jisho
Translates Japanese to English, and English to Japanese.
Works with Romaji, Hiragana, Kanji, and Katakana.

## kat
### Aliases: kats, kitkat, kitkats
Search Google Images.

## kick
Kick all users mentioned by this command.

Requires both the user and bot to have `kick_members` to execute.

## kiss
Kiss a member!

* member - The member to be kissed.

## kon
### Aliases: konkon
Kon, kon!

## konachan
### Aliases: kchan, kwp
Shortcut command to search Konachan through IbSear.ch.

* tags - A list of tags to be used in the search criteria.

## lewd
Lewd!

## lick
Lick a member!

* member - The member to be licked.

## liste
Display list of currently-enabled bot extensions.

Only the bot owner can use this.

## listg
### Aliases: listguilds
List all guilds that the bot is in. Bot owner only.

## lmlu
### Aliases: lmly, letmeloveyou
Let me love you!

## load
### Aliases: loade
Enable the use of an extension.

Only the bot owner can use this.

## makepoll
Create a Straw Poll.

Example usage:

kit makepoll "Name of poll" "Option 1" "Option 2" Option3

## mods
### Aliases: moderators
Display moderators for the given channel.

Assumes that members with `manage_messages`, `kick_members`, and `ban_members` are mods.

## nom
Nom!

## nyan
### Aliases: nya, meow
Nyan!

## owo
owo

## pat
Pat a member!

* member - The member to be patted.

## ping
### Aliases: bang, bang!, beep, beep!, pong
Ping the bot.

## poke
Poke!

## pokedex
### Aliases: dex
This is the list of pokemon queries you can perform.

## pout
Pout!

## purge
### Aliases: prune
Purge a certain number of messages from the channel.

Requires both the user and bot to have `manage_messages` to execute.

## quote
Quote a user.

* user - The user you wish to quote.

## rename
Change the bot's username. Bot owner only.

## restart
Restart the bot. Only the bot owner can use this.

## reverse
Reverse input text.

## rload
### Aliases: reload, rloade
Reload an already-loaded extension.

Only the bot owner can use this.

## rname
### Aliases: randomname
Generate a random name.

## rng
### Aliases: randint
Randomly generate a number. Default range 1-100.

* start - Specify the starting number of the range.
* end - Specify the ending number of the range.

## roll
Roll some dice, using D&D syntax.

Examples:
* roll 5d6 - Roll five six sided dice.
* roll 1d20 2d8 - Roll one twenty sided die, and two eight sided dice.

## rot13
Convert a phrase into ROT13.

* text = The text to convert.

## rule34
### Aliases: r34
Shortcut command to search Rule34 through IbSear.ch.

* tags - A list of tags to be used in the search criteria.

## rwg
### Aliases: rword, randword
Randomly generate a word.

## safebooru
### Aliases: sbooru, sb
Shortcut command to search Safebooru through IbSear.ch.

* tags - A list of tags to be used in the search criteria.

## sandwich
Sandwich!

## set
Change a value in the bot's settings.

## sh
Execute a system command. Bot owner only.

## sha3
Convert a phrase into its SHA-3 hash.

* text = The text to convert.

## slap
Slap a member!

* member - The member to be slapped.

## smug
Smug!

## stare
Stare at a member!

* member - The member to be stared at.

## sudo
Fetch the sudo comic from xkcd.

## tickle
Tickle a member!

* member - The member to be tickled.

## to
Subcommands that encode plaintext. (e.g. to binary)

## triggered
Triggered!

## uload
### Aliases: unload, uloade
Disable the use of an extension.

Only the bot owner can use this.

## unblock
### Aliases: ublock
Unblocking commands (e.g. unblock user).

Only the bot owner can use this.

## userinfo
### Aliases: uinfo
Display information about a user, such as status and roles.
Defaults to the user who invoked the command.

* user - Optional argument. A user in the current channel to get user information about.

## usermeme
### Aliases: um, standard
Create a meme of a user. Use quotes around your arguments.

Example usage:

* kit usermeme "This is" "A meme"
* kit usermeme "This is" "A meme" @Kitsuchan

## wag
### Aliases: tailwag
Tail wag!

## wanted
### Aliases: poster
Create a wanted poster of a user.

Example usage:

* kit wanted
* kit wanted @Kitsuchan

## what
What?

## whoplays
### Aliases: playing
List all members in the current guild playing a game.

* game_name - The game to be checked.

## wiki
### Aliases: wikipedia
Search Wikipedia.

* query - A list of strings to be used in the search criteria.

## wlol
### Aliases: idu, ideu, wakarimasenlol
Wakarimasen, lol!

## xbooru
### Aliases: xb
Shortcut command to search Xbooru through IbSear.ch.

* tags - A list of tags to be used in the search criteria.

## xkcd
### Aliases: xk
Fetch a comic from xkcd.

* comic_id - A desired comic ID. Leave blank for latest comic. Set to r for a random comic.

## yandere
### Aliases: yd
Shortcut command to search Yande.re through IbSear.ch.

* tags - A list of tags to be used in the search criteria.