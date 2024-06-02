from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from claims.models.base_model import DBBaseModel


class Plan(DBBaseModel):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    plan_group = Column(String, nullable=False)

    @classmethod
    def get_or_create_plan(cls, session: Session, plan_group: str):
        plan = session.query(Plan).filter_by(plan_group=plan_group).first()
        if plan is None:
            plan = Plan(plan_group=plan_group)
            session.add(plan)
            session.commit()
            session.refresh(plan)
        return plan
