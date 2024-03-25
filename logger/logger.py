import time
import sys

steady_rate = int(sys.argv[1])
burst = int(sys.argv[2])
time_in_minutes = int(sys.argv[3])

def print_event(i):
    print("Message: " + str(i), flush=True)


time_in_secods = 60 * time_in_minutes
start = time.time()
for i in range(1, time_in_secods * steady_rate):
    print_event(i)
    if i % steady_rate == 0:
        to_wait = 1 - time.time() + start
        if to_wait > 0:
            time.sleep(to_wait)
        start = time.time()

so_far = time_in_secods * steady_rate

for i in range(so_far, so_far + burst + 1):
    print_event(i)
