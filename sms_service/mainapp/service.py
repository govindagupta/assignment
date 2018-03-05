
from django.core.exceptions import ValidationError
import re

def do_input_validation(data, rules):

    for item in rules:
        if item['required']:
            try:
                val = data[item['param']]
            except KeyError:
                raise ValidationError (item['param'] + " is missing")

            if re.match(item['regex'], val) is None:
                raise ValidationError(item['param'] + " is invalid")
