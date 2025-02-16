import discord
from discord.ext import commands
from verification_agent import VerificationAgent

class TrialBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verification_agent = VerificationAgent()

    @commands.command(name='start_trial')
    async def start_trial(self, ctx, profile_name):
        profile = {"name": profile_name, "trial_created": False}
        try:
            self.verification_agent.verify_trial_creation(profile)
            await ctx.send(f"Trial successfully created for {profile_name}")
        except ValueError as e:
            await ctx.send(str(e))

bot = commands.Bot(command_prefix='!')
bot.add_cog(TrialBot(bot))

bot.run('YOUR_DISCORD_BOT_TOKEN')
