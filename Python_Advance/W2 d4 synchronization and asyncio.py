'''
The Story Swiggy's Notification Service

last file we fixed the order page with threads . 2.4 s became 0.4 s
we also found the race condition and fixed it with a Lock

now a NEW service . live order tracking

    every customer waiting for food keeps ONE connection open to swiggy
    so we can push  "rider picked up your order"  the moment it happens

at dinner time 10,000 customers are waiting at the same time
10,000 connections , all open , all doing NOTHING except waiting


the team already knows threads . so they wrote

        for customer in waiting_customers:
            t = Thread(target=hold_connection, args=(customer,))
            t.start()

it worked for 50 test users

on the server with 10,000 it printed

        can't start new thread

do the maths . every thread gets its own stack . on linux that is 8 MB

        10,000 threads  x  8 MB  =  80 GB

the server has 16 GB


now the important question


First Principle Thinking
Ask your self

Q1) those 10,000 connections . how many are actually DOING work
    at any moment ?

    almost none . they are all WAITING for something to happen
    a thread that is waiting is a very expensive way to wait

Q2) a thread costs 8 MB because the operating system must be able to
    interrupt it at ANY line and switch away

    but our code only ever pauses at ONE place . the network wait
    do we need to be interruptible everywhere ?

    No. we only need to pause where WE choose to pause

Q3) so what if pausing was something the FUNCTION did on purpose
    instead of something the OS did to it ?

    then we would not need 10,000 stacks
    one thread could hold all 10,000 paused functions

Q4) you have already seen a function that pauses itself and
    keeps its variables

        remember  yield  from the generators file ?

    hold that thought . that is literally where async came from

'''

import asyncio
import threading
import tracemalloc
from time import sleep, time
from concurrent.futures import ThreadPoolExecutor


#=============================================================================#
#                 PART 1  --  FINISHING SYNCHRONIZATION                       #
#=============================================================================#

#-----------------------------quick recap--------------------------------------#
'''
from the concurrency file , in one minute

    threads SHARE memory . that is fast and that is dangerous

        revenue = revenue + 1

    is really THREE steps . read , add , write
    two threads can read the same old value and one payment is lost

    the fix was a Lock . only one thread inside at a time

        with lock:
            revenue = revenue + 1

a Lock protects ONE thing from EVERYONE
now we need something different
'''


#-----------------------------idea 1 ------------------------------------------#
'''
THE NEW PROBLEM . the gateway has a limit

swiggy's payment gateway says
        "you may open at most 3 connections at a time . more and we ban you"

a Lock is no good here . a Lock allows ONE
we want to allow THREE

that is a SEMAPHORE . a lock with a counter

        Lock            = 1 permit
        Semaphore(3)    = 3 permits

think of 3 parking spaces . the 4th car waits for someone to leave
'''

active = 0
peak = 0
counter_lock = threading.Lock()
gateway_limit = threading.Semaphore(3)          # only 3 at a time


def call_gateway(order_id):
    global active, peak
    with gateway_limit:                          # take a permit , or WAIT
        with counter_lock:
            active = active + 1
            if active > peak:
                peak = active
        sleep(0.2)                               # talking to the bank
        with counter_lock:
            active = active - 1


print("PART 1 . IDEA 1 : Semaphore")

threads = []
for i in range(9):
    t = threading.Thread(target=call_gateway, args=(i,))
    threads.append(t)

start = time()
for t in threads:
    t.start()
for t in threads:
    t.join()
end = time()

print("   9 payments , limit of 3")
print("   highest number running together :", peak)
print(f"   time taken : {end - start:.2f} s   (3 waves of 0.2 s)")

'''
peak never goes above 3 . the gateway is protected

9 payments in 3 waves = 0.6 seconds
without the semaphore all 9 would hit the bank at once and we get banned


WHERE YOU ACTUALLY USE A SEMAPHORE

    a database that allows 20 connections
    an API that allows 100 calls per minute
    downloading files without saturating the network
    a printer queue . 2 printers , 50 jobs

    Semaphore(1) behaves like a Lock . a Lock is just the common case


ONE MORE THING . BoundedSemaphore

    Semaphore lets you release more times than you acquired , which
    silently INCREASES the limit . nobody notices until the ban email
    BoundedSemaphore raises an error instead . prefer it
'''


#-----------------------------the ceiling--------------------------------------#
'''
so threads plus locks plus semaphores solve everything ?

no . they have a hard ceiling . lets measure it
'''


def just_wait(event):
    event.wait()


print()
print("the cost of a thread :")

event = threading.Event()
tracemalloc.start()
start = time()
threads = []
for i in range(2000):
    t = threading.Thread(target=just_wait, args=(event,))
    t.start()
    threads.append(t)
end = time()
current, peak_mem = tracemalloc.get_traced_memory()
tracemalloc.stop()

thread_create_time = end - start
print(f"   2000 threads created in {thread_create_time:.2f} s")
print(f"   python side memory      : {peak_mem / 1024 / 1024:.1f} MB")
print("   PLUS 8 MB of stack each , reserved by the operating system")

event.set()
for t in threads:
    t.join()

'''
2000 threads took a full second just to CREATE . before doing any work

and the stack is the killer

        1,000  threads  x  8 MB  =   8 GB
        10,000 threads  x  8 MB  =  80 GB

for connections that are doing NOTHING but waiting

that is Q1 . we are paying 8 MB to sit still
'''


#=============================================================================#
#                        PART 2  --  ASYNCIO                                  #
#=============================================================================#
'''
this pays off Q4

remember the generators file

        def order_amounts(count):
            for i in range(count):
                yield i * 10          <- gives a value and PAUSES itself

the function paused . it kept its variables . it waited to be asked again
and it cost almost no memory because there was no extra stack

async is that same idea , pointed at WAITING instead of at data

        async def get_menu():
            data = await fetch()      <- pauses HERE and lets others run

    yield   pauses to hand out a value
    await   pauses to wait for something slow

one thread . thousands of paused functions . no stacks
'''


#-----------------------------idea 2 ------------------------------------------#
'''
THE THREE WORDS

    async def       this function is allowed to pause
    await           pause here , let other work run , wake me when it is done
    asyncio.run()   start the event loop and run one async function

what is the EVENT LOOP ?

    one thread with a to do list
    it runs a function until that function says await
    then it parks it , picks the next one , and keeps going
    when the slow thing finishes it puts the function back on the list

    it is a single receptionist handling 200 people , not 200 receptionists
'''


async def get_service(name, delay):
    print("      calling", name)
    await asyncio.sleep(delay)                  # pause . do NOT block others
    print("      got", name)
    return name + "-data"


async def one_at_a_time():
    result1 = await get_service("menu", 0.3)
    result2 = await get_service("offers", 0.3)
    return [result1, result2]


print()
print("PART 2 . IDEA 2 : async and await")
start = time()
answers = asyncio.run(one_at_a_time())
end = time()
print("   result :", answers)
print(f"   time   : {end - start:.2f} s")

'''
0.6 seconds . that is SEQUENTIAL . we did not gain anything yet

why ? because  await  means  "wait right here for this one"
we awaited menu , then awaited offers . one after the other

await alone does not make things concurrent
you have to START them all first . next idea
'''


#-------------------------> Idea 3 <-------------------------------------------#
'''
asyncio.gather . start them ALL , then wait for ALL

this is the exact same shape as the threads file

        for t in threads: t.start()      start them all
        for t in threads: t.join()       then wait for all

gather does both lines at once
'''


async def all_together():
    results = await asyncio.gather(
        get_service("menu", 0.3),
        get_service("offers", 0.3),
        get_service("reviews", 0.3),
        get_service("rider", 0.3),
    )
    return results


print()
print("IDEA 3 : asyncio.gather")
start = time()
answers = asyncio.run(all_together())
end = time()
print("   result :", answers)
print(f"   time   : {end - start:.2f} s   (four 0.3 s waits overlapped)")

'''
4 services , 0.3 seconds each , total 0.3 seconds

look at the printed order . all four "calling" lines come first
then all four "got" lines . they overlapped

gather also keeps the RESULTS IN ORDER even though they finished in any order
that is nicer than the raw threads version where we had to sort it out
'''


#-----------------------------the real comparison------------------------------#
'''
now the number that matters . 2000 waiting connections

threads  -> 2000 stacks
asyncio  -> 2000 paused functions in ONE thread
'''


async def hold_connection(customer_id):
    await asyncio.sleep(0.2)
    return customer_id


async def many_connections(count):
    tasks = []
    for i in range(count):
        tasks.append(hold_connection(i))
    return await asyncio.gather(*tasks)


print()
print("2000 waiting connections :")

tracemalloc.start()
start = time()
done = asyncio.run(many_connections(2000))
end = time()
current, peak_mem = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"   asyncio : {end - start:.2f} s , {peak_mem / 1024 / 1024:.1f} MB")
print(f"   threads : {thread_create_time:.2f} s just to CREATE them ,")
print("             plus 8 MB of stack each from the OS")
print("   all 2000 finished :", len(done) == 2000)

'''
that is the whole reason asyncio exists

    threads  are cheap compared to processes
    tasks    are cheap compared to threads

    the python side looks similar . the STACKS are what kill you
    2000 threads reserve 2000 x 8 MB = 16 GB from the operating system
    2000 tasks reserve nothing . they are just python objects on the heap

    a thread is created by the OS . a task is just a python object
'''


#-----------------------------the #1 asyncio mistake---------------------------#
'''
ONE BLOCKING LINE FREEZES EVERYTHING

there is only ONE thread . if any function refuses to pause , nothing
else can run . the whole server stops

    sleep(1)             BLOCKS . the old one from  time
    await asyncio.sleep(1)   pauses politely

same trap with
    requests.get()       BLOCKS      ->  use httpx or aiohttp
    open().read()        BLOCKS      ->  use aiofiles
    a heavy math loop    BLOCKS      ->  send it to a process
'''


async def polite(name):
    await asyncio.sleep(0.2)
    return name


async def rude(name):
    sleep(0.2)                          # WRONG . blocks the whole loop
    return name


async def all_polite():
    return await asyncio.gather(polite("a"), polite("b"), polite("c"))


async def one_is_rude():
    return await asyncio.gather(rude("a"), rude("b"), rude("c"))


print()
print("blocking vs non blocking :")

start = time()
asyncio.run(all_polite())
polite_time = time() - start

start = time()
asyncio.run(one_is_rude())
rude_time = time() - start

print(f"   await asyncio.sleep : {polite_time:.2f} s   overlapped")
print(f"   plain sleep         : {rude_time:.2f} s   NOT overlapped")

'''
same gather . same three functions . three times slower

and this is the cruel part -> NO ERROR . nothing warns you
your async code just quietly behaves like sequential code

if your async app is slow , look for a blocking call first


IF YOU MUST CALL BLOCKING CODE , hand it to a thread

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, blocking_function, arg)

asyncio and threads are not enemies . asyncio waits , threads block
'''


#-----------------------------semaphore in asyncio-----------------------------#
'''
the gateway still allows only 3 connections
asyncio has its own Semaphore . same idea , different import

    threading.Semaphore   for threads
    asyncio.Semaphore     for async . you must AWAIT the acquire
'''

async_active = 0
async_peak = 0


async def async_gateway(order_id, limit):
    global async_active, async_peak
    async with limit:                            # NOTE async with
        async_active = async_active + 1
        if async_active > async_peak:
            async_peak = async_active
        await asyncio.sleep(0.1)
        async_active = async_active - 1
    return order_id


async def nine_payments():
    limit = asyncio.Semaphore(3)
    tasks = []
    for i in range(9):
        tasks.append(async_gateway(i, limit))
    return await asyncio.gather(*tasks)


print()
print("asyncio Semaphore :")
start = time()
asyncio.run(nine_payments())
end = time()
print("   highest running together :", async_peak)
print(f"   time : {end - start:.2f} s")

'''
NOTE -> we did NOT need a Lock around async_active

why ? there is only ONE thread , and it can only switch at an await
so the three lines between the awaits can never be interrupted

that removes a whole category of race condition
but the moment you put an await in the middle of your read-modify-write ,
the race is back . asyncio has a Lock for exactly that case
'''


#-----------------------------handling failures--------------------------------#
'''
one service is down . we do not want the page to die
'''


async def maybe_fails(name):
    await asyncio.sleep(0.1)
    if name == "offers":
        raise ConnectionError("offers-service is down")
    return name + "-data"


async def fetch_all():
    results = await asyncio.gather(
        maybe_fails("menu"),
        maybe_fails("offers"),
        maybe_fails("reviews"),
        return_exceptions=True,             # <-- the important bit
    )
    return results


print()
print("one service is down :")
for r in asyncio.run(fetch_all()):
    if isinstance(r, Exception):
        print("   FAIL :", r)
    else:
        print("   OK   :", r)

'''
return_exceptions=True  puts the error in the results list instead of
throwing it . the other two services still came back

WITHOUT it , the first error kills the whole gather and you lose
the results of the ones that succeeded

this is the same lesson as job.result() in the threads file
one dead service must not break the page
'''


#-----------------------------httpx--------------------------------------------#
'''
real API calls . requests does NOT work with asyncio because it blocks

        pip install httpx

REFERENCE CODE . not run here because httpx is not installed


        import httpx

        async def fetch(client, url):
            response = await client.get(url)
            return response.status_code

        async def fetch_all(urls):
            async with httpx.AsyncClient(timeout=10) as client:
                tasks = []
                for url in urls:
                    tasks.append(fetch(client, url))
                return await asyncio.gather(*tasks, return_exceptions=True)

        urls = ["https://example.com"] * 10
        results = asyncio.run(fetch_all(urls))


THREE THINGS TO NOTICE

    1. ONE client shared by all requests , inside async with
       it reuses connections . making a client per request is slow and wrong

    2. always give a timeout . without one a dead server hangs your task forever

    3. return_exceptions=True so one bad url does not kill the batch

    requests  ->  blocking  ->  use with ThreadPoolExecutor
    httpx     ->  async     ->  use with asyncio
'''


#-----------------------------how to decide------------------------------------#
'''
you now have FOUR tools . this is the whole decision


        is your code WAITING or CALCULATING ?
                        |
        +---------------+----------------+
        |                                |
    WAITING                        CALCULATING
        |                                |
        |                          ProcessPoolExecutor
        |                          (the GIL blocks threads)
        |
    how many at once ?
        |
    +---+--------------------+
    |                        |
  tens to hundreds      thousands
    |                        |
ThreadPoolExecutor        asyncio
(works with ANY           (needs async libraries
 normal library)           httpx , asyncpg , aiofiles)



SIDE BY SIDE

                        THREADS              ASYNCIO
    how many            hundreds             tens of thousands
    cost each           ~8 MB stack          a few KB
    who decides to pause the OS , anywhere   YOU , at each await
    race conditions     yes . need locks     far fewer . only around await
    normal libraries    all of them work     only async ones
    one slow call       other threads fine   FREEZES EVERYTHING
    difficulty          easier to start      more rules to learn


ADVANTAGES OF ASYNCIO
    + tens of thousands of connections on one thread
    + no 8 MB per connection
    + you can SEE every pause point . the awaits are written down
    + far fewer race conditions . one thread , switches only at await

DISADVANTAGES OF ASYNCIO
    - your whole stack must be async . one blocking call ruins it
    - async spreads . an async function can only be awaited by another one
    - error messages and tracebacks are harder to read
    - NO help at all for CPU work . one thread , same GIL


WHEN TO ACTUALLY REACH FOR IT

    use asyncio when
        thousands of connections at once . chat , live tracking , websockets
        a web API that mostly waits on a database
        a scraper hitting 10,000 urls

    stay with threads when
        a few hundred calls
        the library you must use is blocking (requests , most db drivers)
        the team does not know async yet . threads are simpler and correct
'''


#-----------------------------summary------------------------------------------#

print()
print("SUMMARY")
print("1.  Lock allows 1 . Semaphore(n) allows n . a Lock is Semaphore(1)")
print("2.  use BoundedSemaphore . it errors on over release")
print("3.  a thread costs 8 MB of stack . 10,000 threads = 80 GB")
print("4.  await pauses like yield did . that is where async came from")
print("5.  async def marks it . await pauses it . asyncio.run starts it")
print("6.  await alone is still sequential . gather is what overlaps")
print("7.  asyncio.gather = start them all , then wait for all")
print("8.  2000 tasks = a few MB . 2000 threads reserve 16 GB of stack")
print("9.  ONE blocking call freezes the whole loop . and gives NO error")
print("10. asyncio.sleep not sleep . httpx not requests")
print("11. async with for asyncio.Semaphore")
print("12. return_exceptions=True or one bad service kills the batch")
print("13. WAITING + thousands -> asyncio . WAITING + hundreds -> threads")
print("14. CALCULATING -> processes . asyncio does NOT help CPU work")
print()
print("bye")
