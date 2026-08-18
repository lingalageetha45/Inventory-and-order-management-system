from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.repositories import notification as notification_repository


def list_notifications(
    db: Session,
    user_id: int,
) -> list[Notification]:
    return notification_repository.get_notifications(
        db,
        user_id,
    )


def get_notification(
    db: Session,
    notification_id: int,
    user_id: int,
) -> Notification:
    notification = notification_repository.get_notification_by_id(
        db,
        notification_id,
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    if notification.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot access this notification",
        )

    return notification


def create_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str,
) -> Notification:
    if not title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Notification title cannot be empty",
        )

    if not message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Notification message cannot be empty",
        )

    notification = Notification(
        user_id=user_id,
        title=title.strip(),
        message=message.strip(),
        is_read=False,
    )

    return notification_repository.create_notification(
        db,
        notification,
    )


def mark_notification_as_read(
    db: Session,
    notification_id: int,
    user_id: int,
) -> Notification:
    notification = get_notification(
        db,
        notification_id,
        user_id,
    )

    if not notification.is_read:
        notification.is_read = True

        db.commit()
        db.refresh(notification)

    return notification 