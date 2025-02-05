import datetime
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Vote:
    id: str
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    is_active: bool
    created_at: datetime
