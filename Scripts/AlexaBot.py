import urllib.request as urllib

import discord
import os

from discord.ext import commands

clientTag = ''  # the client tag of your bot user
botGame = ''  # change this to the game that should be displayed in discord for the bot
opusPath = ''  # the path of the opus library

if not discord.opus.is_loaded():
    discord.opus.load_opus(opusPath)

ytdl_opts = {'ignoreerrors': True,
             'noplaylist': True,
             'format': 'bestaudio/best',
             'postprocessors': [{
                 'key': 'FFmpegExtractAudio',
                 'preferredcodec': 'mp3',
                 'preferredquality': '192',
             }]}


class Bot:
    def __init__(self, client):
        self.client = client
        self.player = None
        self.server = None

    async def on_message(self, message):
        if message.content == 'this is so sad':
            voice_channel = message.author.voice.voice_channel
            self.server = message.server
            channel = message.channel
            song = ['despacito']
            if voice_channel:
                if not self.client.voice_client_in(self.server):
                    await self.play_song(song, voice_channel, channel)
                else:
                    await self.client.send_message(channel, 'im already playing')
            else:
                await self.client.send_message(channel, "you haven't joined a voice channel jet")

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *args):
        voice_channel = ctx.message.author.voice.voice_channel
        self.server = ctx.message.server
        channel = ctx.message.channel
        if voice_channel:
            if not self.client.voice_client_in(self.server):
                await self.play_song(args, voice_channel, channel)
            else:
                await self.client.send_message(channel, 'im already playing')
        else:
            await self.client.send_message(channel, "you haven't joined a voice channel jet")

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        if self.player and self.player.is_playing():
            self.player.stop()
            voice = self.client.voice_client_in(self.server)
            await voice.disconnect()
            await self.client.send_message(ctx.message.channel, 'stopped playing')
        else:
            await self.client.send_message(ctx.message.channel, 'im currently not playing anything')

    @commands.command(pass_context=True, no_pm=True)
    async def disconnect(self, ctx):
        if not self.disconnect_voice():
            await self.client.send_message(ctx.message.channel, "i haven't joined a voice channel jet")

    async def play_song(self, args, voice_channel, text_channel):
        song = '+'.join(args)
        print(song)
        song_file = '../MP3s/' + song + '.mp3'
        if os.path.isfile(song_file):
            voice = await self.client.join_voice_channel(voice_channel)
            self.player = voice.create_ffmpeg_player(song_file, after=self.disconnect_voice)
            self.player.volume = 0.3
            self.player.start()
            await self.client.send_message(text_channel, 'playing ' + song)
        else:
            link = song
            if link.find('youtu.be') > -1 or link.find('www.youtube.com') > -1:
                await self.play_song_yt(link, voice_channel, text_channel)
            else:
                link = self.search_yt_video(song)
                await self.play_song_yt(link, voice_channel, text_channel)
                await self.client.send_message(text_channel, link)

    async def play_song_yt(self, link, voice_channel, text_channel):
        try:
            voice = await self.client.join_voice_channel(voice_channel)
            self.player = await voice.create_ytdl_player(link, ytdl_options=ytdl_opts, after=self.disconnect_voice)
            self.player.volume = 0.3
            self.player.start()
            await self.client.send_message(text_channel, 'playing ' + self.player.title)
        except Exception as error:
            print('ERROR IN: ' + str(error.__traceback__.tb_lineno))
            print(error.args)
            await self.client.send_message(text_channel, "I can't play this link: " + link)
            self.disconnect_voice()

    def disconnect_voice(self):
        voice = self.client.voice_client_in(self.server)
        if voice:
            self.client.loop.create_task(voice.disconnect())
            return True
        else:
            return False

    @staticmethod
    def search_yt_video(link):
        response = urllib.urlopen('https://www.youtube.com/results?search_query=' + link)
        html = str(response.read())
        link_location = html.find('<a aria-hidden="true"  href="/watch?v=')
        return 'https://www.youtube.com/watch?v=' + html[link_location + 38:link_location + 49]


client = commands.Bot(command_prefix='alexa ')
client.add_cog(Bot(client))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name=botGame))


client.run(clientTag)
