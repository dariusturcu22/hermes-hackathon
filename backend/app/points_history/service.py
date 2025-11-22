from sqlalchemy.orm import Session
from .model import PointsHistory
from .schema import PointsHistoryCreate, PointsHistoryUpdate


def create_points_history(db: Session, data: PointsHistoryCreate):
    points_entry = PointsHistory(**data.model_dump())
    db.add(points_entry)
    db.commit()
    db.refresh(points_entry)
    return points_entry


def get_points_history(db: Session):
    return db.query(PointsHistory).all()


def get_points_history_by_id(db: Session, entry_id: int):
    return db.query(PointsHistory).filter(PointsHistory.id == entry_id).first()


def update_points_history(db: Session, entry_id: int, data: PointsHistoryUpdate):
    points_entry = get_points_history_by_id(db, entry_id)
    if not points_entry:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(points_entry, key, value)

    db.commit()
    db.refresh(points_entry)
    return points_entry


def delete_points_history(db: Session, entry_id: int):
    points_entry = get_points_history_by_id(db, entry_id)
    if not points_entry:
        return None

    db.delete(points_entry)
    db.commit()
    return True
