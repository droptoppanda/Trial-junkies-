
import discord

class RoleManager:
    def __init__(self, guild):
        self.guild = guild

    def assign_role(self, user, role_name):
        role = discord.utils.get(self.guild.roles, name=role_name)
        if role:
            user.add_roles(role)

    def revoke_role(self, user, role_name):
        role = discord.utils.get(self.guild.roles, name=role_name)
        if role:
            user.remove_roles(role)
