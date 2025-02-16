import discord

class RoleManager:
    def __init__(self, guild):
        self.guild = guild

    async def assign_role(self, user, role_name):
        role = discord.utils.get(self.guild.roles, name=role_name)
        if role:
            await user.add_roles(role)

    async def revoke_role(self, user, role_name):
        role = discord.utils.get(self.guild.roles, name=role_name)
        if role:
            await user.remove_roles(role)
