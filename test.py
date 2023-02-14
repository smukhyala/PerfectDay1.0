from threading import Timer
import time

def hello(msg):
    print(msg + ", world")

t = Timer(5, hello)
t.start()

class RepeatTimer(Timer):  
    def run(self):  
        while not self.finished.wait(self.interval):  
            self.function(*self.args,**self.kwargs)  
            print(' ')  
##We are now creating a thread timer and controling it  
timer = RepeatTimer(1,hello,['Repeating'])  
timer.start() #recalling run  
print('Threading started')  
time.sleep(10)#It gets suspended for the given number of seconds  
print('Threading finishing')  
timer.cancel()