from typing import List
from fastapi import Depends
from app.config.constants import RoleName
from app.core.exceptions import PermissionDeniedException

class RoleChecker:
    def __init__(self, allowed_roles: List[RoleName]):
        self.allowed_roles = [r.value if isinstance(r, RoleName) else str(r) for r in allowed_roles]

    def __call__(self, user_role: str) -> bool:
        if user_role not in self.allowed_roles:
            raise PermissionDeniedException(f"Role '{user_role}' is not authorized to perform this operation.")
        return True
