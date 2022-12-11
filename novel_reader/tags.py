from datetime import datetime
from humanize import naturaltime


def humantime(time: datetime) -> str:
    return naturaltime(datetime.now() - time)
