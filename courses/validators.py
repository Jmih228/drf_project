from rest_framework.serializers import ValidationError


class TitleLinksValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):

        tmp_val = dict(value).get(self.field)
        for val in tmp_val.split():
            if 'http://' in val or 'https://' in val:
                if val.startswith('https://www.youtube.com/') and '://' not in val[24:]:
                    continue
                raise ValidationError('Except "https://www.youtube.com/{var}" no links allowed')


class DescriptionLinksValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):

        tmp_val = dict(value).get(self.field)
        for val in tmp_val.split():
            if 'http://' in val or 'https://' in val:
                if val.startswith('https://www.youtube.com/') and '://' not in val[24:]:
                    continue
                raise ValidationError('Except "https://www.youtube.com/{var}" no links allowed')
