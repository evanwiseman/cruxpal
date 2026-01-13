from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import relationship

from backend.app.db.base import Base


class Ascent(Base):
    __tablename__ = "ascents"

    id = Column(Integer, primary_key=True, index=True)

    athlete_id = Column(Integer, ForeignKey("athletes.id"), nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)

    sent = Column(Boolean, default=False)
    attempt = Column(Integer, default=0)
    notes = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    athlete = relationship("Athlete", back_populates="ascents")
    route = relationship("Route", back_populates="ascents")
