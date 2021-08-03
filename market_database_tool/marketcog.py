import market_database_tool
from discord.ext import commands
import raia

class MarketCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(name='checkitem')
	async def checkitem(self, ctx, item_name_arg):
		check = raia.player_system.get_player_by_id(ctx.author.id)
		if check == None:
			await ctx.send(f"Hello there {ctx.author.mention} you cannot use any other commands because you are not yet in the game, type \"r/budgetme \" to get started.")
			return
		item = raia.market_system.get_item_by_name(str(item_name_arg))
		await ctx.send(f"item id : {item.item_id}\nitem name : {item.item_name}\nitem price :  {item.item_price}")
		return
	

	@commands.command(name='shop')
	async def shop(self, ctx):
		check = raia.player_system.get_player_by_id(ctx.author.id)
		if check == None:
			await ctx.send(f"Hello there {ctx.author.mention} you cannot use any other commands because you are not yet in the game, type \"r/budgetme \" to get started.")
			return
		raia.market_system.cache_items()
		msg = ""
		for hasht in raia.market_system.list_all_items():
			msg+=hasht
		if msg == "":
			await cts.send("Item not found.")
		else:
			await ctx.send(msg)


	@commands.command(name='buy')
	async def buy(self, ctx, item_name, qntty=1):
		check = raia.player_system.get_player_by_id(ctx.author.id)
		if check == None:
			await ctx.send(f"Hello there {ctx.author.mention} you cannot use any other commands because you are not yet in the game, type \"r/budgetme \" to get started.")
			return
		elif qntty > 100:
			await ctx.send("the max item quantity is 100.")
			return


		check_item = raia.market_system.get_item_by_name(str(item_name))
		if check_item != None:
			total = int(check_item.item_price) * int(qntty)
			gold = raia.player_system.get_player_by_id(int(ctx.author.id)).player_gold
			if gold >= total: 
				raia.player_system.by_id_deduct_player_gold(int(ctx.author.id), total)
				await ctx.send(f"{ctx.author.mention} bought {qntty} {check_item.item_name} for {total} gold.")
			else:
				await ctx.send(f"{ctx.author.mention} you don't have enough wealth.")
		else:
			return


	@commands.command(name='sell')
	async def sell(self, ctx, item_name, qntty=1):
		check = raia.player_system.get_player_by_id(ctx.author.id)
		if check == None:
			await ctx.send(f"Hello there {ctx.author.mention} you cannot use any other commands because you are not yet in the game, type \"r/budgetme \" to get started.")
			return
		elif qntty < 0:
			await ctx.send("cannot sell at given amount.")
			return
		
		""""Item selling here"""


def setup(bot):
	bot.add_cog(MarketCommands(bot))