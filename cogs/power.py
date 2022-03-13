import discord
from discord.ext import commands
import json
import os
import random
import re
import sys

from typing import List, Dict, Union, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from clogger import clogger
from split_text import split_text


def strip_tags(string):
    """
    This function will strip all html tags from string returning the inner html text using regex only.
    """
    return re.sub('<.*?>', '', string)

class PowerSearch(commands.Cog):
    """Power Cog"""

    def __init__(self, bot):
        self.bot = bot

        
    @commands.command(aliases=["powers"])
    async def power(self, ctx, *, name: str):
        """Searches for a power in the database."""        
        search_message = await ctx.send(f"```Searching for power: `{name}`...```")

        # Load the database.
        with open("/home/dev/Code/powerswikia/powers.json", "r") as f:
            powers = json.load(f)

        # Search for the power in the database.
        for power in powers:
            # If the name is found, send an embed with the power's information.
            try:
                akas_lower = [p.lower() for p in power["attributes"]["also_called"]]
            except Exception as e:
               akas_lower = []

            clogger(akas_lower)

            if name.lower() == power["name"].lower() or name.lower() in akas_lower:
                # Create an embed with the power's information.
                img_path = power["image"]
                image_path = f"/home/dev/Code/powerswikia/{img_path}"
                print(image_path)
                description = None
                quote_string_list = []
                if len(power["quotes"]):
                    for quote_list in power["quotes"]:
                        quote = strip_tags(quote_list[0].replace("<br>","\n"))
                        author = strip_tags(quote_list[1])
                        work = strip_tags(quote_list[2])

                        quote_string_list.append(f"**\"{quote}\"**\n\t```*-{author}, ({work})*```")

                description = power["description"] + "\n\n" + "\n".join(quote_string_list)
                
                embed = discord.Embed(title=power["name"], url=power["url"], description=description)
                if image_path:
                    embed.set_image(url=f"attachment://{image_path}")
                send_list = [embed,]
                
                # Add all of the attributes to the embed.
                # for attribute in power["attributes"]:
                #     if power["attributes"][attribute]:
                #         # Create a string to add all of the values to.
                #         value = ""
                #         # Add each value to the string and separate them by a comma and space.
                #         attr_embed = discord.Embed(title=attribute.title().replace("_", " "), url=power["url"])
                #         for v in power["attributes"][attribute]:
                #             if len(v):
                #                 attr_embed.add_field(name="\u200b", value=v, inline=False)
                #         send_list.append(attr_embed)

                # Send the embeds and return out of the function.
                await search_message.delete()
                for idx, e in enumerate(send_list):
                    if idx == 0:
                        if image_path:
                            await ctx.send(file=discord.File(image_path), embed=e)
                        else:
                            await ctx.send(embed=e)
                    else:
                        await ctx.send(embed=e)
                return

        # If no power is found, send an error message and return out of the function.
        await ctx.send(f"```No power called `{name}` was found.```", delete_after=5.0)

    @commands.command(aliases=["randompowers"])
    async def randompower(self, ctx):  # TODO: Add a random power command.
        """Sends a random power from the database."""
        await ctx.send(f"```Searching for a random power...```", delete_after=5.0)

        # Load the database.
        with open("/home/dev/Code/powerswikia/powers.json", "r") as f:
            powers = json.load(f)

        # Get a random power from the database and send an embed with it's information.
        random_power = powers[random.randint(0, len(powers))]
        img_path = random_power["image"]
        image_path = f"/home/dev/Code/powerswikia/{img_path}"
        description = None
        quote_string_list = []
        if len(random_power["quotes"]):
            for quote_list in random_power["quotes"]:
                quote = strip_tags(quote_list[0].replace("<br>","\n"))
                author = strip_tags(quote_list[1])
                work = strip_tags(quote_list[2])

                quote_string_list.append(f"**\"{quote}\"**\n\t```*-{author}, ({work})*```")

        description = "\n\n\n".join(quote_string_list)

        # Get a random power from the database and send an embed with it's information.
        e = discord.Embed(title=random_power["name"], url=random_power["url"], description=description)
        if image_path:
            e.set_image(url=f"attachment:/{image_path}")
            await ctx.send(file=discord.File(image_path), embed=e)
        else:
            await ctx.send(embed=e)

def setup(client):
    client.add_cog(PowerSearch(client))