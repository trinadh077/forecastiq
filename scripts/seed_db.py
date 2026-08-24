import asyncio
import sys
import os

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.database.session import async_session_factory
from app.models import Role, Organization, User
from app.core.security import get_password_hash
from app.config.constants import RoleName

async def seed_database():
    print("Seeding database initial records...")
    async with async_session_factory() as session:
        # 1. Admin Role
        admin_role = Role(
            id="role-admin-001",
            name=RoleName.ADMIN,
            description="Super Administrator",
            permissions_json={"all": True}
        )
        session.add(admin_role)

        # 2. Sample Organization
        org = Organization(
            id="org-default-001",
            name="Acme Revenue Corp",
            slug="acme-corp",
            domain="acme.com"
        )
        session.add(org)

        # 3. Initial Admin User
        user = User(
            id="user-admin-001",
            email="admin@forecastiq.com",
            hashed_password=get_password_hash("Admin123!"),
            full_name="System Administrator",
            is_superuser=True,
            organization_id=org.id,
            role_id=admin_role.id
        )
        session.add(user)

        await session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_database())
