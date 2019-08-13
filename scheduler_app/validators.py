from django.core.exceptions import ValidationError


def validate_5_segments_or_not(value):
    # for el in value.split():
    #     try:
    #         t = int(el)
    #     except (ValueError, TypeError):
    #         notdigit = True
    #         break
    if len(value.split()) != 5:
        raise ValidationError('%(value)s must have 5 segments', params={'value': value},)
