from datetime import datetime, timedelta 
d = datetime(2023, 1, 1) 
new_date = d + timedelta(days=10)
print(new_date)

date_string = "2023-05-01" 
date_obj = datetime.strptime(date_string, "%Y-%d-%m")
print(date_obj)