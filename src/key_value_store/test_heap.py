from queue import PriorityQueue
from datetime import datetime,timedelta

pq = PriorityQueue()

first_time = datetime.now() + timedelta(seconds=-20)
second_time = datetime.now() + timedelta(seconds = 10)

pq.put((first_time, ["hello","how","are","you"]))
pq.put((second_time, ["how","are","you"]))

print(pq.get()[0].time())