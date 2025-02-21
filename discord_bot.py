import os
import discord
from discord.ext import commands
from trial_request_agent import TrialRequestAgent
from profile_generation_agent import ProfileGenerationAgent
from credential_generation_agent import CredentialGenerationAgent
from subscription_verification import verify_subscription # Retaining this for subscription check


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')

@bot.command()
async def trial(ctx, platform: str):
    try:
        await ctx.send("Generating trial account...")

        # Verify subscription - adapted from original code
        is_active, _, sub_details = verify_subscription(str(ctx.author.id))
        if not is_active:
            await ctx.send("❌ Active subscription required for trial creation")
            return

        if sub_details.get('trials_remaining', 0) <= 0:
            await ctx.send("❌ No trials remaining in current subscription")
            return


        profile_agent = ProfileGenerationAgent()
        profile = profile_agent.generate_profile()

        trial_agent = TrialRequestAgent(platform)
        result = trial_agent.initiate_trial_creation()

        await ctx.send(f"Trial created successfully!\nPlatform: {platform}\nEmail: {profile['email']}\nPassword: Generated and sent to DM")
        try:
            await ctx.author.send(f"Your trial credentials:\nEmail: {profile['email']}\nPassword: {profile.get('password', 'defaultpass123')}")
        except discord.Forbidden:
            await ctx.send("⚠️ Couldn't send private details. Please enable DMs from server members.")

    except Exception as e:
        await ctx.send(f"Error creating trial: {str(e)}")

def run_bot():
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        raise ValueError("Discord bot token not found")
    bot.run(token)

if __name__ == "__main__":
    run_bot()