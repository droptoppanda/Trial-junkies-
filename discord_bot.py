
import os
import discord
from discord.ext import commands
from trial_request_agent import TrialRequestAgent
from profile_generation_agent import ProfileGenerationAgent
from credential_generation_agent import CredentialGenerationAgent
from trial_execution_agent import TrialExecutionAgent
from verification_agent import VerificationAgent
from subscription_verification import verify_subscription

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')

@bot.command()
async def trial(ctx, platform: str):
    try:
        # Initial response
        status_msg = await ctx.send("🔄 Processing trial request...")
        
        # Verify subscription
        is_active, _, sub_details = verify_subscription(str(ctx.author.id))
        if not is_active:
            await status_msg.edit(content="❌ Active subscription required for trial creation")
            return
            
        if sub_details.get('trials_remaining', 0) <= 0:
            await status_msg.edit(content="❌ No trials remaining in current subscription")
            return

        # Generate credentials
        await status_msg.edit(content="🔄 Generating credentials...")
        cred_agent = CredentialGenerationAgent()
        email = cred_agent.generate_email()
        phone = cred_agent.generate_phone()
        card = cred_agent.generate_card()

        # Generate profile
        profile_agent = ProfileGenerationAgent()
        profile = profile_agent.generate_profile()
        profile.update({
            'email': email,
            'phone': phone,
            'card': card
        })

        # Execute trial
        await status_msg.edit(content="🔄 Creating trial account...")
        trial_agent = TrialExecutionAgent(platform, os.getenv('WEBDRIVER_PATH'))
        success = trial_agent.execute_trial(profile, {}, ctx.author.id, True)

        if success:
            # Send success message in channel
            await status_msg.edit(content=f"✅ Trial created successfully!\nPlatform: {platform}")
            
            # Send private details via DM
            try:
                dm_content = f"""
Your trial credentials:
Platform: {platform}
Email: {profile['email']}
Password: {profile.get('password', 'defaultpass123')}
Card: {card[-4:]} (last 4 digits)
"""
                await ctx.author.send(dm_content)
            except discord.Forbidden:
                await ctx.send("⚠️ Couldn't send private details. Please enable DMs from server members.")

        else:
            await status_msg.edit(content="❌ Failed to create trial account")

    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

def run_bot():
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        raise ValueError("Discord bot token not found")
    bot.run(token)

if __name__ == "__main__":
    run_bot()
