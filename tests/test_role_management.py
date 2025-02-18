import unittest
from unittest.mock import AsyncMock, MagicMock
from role_management import RoleManager

class TestRoleManager(unittest.TestCase):
    def setUp(self):
        self.guild = MagicMock()
        self.user = MagicMock()
        self.role_name = "test_role"
        self.role_manager = RoleManager(self.guild)

    def test_assign_role(self):
        role = MagicMock()
        self.guild.roles = [role]
        role.name = self.role_name
        self.user.add_roles = AsyncMock()

        self.role_manager.assign_role(self.user, self.role_name)
        self.user.add_roles.assert_called_with(role)

    def test_revoke_role(self):
        role = MagicMock()
        self.guild.roles = [role]
        role.name = self.role_name
        self.user.remove_roles = AsyncMock()

        self.role_manager.revoke_role(self.user, self.role_name)
        self.user.remove_roles.assert_called_with(role)

if __name__ == '__main__':
    unittest.main()
