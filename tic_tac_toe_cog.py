from collections import OrderedDict

import discord
from discord.ext import commands

import emojis

BOARD = [[":one:", ":two:", ":three:"], [":four:", ":five:", ":six:"], [":seven:", ":eight:", ":nine:"]]

NUMS_LIST = [
    ("one", emojis.encode(":one:")),
    ("two", emojis.encode(":two:")),
    ("three", emojis.encode(":three:")),
    ("four", emojis.encode(":four:")),
    ("five", emojis.encode(":five:")),
    ("six", emojis.encode(":six:")),
    ("seven", emojis.encode(":seven:")),
    ("eight", emojis.encode(":eight:")),
    ("nine", emojis.encode(":nine:"))
]
NUMS = OrderedDict(NUMS_LIST)


def format_board(board: list) -> str:
    output_board = "\n".join((" ".join((value for value in row))) for row in board)
    return output_board


class TicTacToeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.board = ""

    @commands.command(name="tictactoe")
    async def tic_tac_toe(self, ctx):
        self.board = format_board(BOARD)
        board = await ctx.send(self.board)
        for emoji in NUMS.values():
            await board.add_reaction(emoji)


