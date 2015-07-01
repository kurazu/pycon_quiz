import datetime

tomorrow = datetime.date.today() + datetime.timedelta(days=1)
print tomorrow.strftime('%Y-%m-%d')
