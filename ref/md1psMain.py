import md1psNet as md1
import threading as th

if __name__ == '__main__':
    obj1 = md1.Env()
    thread1 = th.Thread(obj1.run(100000))
    thread1.start()
