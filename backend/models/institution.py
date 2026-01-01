from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from database import Base


class Institution(Base):
    __tablename__ = "institutions"

    id = Column(Integer, primary_key=True)

    name = Column(String(255), nullable=False)

    # География
    locality_id = Column(
        Integer,
        ForeignKey("localities.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Тип учреждения
    type = Column(
        Enum(
            "university",
            "college",
            "lyceum",
            "school",
            "other",
            name="institution_type",
        ),
        default="university",
        nullable=False,
    )
