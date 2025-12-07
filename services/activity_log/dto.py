from typing import Optional
from core.dto import BaseDTO, dataclass, field
from core.enums import ActorType


@dataclass
class FilterActivityLogsDTO(BaseDTO):
    """DTO for filtering activity logs."""

    actor_type: Optional[ActorType] = field(default=None)
    actor_identifier: Optional[str] = field(default=None)
    actor_name: Optional[str] = field(default=None)
