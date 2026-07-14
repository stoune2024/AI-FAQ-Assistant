"""

Здесь будут жить все Depends

"""

from typing import Annotated, Any

from fastapi import Depends

from settings.settings import Settings, get_settings
from app.database import get_session

SettingsDep = Annotated[Settings, Depends(get_settings)]

SessionDep = Annotated[Any, Depends(get_session)]
