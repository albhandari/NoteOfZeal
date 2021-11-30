import time

print("Your 45 minute work period starts now!")
for i in range(4):
    t = 45*60
    while t:
        minutes = t // 60
        seconds = t % 60
        timer = '{:02d}:{:02d}'.format(minutes, seconds)
        print(timer, "\r")
        time.sleep(1)
        t -= 1
    print("Time for break!")

    t = 15*60
    while t:
        minutes = t // 60
        seconds = t % 60
        timer = '{:02d}:{:02d}'.format(minutes, seconds)
        print(timer, "\r")
        time.sleep(1)
        t -= 1
print("Back to work/studying!")
