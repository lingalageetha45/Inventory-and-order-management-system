from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.notification import Notification


def get_notification_by_id(
    db: Session,
    notification_id: int,
) -> Notification | None:
    return db.get(Notification, notification_id)


def get_notifications(
    db: Session,
    user_id: int,
) -> list[Notification]:
    return db.scalars(
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
    ).all()


def create_notification(
    db: Session,
    notification: Notification,
) -> Notification:
    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


def mark_as_read(
    db: Session,
    notification: Notification,
) -> Notification:
    notification.is_read = True
    db.commit()
    db.refresh(notification)

    return notification