from fastapi import Depends, HTTPException, status
from app.dependencies.auth import get_current_user
from app.models.user import User


def require_roles(*allowed_roles):
    def role_checker(
        current_user: User = Depends(get_current_user),
    ):
        user_role = current_user.role

        # Support enum and string role values
        role_value = (
            user_role.value
            if hasattr(user_role, "value")
            else user_role
        )

        allowed_values = [
            role.value if hasattr(role, "value") else role
            for role in allowed_roles
        ]

        if role_value not in allowed_values:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )

        return current_user

    return role_checker