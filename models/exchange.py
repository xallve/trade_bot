from datetime import datetime

from models.model import AbstractModel
from Api import utils


class Exchange(AbstractModel):
    resource_name = 'exchange'

    id: str = ''
    name: str = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)