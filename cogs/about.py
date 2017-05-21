#!/usr/bin/env python3

# Standard modules
import datetime
import resource
import sys

# Third party modules
import discord
from discord.ext import commands

# Bundled modules
import app_info
import helpers
import settings

class About:
    """Commands that display information about the bot, user, etc."""

    @commands.group(aliases=["botinfo", "binfo", "about"], invoke_without_command=True)
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def info(self, ctx):
        """Display bot info, e.g. library versions."""
        
        uptime = str(datetime.datetime.now() - ctx.bot.time_started).split(".")[0]
        
        embed = discord.Embed()
        embed.description = ctx.bot.description
        
        if not helpers.has_scanning(ctx):
            embed.set_thumbnail(url=ctx.bot.user.avatar_url_as(format="png", size=128))
        else:
            embed.set_footer(text="Thumbnail omitted on this channel due to image scanning.")
        
        embed.add_field(name="Version", value=app_info.VERSION_STRING)
        
        ainfo = await ctx.bot.application_info()
        owner = ainfo.owner.mention
        embed.add_field(name="Owner", value=owner)
        
        support_guild = settings.manager.get("SUPPORT_GUILD", "")
        if len(support_guild) > 0:
            embed.add_field(name="Support guild", value=support_guild)
        
        num_guilds = len(ctx.bot.guilds)
        num_users = len(list(filter(lambda member: not member.bot, ctx.bot.get_all_members())))
        embed.add_field(name="Serving", value=f"{num_users} people in {num_guilds} guilds")
        
        embed.add_field(name="Uptime", value=uptime)
        embed.add_field(name="Python", value="{0}.{1}.{2}".format(*sys.version_info))
        embed.add_field(name="discord.py", value=discord.__version__)
        
        usage_memory = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000, 2)
        embed.add_field(name="Cookies eaten", value=f"{usage_memory} megabites")
        
        await ctx.send(embed=embed)
    
    @commands.command(brief="Display guild (server) info.", aliases=["ginfo", "serverinfo", "sinfo"])
    @commands.guild_only()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def guildinfo(self, ctx):
        """Display information about the current guild, such as owner, region, emojis, and roles."""
        
        guild = ctx.guild
        
        embed = discord.Embed(title=guild.name)
        embed.description = guild.id
        
        if not helpers.has_scanning(ctx):
            embed.set_thumbnail(url=guild.icon_url)
        else:
            embed.set_footer(text="Thumbnail omitted on this channel due to image scanning.")
        
        embed.add_field(name="Owner", value=guild.owner.name)
        
        num_humans = helpers.count_humans(guild)
        embed.add_field(name="Humans", value=num_humans)
        
        num_bots = helpers.count_bots(guild)
        embed.add_field(name="Bots", value=num_bots)
        
        embed.add_field(name="Text channels", value=len(guild.text_channels))
        embed.add_field(name="Voice channels", value=len(guild.voice_channels))
        embed.add_field(name="Custom emojis", value=len(guild.emojis) or None)
        embed.add_field(name="Roles", value=len(guild.roles)-1 or None)
        embed.add_field(name="Region", value=str(guild.region))
        embed.add_field(name="Created at", value=guild.created_at.ctime())
        
        await ctx.send(embed=embed)

    @commands.command(brief="Display channel info.", aliases=["cinfo"])
    @commands.guild_only()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def channelinfo(self, ctx, *, channel:discord.TextChannel=None):
        """Display information about a text channel.
        Defaults to the current channel.
        
        * channel - Optional argument. A specific channel to get information about."""
        
        # If channel is None, then it is set to ctx.channel.
        channel = channel or ctx.channel
        
        embed = discord.Embed(title=f"{channel.name}")
        
        try:
            embed.description = channel.topic
        except AttributeError:
            pass
        
        embed.add_field(name="Channel ID", value=channel.id)
        
        try:
            embed.add_field(name="Guild", value=channel.guild.name)
        except AttributeError:
            pass
        
        embed.add_field(name="Members", value=len(channel.members))
        embed.add_field(name="Created at", value=channel.created_at.ctime())
        
        if channel.is_nsfw():
            embed.set_footer(text="NSFW content is allowed for this channel.")
        
        await ctx.send(embed=embed)
    
    @commands.command(brief="Display voice channel info.", aliases=["vcinfo"])
    @commands.guild_only()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def vchannelinfo(self, ctx, *, channel:discord.VoiceChannel):
        """Display information about a voice channel.
        
        * channel - A specific voice channel to get information about."""
        
        embed = discord.Embed(title=f"{channel.name}")
        embed.add_field(name="Channel ID", value=channel.id)
        try:
            embed.add_field(name="Guild", value=channel.guild.name)
        except AttributeError:
            pass
        embed.add_field(name="Bitrate", value=f"{channel.bitrate}bps")
        if channel.user_limit > 0:
            user_limit = channel.user_limit
        else:
            user_limit = None
        embed.add_field(name="User limit", value=user_limit)
        embed.add_field(name="Created at", value=channel.created_at.ctime())
        await ctx.send(embed=embed)
    
    @commands.command(brief="Display user info.", aliases=["uinfo"])
    @commands.guild_only()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def userinfo(self, ctx, *, user:discord.Member=None):
        """Display information about a user, such as status and roles.
        Defaults to the user who invoked the command.
        
        * user - Optional argument. A user in the current channel to get user information about."""
        
        # If user is None, then it is set equal to ctx.author.
        if not user:
            user = ctx.author
        
        title = f"{user.name}#{user.discriminator}"
        embed = discord.Embed(title=title)
        embed.color = user.color
        
        if user.game:
            embed.description = f"Playing **{user.game}**"
        
        if not helpers.has_scanning(ctx):
            embed.set_thumbnail(url=user.avatar_url_as(format="png", size=128))
        else:
            embed.set_footer(text="Thumbnail omitted on this channel due to image scanning.")
        
        embed.add_field(name="User ID", value=user.id)
        embed.add_field(name="Nickname", value=user.nick)
        embed.add_field(name="Bot user?", value="Yes" if user.bot else "No")
        status = user.status.name.capitalize() if user.status.name != "dnd" else "Do Not Disturb"
        embed.add_field(name="Status", value=status)
        embed.add_field(name="Joined guild at", value=user.joined_at.ctime())
        embed.add_field(name="Joined Discord at", value=user.created_at.ctime())
        roles = ", ".join((role.name for role in user.roles if not role.is_default()))[:1024]
        embed.add_field(name="Roles", value=roles, inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(brief="Display role info.", aliases=["rinfo"])
    @commands.guild_only()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def roleinfo(self, ctx, *, role:discord.Role):
        """Display information about a role.
        
        * role - The role to display information about."""
        
        embed = discord.Embed(title=role.name)
        embed.color = role.color
        embed.description = role.id
        
        embed.add_field(name="Create instant invite", value=role.permissions.create_instant_invite)
        embed.add_field(name="Kick members", value=role.permissions.kick_members)
        embed.add_field(name="Ban members", value=role.permissions.ban_members)
        embed.add_field(name="Administrator", value=role.permissions.administrator)
        embed.add_field(name="Manage channels", value=role.permissions.manage_channels)
        embed.add_field(name="Manage guild", value=role.permissions.manage_guild)
        embed.add_field(name="Add reactions", value=role.permissions.add_reactions)
        embed.add_field(name="View audit logs", value=role.permissions.view_audit_logs)
        embed.add_field(name="Read messages", value=role.permissions.read_messages)
        embed.add_field(name="Send messages", value=role.permissions.send_messages)
        embed.add_field(name="Send TTS messages", value=role.permissions.send_tts_messages)
        embed.add_field(name="Manage messages", value=role.permissions.manage_messages)
        embed.add_field(name="Embed links", value=role.permissions.embed_links)
        embed.add_field(name="Attach files", value=role.permissions.attach_files)
        embed.add_field(name="Read message history", value=role.permissions.read_message_history)
        embed.add_field(name="Mention everyone", value=role.permissions.mention_everyone)
        embed.add_field(name="External emojis", value=role.permissions.external_emojis)
        embed.add_field(name="Connect to voice channel", value=role.permissions.connect)
        embed.add_field(name="Speak in voice channel", value=role.permissions.speak)
        embed.add_field(name="Mute members", value=role.permissions.mute_members)
        embed.add_field(name="Deafen members", value=role.permissions.deafen_members)
        embed.add_field(name="Move members", value=role.permissions.move_members)
        embed.add_field(name="Use voice activation", value=role.permissions.use_voice_activation)
        embed.add_field(name="Change nickname", value=role.permissions.change_nickname)
        embed.add_field(name="Manage nicknames", value=role.permissions.manage_nicknames)
        
        embed2 = discord.Embed()
        embed2.color = role.color
        embed2.add_field(name="Manage roles", value=role.permissions.manage_roles)
        embed2.add_field(name="Manage webhooks", value=role.permissions.manage_webhooks)
        embed2.add_field(name="Manage emojis", value=role.permissions.manage_emojis)
        
        await ctx.send(embed=embed)
        await ctx.send(embed=embed2)

    @commands.command(brief="Display emoji info.", aliases=["einfo"])
    @commands.guild_only()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def emojiinfo(self, ctx, *, emoji:discord.Emoji):
        """Display information for a custom emoji.
        
        * emoji - The emoji to get information about."""
        
        embed = discord.Embed(title=emoji.name)
        embed.description = f"{emoji.id} | [Full image]({emoji.url})"
        
        embed.add_field(name="Guild", value=f"{emoji.guild.name} ({emoji.guild.id})")
        embed.add_field(name="Managed", value=emoji.managed)
        embed.add_field(name="Created at", value=emoji.created_at.ctime())
        
        if not helpers.has_scanning(ctx):
            embed.set_thumbnail(url=emoji.url)
        else:
            embed.set_footer(text="Thumbnail omitted on this channel due to image scanning.")
        
        await ctx.send(embed=embed)

def setup(bot):
    """Setup function for About."""
    bot.add_cog(About())
