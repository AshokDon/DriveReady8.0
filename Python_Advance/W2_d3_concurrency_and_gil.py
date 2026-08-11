'''
The Story Swiggy's Slow Order Page

You have all opened swiggy and tapped on a restaurant
before that page shows anything the backend must call SIX services

service                what it gives you        time
-------------------------------------------------------
restaurant service     name, photo, rating      400 ms
menu service           the food list            400 ms
delivery service       "35 mins"                400 ms
offers service         "50% OFF"                400 ms
reviews service        star ratings             400 ms
rider service          rider location           400 ms
-------------------------------------------------------
TOTAL one after another                        2400 ms

2.4 seconds. the user is just staring at a loading spinner

now the important question


First Principle Thinking
Ask your self

Q1) during those 2.4 seconds what is the CPU actually DOING ?

    Nothing.
    it sent a network request and it is WAITING for the reply
    it is like a cook who puts rice on the stove and then just
    STANDS AND STARES at the pot for 20 minutes
    instead of chopping vegetables while the rice boils

Q2) do these 6 services depend on each other ?

    No. the menu does not need the rider location
    so why are we waiting for #1 to finish before starting #2 ?

Q3) if all six ran at the SAME TIME what would the total be ?

    400 ms. not 2400 ms
    6x faster and we did not buy a single new server

Q4) now a DIFFERENT job . resize 1000 photos each takes 400ms of
    pure CPU calculation . does the same trick work ?

    hold that question . it is the whole reason this topic is big

'''

import os
from threading import Thread, Lock
from time import sleep, time
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


#-----------------------------vocabulary---------------------------------------#
'''
get these 3 right and everything else follows

PROGRAM   -> a file sitting on your disk . not running . passive
             like a recipe written in a book

PROCESS   -> a running instance of that program
             it gets its OWN MEMORY . its own variables
             like a kitchen that is actually cooking that recipe

THREAD    -> a worker INSIDE a process
             all threads of a process SHARE the same memory
             like the cooks working inside that ONE kitchen


      +------------- PROCESS 1 (own memory) -------------+
      |   Thread-1     Thread-2     Thread-3             |
      |       ------ SHARED VARIABLES ------             |
      +--------------------------------------------------+

      +------------- PROCESS 2 (own memory) -------------+
      |   Thread-1                                       |
      |       ------ ITS OWN VARIABLES ------            |
      +--------------------------------------------------+


ONE SENTENCE THAT MATTERS

        THREADS SHARE MEMORY .  PROCESSES DO NOT

that single fact creates every advantage and every danger in this file


CONCURRENCY vs PARALLELISM   (interviewers love this)

CONCURRENCY = many tasks IN PROGRESS , switching between them
              ONE cook making 3 dishes switching while things boil

PARALLELISM = many tasks RUNNING at the same instant
              THREE cooks , three dishes

in python threads give CONCURRENCY . processes give PARALLELISM
'''


#-----------------------------idea 1 ------------------------------------------#
'''
SEQUENTIAL . this is what swiggy had
call one service , wait , call next , wait , call next ...
'''

services = ['restaurant', 'menu', 'delivery', 'offers', 'reviews', 'rider']


def call_service(name):
    print("   calling", name)
    sleep(0.4)                     # sleep = WAITING = this is I/O work
    print("   got", name, "data")


print("SEQUENTIAL :")
start = time()
for s in services:
    call_service(s)
end = time()
seq_time = end - start
print(f"sequential time : {seq_time:.2f} s")

'''
2.4 seconds and the CPU was idle almost the whole time
we are not slow because we are doing too much work
we are slow because we are WAITING , one wait at a time
'''


#-------------------------> Idea 2 <-------------------------------------------#
'''
THREADS . do all the waiting together

a thread lets us START all six calls and then wait for all of them
TOGETHER instead of one by one

exact same function . we only change HOW we call it
'''

print()
print("THREADED :")

threads = []
for s in services:
    t = Thread(target=call_service, args=(s,))
    threads.append(t)
    # note args must be a TUPLE
    # args=(s) is NOT a tuple it is just s
    # for one argument you must write args=(s,) with the comma

start = time()

for t in threads:
    t.start()          # START ALL SIX FIRST

for t in threads:
    t.join()           # THEN wait for all six

end = time()
thread_time = end - start

print(f"threaded time   : {thread_time:.2f} s")
print(f"speedup         : {seq_time / thread_time:.1f}x")

'''
2.4 seconds  ->  0.4 seconds

look at the output above . in the sequential part you see

    calling restaurant
    got restaurant data
    calling menu
    got menu data          one finishes , then next starts

in the threaded part you see

    calling restaurant
    calling menu
    calling delivery       all six start together
    ...                    then all six finish together


WHY ? because the six 0.4 second WAITS happened AT THE SAME TIME
instead of back to back

we did not make the network faster
we just stopped standing in a queue to wait

sequential                     threaded
---------------------------------------------------
wait 0.4 for restaurant        all six start together
wait 0.4 for menu              all six wait together
wait 0.4 for delivery          all six finish together
wait 0.4 for offers
wait 0.4 for reviews           total = 0.4 s
wait 0.4 for rider
total = 2.4 s


ONE MORE THING YOU MAY NOTICE IN THE OUTPUT

sometimes two lines get MIXED together like this

        got   got delivery data
     menu data

that is not a bug in your code . print() is really TWO steps ->
write the text , then write the newline . a thread can get paused
in between those two steps

two threads touched the same thing (the screen) at the same time
and the output got corrupted

remember this . it is a small preview of the BIG problem later
in this file
'''


#-----------------------------how do i get the answer back---------------------#
'''
above the function only PRINTED . it did not give us the data

problem -> a thread cannot return a value to you
        result = t.start()      does NOT work

simple fix -> the thread puts its answer into a list
'''

answers = []

# in real life every service is a different speed . lets be realistic
speed = {'restaurant': 0.5, 'menu': 0.1, 'delivery': 0.3,
         'offers': 0.2, 'reviews': 0.4, 'rider': 0.15}


def call_service_collect(name):
    sleep(speed[name])
    answers.append(name + "-data")       # put the answer in the shared list


threads = []
for s in services:
    t = Thread(target=call_service_collect, args=(s,))
    threads.append(t)

for t in threads:
    t.start()
for t in threads:
    t.join()

print()
print("we asked in this order :", services)
print("answers came back as   :", answers)

'''
LOOK AT THE TWO LINES . THE ORDER IS DIFFERENT

we asked  restaurant , menu , delivery , offers , reviews , rider
we got    menu , rider , offers , delivery , reviews , restaurant

why ? menu took 0.1 s so it finished first
      restaurant took 0.5 s so it finished last

whichever thread finishes first appends first
threads do NOT come back in the order you started them

that is fine here . but if your code says answers[0] expecting the
restaurant , you now have a bug

if you need the order correct use the object way below ,
or ThreadPoolExecutor at the end of this file
'''


#-----------------------------the #1 beginner mistake--------------------------#
'''
this is the mistake almost everyone makes the first time
it looks correct . it reads nicely . and it gives you ZERO benefit
'''


def quiet_service(name):
    sleep(0.4)


start = time()
for s in services:
    t = Thread(target=quiet_service, args=(s,))
    t.start()
    t.join()                   # WRONG . waits here before starting the next one
end = time()
wrong_time = end - start

print()
print(f"start+join in same loop : {wrong_time:.2f} s   no benefit at all")
print(f"start all then join all : {thread_time:.2f} s   correct")

'''
join() means "block until this thread finishes"
if you join immediately after start you are just doing it one by one again
with extra typing

RULE ->  START THEM ALL . THEN JOIN THEM ALL
'''


#-----------------------------the other way to make a thread-------------------#
'''
way 1 was Thread(target=function)
way 2 is to subclass Thread and write run()

nice thing about way 2 -> the object can HOLD its own answer in self.result
so you do not need a shared list , and the order stays correct
'''


class ServiceCaller(Thread):
    def __init__(self, service_name):
        super().__init__()             # MUST call this or python errors out
        self.service_name = service_name
        self.result = None

    def run(self):                     # must be named exactly "run"
        sleep(0.4)
        self.result = self.service_name + "-data"


workers = []
for s in services:
    w = ServiceCaller(s)
    workers.append(w)

for w in workers:
    w.start()                          # start()  NOT  run()
for w in workers:
    w.join()

print()
print("results from objects :")
for w in workers:
    print("   ", w.result)             # order is correct now

'''
WARNING 1 -> you must call super().__init__() or it breaks

WARNING 2 -> t.start() creates a NEW thread and calls run() inside it
             t.run()   just calls the method normally on the SAME thread
                       no thread is created at all

             the bad part is t.run() still "works" . it just runs slowly
             one by one and gives no error . that is the worst kind of bug

             ALWAYS start() . NEVER run()
'''


#-------------------------> Idea 3 <-------------------------------------------#
'''
THE GIL . why threads are not magic

remember Q4 from the top
    "resize 1000 photos each 400ms of pure CPU work . same trick ?"

the answer is NO . and here is why

python (CPython) has a GLOBAL INTERPRETER LOCK . the GIL

    only ONE thread can run python code at a time
    even if your laptop has 16 cores

        Thread1 ---
        Thread2 ------>  [ GIL ]  ---> only one gets in
        Thread3 ---

then why did our swiggy example get 6x faster ??

BECAUSE THE GIL IS RELEASED WHILE WAITING

    sleep()           -> releases the GIL
    network call      -> releases the GIL
    reading a file    -> releases the GIL
    heavy math loop   -> HOLDS the GIL

so threads help when your code is WAITING
threads do NOT help when your code is CALCULATING


THE ONE RULE FOR THIS WHOLE TOPIC

    +--------------------------------------------------+
    |  I/O-BOUND  (waiting : network , disk , sleep)   |
    |         --->  USE THREADS                        |
    |                                                  |
    |  CPU-BOUND  (calculating : math , images , ML)   |
    |         --->  USE PROCESSES                      |
    +--------------------------------------------------+

let us PROVE it . same 4 threads . different kind of work
'''


def heavy_math():
    total = 0
    for i in range(4000000):       # pure calculation . no waiting at all
        total = total + i * i
    return total


# --- CPU work one after another ---
start = time()
for i in range(4):
    heavy_math()
end = time()
cpu_seq = end - start

# --- CPU work with 4 threads ---
threads = []
for i in range(4):
    t = Thread(target=heavy_math)
    threads.append(t)

start = time()
for t in threads:
    t.start()
for t in threads:
    t.join()
end = time()
cpu_threads = end - start

print()
print(f"CPU work sequential : {cpu_seq:.2f} s")
print(f"CPU work threaded   : {cpu_threads:.2f} s   NOT faster")
print(f"I/O work sequential : {seq_time:.2f} s")
print(f"I/O work threaded   : {thread_time:.2f} s   6x faster")

'''
same 4 threads . completely different result

I/O work  -> threads WIN   they wait together
CPU work  -> threads LOSE  they queue up for the GIL , plus switching cost

this is the single most important fact about python threading
if you remember one thing from this file remember this
'''


#-------------------------> Idea 4 <-------------------------------------------#
'''
PROCESSES . escape the GIL

for CPU work we need REAL parallelism -> separate PROCESSES

each process has its own python interpreter and its OWN GIL
so they truly run at the same time on different CPU cores

good news -> the code looks the same as Thread

        Thread(target=fn)
        Process(target=fn)

        .start()   .join()      same


IMPORTANT -> multiprocessing code MUST be inside

        if __name__ == "__main__":

on windows and mac python starts a child process by RE-IMPORTING your file
without the guard each child re runs your code and makes more children
forever . on linux it usually works anyway which makes this a nasty bug
that only shows up on your friends laptop
'''

cores = os.cpu_count()

if __name__ == "__main__":

    processes = []
    for i in range(4):
        p = Process(target=heavy_math)
        processes.append(p)

    start = time()
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    end = time()
    cpu_procs = end - start

    print()
    print("cores on this machine :", cores)
    print(f"CPU sequential : {cpu_seq:.2f} s")
    print(f"CPU threads    : {cpu_threads:.2f} s   GIL blocks it")
    print(f"CPU processes  : {cpu_procs:.2f} s")

    if cores > 1:
        print("-> processes are faster . that is REAL parallelism")
    else:
        print("-> this machine has only 1 core so there is nothing to run")
        print("   in parallel . on your 4 core laptop you will see roughly")
        print("   sequential divided by number of cores")

'''
on a normal 4 core laptop you will see something like

    CPU sequential : 2.40 s
    CPU threads    : 2.45 s     no help , the GIL
    CPU processes  : 0.65 s     about 4x faster

that is the whole point of processes
'''


#-----------------------------the danger---------------------------------------#
'''
threads sharing memory is FAST . it is also DANGEROUS

swiggy keeps a running total of todays revenue in one variable
four threads each add 1000 payments to it

expected 4000 . lets see what we actually get


why does it break ? because

        revenue = revenue + 1

is NOT one action . it is THREE

        1. READ  revenue
        2. ADD   1
        3. WRITE revenue back

a thread can be paused BETWEEN step 1 and step 3

        Thread A reads  100
        Thread B reads  100      same old value
        Thread A writes 101
        Thread B writes 101      should be 102 . ONE PAYMENT LOST
'''

revenue = 0


def add_payments_unsafe():
    global revenue
    for i in range(1000):
        tmp = revenue          # READ
        sleep(0)               # let another thread jump in (widens the gap)
        revenue = tmp + 1      # WRITE . tmp may already be old


threads = []
for i in range(4):
    t = Thread(target=add_payments_unsafe)
    threads.append(t)

for t in threads:
    t.start()
for t in threads:
    t.join()

print()
print("expected revenue :", 4000)
print("actual revenue   :", revenue, "  PAYMENTS LOST")

'''
the sleep(0) is only there so the bug shows up EVERY time in class
in real code the gap is tiny but it is still there

that is what makes race conditions so evil
they pass all your tests and then fail once a week at 3 AM
and you cannot reproduce it
'''


#-----------------------------the fix------------------------------------------#
'''
a Lock makes it one at a time
only ONE thread can be inside the "with lock:" block
'''

revenue_safe = 0
lock = Lock()


def add_payments_safe():
    global revenue_safe
    for i in range(1000):
        with lock:                 # only one thread inside at a time
            tmp = revenue_safe
            sleep(0)
            revenue_safe = tmp + 1


threads = []
for i in range(4):
    t = Thread(target=add_payments_safe)
    threads.append(t)

for t in threads:
    t.start()
for t in threads:
    t.join()

print("expected revenue :", 4000)
print("with lock        :", revenue_safe, "  correct every time")

'''
the code inside "with lock:" is called the CRITICAL SECTION
only one thread may be inside it

ALWAYS use "with lock:"
the manual way needs try/finally

        lock.acquire()
        try:
            revenue = revenue + 1
        finally:
            lock.release()     # if you forget this everything hangs forever

keep the critical section as SMALL as possible
never do a network call while holding a lock . everyone else waits
'''


#-------------------------> Idea 5 <-------------------------------------------#
'''
what you actually use at work -> ThreadPoolExecutor

making Thread objects by hand is great for learning
in real code you use a POOL . same idea , much less typing
and the results come back IN ORDER

best part -> to switch from threads to processes you change ONE WORD
'''


def get_service_data(name):
    sleep(0.4)
    return name + "-data"          # now the function can just RETURN


start = time()
with ThreadPoolExecutor(max_workers=6) as pool:
    results = pool.map(get_service_data, services)
    for r in results:
        print("   ", r)
end = time()
pool_time = end - start

print(f"pool time : {pool_time:.2f} s   same speed , way less code")

'''
compare the two versions

MANUAL                                    POOL
answers = []                              with ThreadPoolExecutor(6) as pool:
threads = []                                  results = pool.map(fn, services)
for s in services:
    t = Thread(target=fn, args=(s,))
    threads.append(t)
for t in threads: t.start()
for t in threads: t.join()

8 lines , and the function had to           2 lines , the function just
append into a shared list                   returns normally , order is correct


ONE MORE BIG REASON TO USE POOLS -> errors

if a raw Thread raises an exception it prints a traceback and DIES silently
your program keeps going thinking everything worked
with a pool the exception comes back to you and you can catch it
'''


def service_may_fail(name):
    sleep(0.2)
    if name == "offers":
        raise ConnectionError("offers-service is down")
    return name + "-data"


print()
print("one service is down :")

with ThreadPoolExecutor(max_workers=6) as pool:
    jobs = []
    for s in services:
        job = pool.submit(service_may_fail, s)
        jobs.append(job)

    for job in jobs:
        try:
            print("   OK   ", job.result())
        except Exception as e:
            print("   FAIL  ", e)

'''
one dead service did NOT break the whole page
the other five loaded fine . that is what you want in production

job.result()  gives you the answer , OR raises the error that happened
inside that thread . that is why we wrap it in try / except
'''


#-----------------------------ProcessPoolExecutor------------------------------#
'''
for CPU work . literally the same code with ONE word changed
'''

if __name__ == "__main__":

    start = time()
    with ThreadPoolExecutor() as pool:
        for i in range(4):
            pool.submit(heavy_math)
    end = time()
    t_time = end - start

    start = time()
    with ProcessPoolExecutor() as pool:            # ONE WORD CHANGED
        for i in range(4):
            pool.submit(heavy_math)
    end = time()
    p_time = end - start

    print()
    print(f"ThreadPoolExecutor  : {t_time:.2f} s")
    print(f"ProcessPoolExecutor : {p_time:.2f} s")
    if cores > 1:
        print("-> processes win because this is CPU work")
    else:
        print("-> no difference here , only 1 core . on your laptop they win")


#-----------------------------how to decide------------------------------------#
'''
the only flowchart you need


        is your code mostly WAITING or mostly CALCULATING ?
                        |
        +---------------+----------------+
        |                                |
    WAITING                        CALCULATING
    (network , disk ,              (math , images ,
     database , sleep)              ML , encryption)
        |                                |
        v                                v
    ThreadPoolExecutor              ProcessPoolExecutor



REAL EXAMPLES

    USE THREADS                          USE PROCESSES
    -----------                          -------------
    calling 6 swiggy services            resizing 10000 photos
    downloading 50 files                 video encoding
    hitting 100 API endpoints            training an ML model
    reading many files from disk         password hashing
    web scraping                         big pandas / numpy math
    database queries                     parsing 1000 huge log files
    keeping a UI from freezing           monte carlo simulation



COMPARISON

                        THREADS              PROCESSES
    memory              SHARED               SEPARATE
    real parallelism    NO (GIL)             YES
    cost to create      cheap (KB)           expensive (MB)
    sharing data        free but risky       must be copied
    if one crashes      can kill all         others survive
    main danger         race conditions      memory + startup cost
    how many            tens to hundreds     about = number of cores



ADVANTAGES OF THREADS
    + huge speedup for waiting type work   2.4s -> 0.4s
    + cheap , you can make hundreds
    + share data with zero copying
    + work with ANY normal library , no rewrite needed
    + keep an app responsive instead of frozen

DISADVANTAGES OF THREADS
    - NO speedup for CPU work  (the GIL)
    - race conditions . bugs that appear randomly and are brutal to find
    - deadlock . two threads each waiting for the others lock
    - output order is unpredictable
    - an error inside a raw thread is silent

ADVANTAGES OF PROCESSES
    + REAL multi core parallelism , GIL does not apply
    + one crash does not kill the others
    + no shared variables so no accidental race conditions

DISADVANTAGES OF PROCESSES
    - slow to start . milliseconds each plus a memory copy
    - uses much more RAM . each has its own interpreter
    - data must be copied to be sent . big objects are expensive
    - needs the  if __name__ == "__main__"  guard
    - harder to debug


ONE LAST WARNING
    do not add threads before you know WHY your code is slow
    if the bottleneck is calculation threads make it WORSE
    measure first . then choose
'''


#-----------------------------summary------------------------------------------#

print()
print("SUMMARY")
print("1.  process = own memory . thread = shared memory")
print("2.  concurrency = taking turns . parallelism = truly at once")
print("3.  the GIL . only one thread runs python code at a time")
print("4.  BUT the GIL is released while waiting -> threads help I/O")
print("5.  WAITING work -> ThreadPoolExecutor")
print("    CALCULATING  -> ProcessPoolExecutor")
print("6.  start() ALL then join() ALL . never start+join in one loop")
print("7.  use start() never run()")
print("8.  a thread cannot return . use a list , self.result , or a pool")
print("9.  revenue = revenue + 1 is 3 steps not 1 . shared data needs a Lock")
print("10. multiprocessing needs  if __name__ == '__main__':")
print()
print("bye")
