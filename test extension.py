import datetime
import time


now = str(time.time()).split(".")[0]
file = "ohigiy.png"

print(file.split(".")[-2]+str("_")+str(now)+"."+str(file.split(".")[-1]))