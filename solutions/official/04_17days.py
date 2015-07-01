import datetime

tomorrow = datetime.date.today() + datetime.timedelta(days=17)
print tomorrow.strftime('%Y-%m-%d')
