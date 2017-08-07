# -*- coding: utf-8 -*-
import threading
import random
import time

def worker_func():
    print('worker thread started in %s' % (threading.current_thread()))
    # 改变随机数生成器的种子
    random.seed()
    # 让线程睡眠s随机一段时间
    time.sleep(random.random())
    print('worker thread finished in %s' % (threading.current_thread()))

def simple_thread_demo():
    # 创建十个线程来进行测试
    for i in range(10):
        # 每个线程都执行worker_func这个方法，注意这里不需要带括号
        threading.Thread(target=worker_func).start()

# 线程安全锁：一个时间只会有一个线程在运行
def worker_func_lock(lock):
    lock.acquire() # 请求
    worker_func() # 执行
    lock.release() # 释放

# 线程锁
gLock = threading.Lock()
# 线程信号量
gSem = threading.Semaphore(3)


def thread_lock_demo():
    for i in range(10):
        # 开始带锁的线程
        threading.Thread(target=worker_func_lock, args=[gSem]).start()


# 开始讲解经典的线程问题：银行取钱
gPool = 1000
gCondition = threading.Condition()

# 生产者类
class Producer(threading.Thread):
    # 重写父类的run方法
    def run(self):
        # 打印初始的钱
        print('%s started' % threading.current_thread())
        while True:
            # 引用全局变量
            global gPool
            global gCondition
            # 为关键资源操作上锁
            gCondition.acquire()
            random.seed()
            p = random.randint(100, 200)
            gPool += p  # 金库存钱是关键操作，要确保为原子操作
            print('%s: Produced %d. Left %d' % (threading.current_thread(), p, gPool))
            # 随机睡眠一下，为了方便查看打印信息
            time.sleep(random.random())
            gCondition.notify_all()
            # 先通知，再释放
            gCondition.release()


# 消费者类：不停拿钱
class Consumer(threading.Thread):
    def run(self):
        print('%s started' % threading.current_thread())
        while True:
            global gPool
            global gCondition
            # 还是先上锁
            gCondition.acquire()
            # 改变随机数生成器种子
            random.seed()
            # 随机一个消费者要取的金额数
            c = random.randint(500, 1000)
            print('%s: Trying to consume %d. Left %d' % (threading.current_thread(), c, gPool))
            # 如果钱不够就等待生产者存入
            while gPool < c:
                gCondition.wait()
            # 如果钱够就直接扣除
            gPool -= c
            # 随机睡眠一下，为了方便查看打印信息
            time.sleep(random.random())
            print('%s: Consumed %d. Left %d' % (threading.current_thread(), c, gPool))
            gCondition.release()


# 生产者-消费者问题
def consumer_producer_demo():
    for i in range(10):
        Consumer().start()

    for i in range(1):
        Producer().start()

if __name__ == '__main__':
    # simple_thread_demo()
    # thread_lock_demo()
    consumer_producer_demo()