import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from trial_execution_agent import TrialExecutionAgent
from profile_generation_agent import ProfileGenerationAgent
from credential_generation_agent import CredentialGenerationAgent
from verification_agent import VerificationAgent
from subscription_verification import verify_subscription

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

@bot.command(name="trial")
async def create_trial(ctx, service_url: str):
    """Create a trial account for the specified service"""
    try:
        # Verify subscription
        is_active, _, sub_details = verify_subscription(str(ctx.author.id))
        if not is_active:
            await ctx.send("❌ Active subscription required for trial creation")
            return

        if sub_details.get('trials_remaining', 0) <= 0:
            await ctx.send("❌ No trials remaining in current subscription")
            return

        # Generate profile
        profile_agent = ProfileGenerationAgent()
        profile = profile_agent.generate_profile()

        # Execute trial
        trial_agent = TrialExecutionAgent(service_url, os.getenv('WEBDRIVER_PATH'))
        result = trial_agent.execute_trial(profile, {}, discord_user_id=str(ctx.author.id))

        if result["status"] == "success":
            # Send public confirmation
            await ctx.send("✅ Trial created successfully! Check your DMs for login details.")

            # Send private details
            dm_message = (
                "🎉 **Trial Account Created!**\n"
                f"**Service:** {service_url}\n"
                f"**Email:** {profile['email']}\n"
                f"**Password:** {profile.get('password', 'Check email for password')}\n"
                "\n⚠️ Keep these details safe and private!"
            )
            try:
                await ctx.author.send(dm_message)
            except discord.Forbidden:
                await ctx.send("⚠️ Couldn't send private details. Please enable DMs from server members.")
        else:
            await ctx.send(f"❌ Trial creation failed: {result.get('error', 'Unknown error')}")

    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command(name="balance")
async def check_balance(ctx):
    """Check remaining trials in subscription"""
    try:
        is_active, is_trial, sub_details = verify_subscription(str(ctx.author.id))
        if not is_active:
            await ctx.send("❌ No active subscription found")
            return

        trials_left = sub_details.get('trials_remaining', 0)
        await ctx.send(f"🎫 Trials remaining: {trials_left}")
    except Exception as e:
        await ctx.send(f"❌ Error checking balance: {str(e)}")

def run_bot():
    bot.run(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    run_bot()