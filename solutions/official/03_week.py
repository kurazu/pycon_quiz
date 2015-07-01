import datetime

tomorrow = datetime.date.today() + datetime.timedelta(days=7)
print tomorrow.strftime('%Y-%m-%d')
