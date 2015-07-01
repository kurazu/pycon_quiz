import datetime

tomorrow = datetime.date.today() + datetime.timedelta(days=2048)
print tomorrow.strftime('%Y-%m-%d')
