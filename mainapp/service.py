
from django.core.exceptions import ValidationError
import re
import time
from .utils import *

def do_input_validation(data, rules):

    for item in rules:
        if item['required']:
            try:
                val = data[item['param']]
            except KeyError:
                raise ValidationError (item['param'] + " is missing")

            if re.match(item['regex'], val) is None:
                raise ValidationError(item['param'] + " is invalid")


RATE_LIMIT_DURATION= 24*3600   # in sec
RATE_LIMIT_COUNT= 50


# check for rate limit. 50 times in 24 hrs
def is_rate_validated(from_no):
    """ First time -  initiate cache,
        Check for rate limit
        Reset if required """
    from_key_time = "from_time_"+from_no
    from_key_count = "from_count_" + from_no

    if not get_cache(from_key_time) or not get_cache(from_key_count):
        set_cache(from_key_time, time.time())
        set_cache(from_key_count, 1)
        return True
    cached_time = get_cache(from_key_time)
    time_diff = time.time() - cached_time
    cached_count = get_cache(from_key_count)

    if time_diff < RATE_LIMIT_DURATION and cached_count >= RATE_LIMIT_COUNT:
        return False
    elif time_diff > RATE_LIMIT_DURATION:
        set_cache(from_key_time, cached_time + RATE_LIMIT_DURATION)
        set_cache(from_key_count, 1)
        return True
    else:  # cached_count < RATE_LIMIT_COUNT
        # print("hit from -%s, count - %s" % (from_no,cached_count))
        set_cache(from_key_count, cached_count+1)
        return True

