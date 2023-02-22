from datetime import datetime

now = datetime.now()
dstr = now.strftime("%Y-%m-%d_%H-%M-%S")

print(f'current Date is:    {dstr}')
