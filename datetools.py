from datetime import tzinfo, timedelta

def date_to_dict(date):
    return {'year': date.year,
            'month': date.month,
            'day': date.day,
            'hour': date.hour,
            'minute': date.minute,
            'second': date.second}


timezones = {
    'Paris': tzinfo(timedelta(hours=1)),
    'London': tzinfo(timedelta(hours=0))
}