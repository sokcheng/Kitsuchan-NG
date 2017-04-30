# List of commands
* Note 1: Some of these commands are in the [Kitsuchan-NG-cogs](https://github.com/n303p4/Kitsuchan-NG-cogs) repo.
* Note 2: This file was automatically generated and may look bad.

## 8ball
### Aliases: eightball
Ask the Magic 8-Ball a question.

* question - The question to ask. Must end in a ?

## about
### Aliases: a, info, i
Information subcommands, e.g. channel information.

## antigravity
Fetch the antigravity comic from xkcd.

## avatar
Display a user's avatar.
Defaults to displaying the avatar of the user who invoked the command.

* user - A member who you can mention for avatar.

## ban
Ban all users mentioned by this command.

Requires both the user and bot to have `ban_members` to execute.

## block
Blocking commands (e.g. block user).

Only the bot owner can use this.

## boots
Boots!

## censor
### Aliases: clean
Delete the bot's previous message(s). Bot owner only.

* times - Number of message to delete. Defaults to 1.

## cgames
Shows the currently most played games

## choose
Choose between one of various supplied things.

Syntax:

* choose x | y | z - Choose between x, y, and z.

## coin
### Aliases: cflip, coinflip
Flip a coin.

## cry
Cry!

## cuddle
### Aliases: snuggle
Cuddle a member!

* member - The member to be cuddled.

## dead
Dead!

## didsay
Checks if a user said a particular phrase.

* user - A member to mention.
* phrase - A phrase to check against. Leave blank to show all instances.

## discrim
### Aliases: discriminator
Find all users with a given discriminator.

* discriminator - A discriminator to search for.

## echo
### Aliases: say
Repeat the user's text back at them. Bot owner only.

* text - A string to be echoed back.

## eval
Evaluate a Python expression. Bot owner only.

## fdesk
### Aliases: facedesk
Facedesk!

## from
Subcommands that decode plaintext. (e.g. from binary)

## ghelp
Generate a file listing currently loaded commands. Bot owner only.

## glomp
### Aliases: tacklehug, tackle
Glomp!

## google
### Aliases: g
Search the web with Google.

Example usage:
* google a cat - Google search for a cat.
* google image a cat - Google image search for a cat.
* google maps a cat - Google maps search for a cat.

Originally made by Kowlin https://github.com/Kowlin/refactored-cogs, edited by Aioxas.

Modified to work with Kitsuchan-NG.

## halt
### Aliases: shutdown, kys
Halt the bot. Only the bot owner can use this.

## help
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
* ib red_hair -armor - Search for images tagged with `red_hair` and not `armor`.
* ib 1280x1024 - Search for images that are 1280x1024.
* ib 5:4 - Search for images in 5:4 aspect ratio.
* ib random: - You don't care about what you get.

## invite
Generate an invite link for this bot.

## jisho
Translates Japanese to English, and English to Japanese.
Works with Romaji, Hiragana, Kanji, and Katakana.

## kick
Kick all users mentioned by this command.

Requires both the user and bot to have `kick_members` to execute.

## kiss
Kiss a member!

* member - The member to be kissed.

## kon
### Aliases: konkon
Kon, kon!

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
### Aliases: bang, bang!, pong
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

## rwg
### Aliases: rword, randword
Randomly generate a word.

## sandwich
Sandwich!

## sh
Execute a system command. Bot owner only.

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

## what
What?

## whoplays
Shows a list of all the people playing a game.

## wiki
### Aliases: wikipedia
Search Wikipedia.

* query - A list of strings to be used in the search criteria.

## wlol
### Aliases: wakarimasenlol
Wakarimasen, lol!

## xkcd
### Aliases: xk
Fetch a comic from xkcd.

* comic_id - A desired comic ID. Leave blank for latest comic. Set to r for a random comic.