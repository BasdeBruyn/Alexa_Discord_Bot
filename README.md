# Discord_Alexa_Bot
Discord bot that plays music when you ask alexa to do so

## Requirements
* a discord bot user
* python 3.5 or higher
* discord.py[voice] module installed
* ffmpeg installed with open-ssl enabled
* the opus library if you're not running it on windows
* youtube-dl module installed

## Setup
To set the bot up change the **clientTag**, **botGame** and **opusPath** fields to your situation.  
If you play the same song all the time you can download it as an mp3 and put it the **MP3s** folder so it doesn't have to download it every time.

## Usage
* The command prefix for alexa is _"alexa "_ so for her to play something you type _"alexa play **song**"_ and she will play it in the voice channel you're in.
* To stop her playing type _"alexa stop"_.  
* If something goes wrong and alexa is still in the voicechannel type _"alexa disconnect"_.  
* And just for the memes if you type _"this is so sad"_ she plays despacito.

## Maintenance
Because I mostly wrote this for myself, I won't be that active on this repository. If you have any problems I probably can't help you, but these are some things that I have encountered with an easy fix:
* If alexa says _"I can't play this link"_  with almost every youtube song or link, try to update youtube-dl _(pip install -U youtube-dl)_. This happens becasue youtube regularly updates their video player and youtrube-dl has to keep up with those changes.
* If the python script keeps crashing with a network error, it's probably because your internet sometimes cuts out too long. A simpel fix that I found is to run the python script in an endless loop via a bash or batch script, this will try to restart the bot untill it has a connection again. I know this is a bit dirty but i couldn't find a more reliable option.