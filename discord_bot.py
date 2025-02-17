import discord
from discord.ext import commands
from verification_agent import VerificationAgent
from trial_execution_agent import TrialExecutionAgent
import os

class TrialBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verification_agent = VerificationAgent()
        self.trial_execution_agent = TrialExecutionAgent(platform_url="http://example.com", webdriver_path="/path/to/chromedriver")

    @commands.command(name='start_trial')
    async def start_trial(self, ctx, profile_name):
        profile = {"name": profile_name, "trial_created": False}
        form_fields = {"name": profile_name}  # Example form fields
        try:
            self.verification_agent.verify_trial_creation(profile)
            result = self.trial_execution_agent.execute_trial(profile, form_fields)
            await ctx.send(result)
        except ValueError as e:
            await ctx.send(str(e))

bot = commands.Bot(command_prefix='!')
bot.add_cog(TrialBot(bot))

# Use environment variable for the bot token
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
