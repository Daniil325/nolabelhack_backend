from sqlalchemy.orm import mapper, registry

from src.infra.database.models.vote import Vote
from src.core.entities import Vote as VoteEntity

mapper_reg = registry()
metadata = mapper_reg.metadata

mapper_reg(VoteEntity, Vote)
