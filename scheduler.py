from enum import Enum
import time
import random

from multiprocessing import Process
import multiprocessing

from redis_collections import Dict
from redis import StrictRedis

conn = StrictRedis()
try:
    conn.ping()
except:
    raise Exception('redis not started')
page_dict = Dict(redis=conn, writeback=True, key='SPYDERWEB__PAGE_DICT')

def page(h: str, url: str):
    rn = random.randint(1,10)
    time.sleep(rn)
    print(f'{h} - {rn} - {url}')

def main():
    pl = []
    print ("Start")
    for i in range(1,10):
        p = Process(target=page, args=(i, random.random()))
        p.start()
        pl.append(p)
    while True:
        time.sleep(2)
        r = [x.is_alive() for x in pl]
        print('---')
        print(r)
        print(multiprocessing.active_children())
        print([i.pid for i in multiprocessing.active_children()])
        print('---')
        if not any(r): break
    print ("End")

if __name__ == '__main__':
    main()
