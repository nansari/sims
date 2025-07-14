import time
from datetime import datetime, timezone

def current_epoch_time():
    """Returns the current epoch time."""
    return int(time.time())

def epoch_to_utc_iso(epoch_time):
    """Converts epoch time to UTC time in ISO format."""
    return datetime.fromtimestamp(epoch_time, tz=timezone.utc).isoformat()

e = current_epoch_time()
print(e)
print(epoch_to_utc_iso(e))