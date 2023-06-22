from datetime import datetime
import time

for i in range(100):
    time.sleep(3)
    print(datetime.now().date())