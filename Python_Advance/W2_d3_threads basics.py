'''
THREADS AND PROCESSES  --  the basics first

before we go to the real problem let us understand
what a thread is , what a process is , and how to make them


start with something you already know

when you run  python myfile.py  what happens ?
windows / linux creates a PROCESS and gives it some memory
your code runs inside that process , line by line , one at a time

that "one at a time" is the thing we want to change today


THREE WORDS . get these right and everything else follows

PROGRAM   -> a file sitting on your disk . it is NOT running
             like a recipe written in a cookbook

PROCESS   -> a running instance of that program
             it has its OWN MEMORY . its own variables
             like a kitchen that is actually cooking that recipe

THREAD    -> a worker INSIDE a process
             all threads of a process SHARE the same memory
             like the cooks working inside that ONE kitchen


        +------------ PROCESS (own memory) -------------+
        |                                               |
        |    Thread-1      Thread-2      Thread-3       |
        |                                               |
        |        ----- SHARED VARIABLES -----           |
        |                                               |
        +-----------------------------------------------+


so far every program you have written had exactly ONE thread
python calls it the MAIN THREAD . today we make more of them


ONE SENTENCE TO REMEMBER

        THREADS SHARE MEMORY .  PROCESSES DO NOT

'''

import os
from threading import Thread, current_thread, active_count
from multiprocessing import Process, current_process
from time import sleep, time


#-----------------------------look at the main thread--------------------------#
'''
before making a new thread lets look at the one we already have
'''

print("thread name  :", current_thread().name)
print("threads alive:", active_count())
print("process id   :", os.getpid())

'''
MainThread . that is the one running your code right now
every print , every loop you have ever written ran on it
'''


#-----------------------------idea 1 ------------------------------------------#
'''
FIRST WAY TO MAKE A THREAD -> subclass Thread and write run()

rules
    1. your class must inherit from Thread
    2. the method MUST be named  run
    3. you start it with  start()  not  run()
'''


class Hello(Thread):
    def run(self):                 # must be named run
        for i in range(5):
            print("Hello")
            sleep(0.2)


class Hi(Thread):
    def run(self):                 # careful -> self , not slef
        for i in range(5):
            print("Hi")
            sleep(0.2)


if __name__ == "__main__":

    t1 = Hello()
    t2 = Hi()

    t1.start()                     # start() creates a NEW thread
    t2.start()

    t1.join()                      # wait for t1 to finish
    t2.join()                      # wait for t2 to finish

    print("both threads finished")

'''
run it 2 or 3 times . the Hello / Hi order KEEPS CHANGING

that is normal . that is what concurrency looks like
nobody promised you an order . the operating system decides


YOU MAY ALSO SEE SOMETHING LIKE THIS

        HiHello
        <blank line>

the two words got MIXED on one line . that is not a bug in your code

print() is actually TWO steps -> write the text , then write the newline
a thread can get paused in between those two steps
so Hi wrote its text , Hello jumped in and wrote its text , then the
newlines came after

this is your first look at a REAL problem with sharing
two threads touched the same thing (the screen) at the same time
and the result got corrupted

remember this feeling . later we fix it with a Lock


if you had NOT written the two join() lines then
"both threads finished" could print BEFORE the threads are done
'''


#-----------------------------start() vs run()---------------------------------#
'''
this is the mistake everyone makes once

    t.start()  ->  creates a NEW thread and calls run() inside it
    t.run()    ->  just calls the method normally . NO thread is created

the dangerous part -> t.run() still "works"
it prints the same output . it gives no error
it is just completely sequential . you get zero benefit and no warning
'''


class Counter(Thread):
    def __init__(self, name):
        super().__init__()         # MUST call this or python errors out
        self.tname = name

    def run(self):
        sleep(0.3)
        print("   ", self.tname, "done on ->", current_thread().name)


if __name__ == "__main__":

    print()
    print("using run()  (wrong) :")
    s = time()
    Counter("A").run()             # no thread . runs on MainThread
    Counter("B").run()
    print("     time:", f"{time() - s:.2f} s")

    print("using start() (right):")
    s = time()
    a, b = Counter("A"), Counter("B")
    a.start(); b.start()
    a.join(); b.join()
    print("     time:", f"{time() - s:.2f} s")

'''
look at the thread name printed in each case

run()   -> both say MainThread . 0.6 seconds . no threading happened
start() -> both say Thread-N   . 0.3 seconds . real threading

ALWAYS start() . NEVER run()
'''


#-----------------------------idea 2 ------------------------------------------#
'''
SECOND WAY TO MAKE A THREAD -> Thread(target=function)

no class needed . you just point the thread at a function
this is the way you will use 90 percent of the time
'''


def greet(name, times):
    for i in range(times):
        print("hello", name)
        sleep(0.2)


if __name__ == "__main__":

    print()
    t1 = Thread(target=greet, args=("ashok", 3))
    t2 = Thread(target=greet, args=("swiggy", 3))

    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("done")

'''
NOTE ON args  -> it must be a TUPLE

    args = ("ashok", 3)      correct , two arguments
    args = ("ashok",)        correct , ONE argument . see the comma
    args = ("ashok")         WRONG . that is just a string , not a tuple

that missing comma gives a confusing error . everyone hits it once
'''


#-----------------------------join() . what it really does---------------------#
'''
join() means -> "stop here and wait until this thread is finished"

without join the main thread runs ahead and finishes first
'''


def slow_task():
    sleep(0.5)
    print("   task finished")


if __name__ == "__main__":

    print()
    print("without join :")
    t = Thread(target=slow_task)
    t.start()
    print("   main thread reached the end already")   # prints FIRST
    t.join()                                          # cleanup so output is clean

    print("with join :")
    t = Thread(target=slow_task)
    t.start()
    t.join()
    print("   main thread waited properly")           # prints SECOND

'''
so join is how you say "I need the result , wait for it"

useful checks you also get

    t.is_alive()   -> True while still running
    t.name         -> readable name , very useful in logs
'''


#-------------------------> now the real example <-----------------------------#
'''
this is the code we started with . downloading 3 files

each download WAITS 0.5 seconds for the network
3 files , one after another = 1.5 seconds
'''


def Download(file_name):
    print("   downloading ...", file_name)
    sleep(0.5)                              # this is the WAITING part
    print("   download completed", file_name)


if __name__ == "__main__":

    files = ['video.mp4', 'image.png', 'data.csv']

    # ---------- way 1 : one after another ----------
    print()
    print("SEQUENTIAL :")
    start = time()
    for f in files:
        Download(f)
    seq_time = time() - start               # keep it in its OWN variable
    print("sequential time :", f"{seq_time:.2f} s")

    # ---------- way 2 : all at the same time ----------
    print()
    print("THREADED :")
    threds = []
    for f in files:
        t = Thread(target=Download, args=(f,))
        threds.append(t)

    start = time()
    for t in threds:
        t.start()                           # start ALL first
    for t in threds:
        t.join()                            # then wait for ALL
    thread_time = time() - start
    print("threaded time   :", f"{thread_time:.2f} s")

    print()
    print("sequential :", f"{seq_time:.2f} s")
    print("threaded   :", f"{thread_time:.2f} s")
    print("speedup    :", f"{seq_time / thread_time:.1f}x")

'''
1.5 seconds  ->  0.5 seconds

WHY ?
because the three 0.5 second WAITS happened AT THE SAME TIME
instead of one after another

we did not make the internet faster
we just stopped standing in a queue to wait

sequential                      threaded
-----------------------------------------------------
wait 0.5 for video.mp4          all three start together
wait 0.5 for image.png          all three wait together
wait 0.5 for data.csv           all three finish together
total = 1.5 s                   total = 0.5 s


A MISTAKE THAT IS EASY TO MAKE HERE

if you write the sequential timing and then reuse the same variable
names start and end for the threaded part , you lose the first result

        start = time()
        for f in files: Download(f)
        end = time()            <- this value gets overwritten below
        ...
        start = time()          <- overwritten here
        ...
        end = time()
        print(end - start)      <- only prints the THREADED time

you never see 1.5 seconds . you only see 0.5 and cannot compare
that is why above we saved it as seq_time and thread_time
'''


#-----------------------------the other big mistake----------------------------#
'''
start() and join() inside the SAME loop
it looks correct and it gives you ZERO benefit
'''

if __name__ == "__main__":

    print()
    start = time()
    for f in files:
        t = Thread(target=Download, args=(f,))
        t.start()
        t.join()                # WRONG . waits here before starting the next
    wrong_time = time() - start

    print("start+join in same loop :", f"{wrong_time:.2f} s", " no benefit")
    print("start all then join all :", f"{thread_time:.2f} s", " correct")

'''
join blocks . so you start one , wait for it , start next , wait for it
that is just a normal for loop with extra typing

RULE ->  START THEM ALL . THEN JOIN THEM ALL
'''


#-------------------------> now PROCESS <--------------------------------------#
'''
a PROCESS is a completely separate running program
it gets its own memory and its own python interpreter

good news -> the code looks almost identical to Thread

    Thread(target=fn, args=(x,))
    Process(target=fn, args=(x,))

    .start()  .join()   same

IMPORTANT -> multiprocessing MUST be inside

        if __name__ == "__main__":

on windows and mac python starts a child process by RE-IMPORTING your file
without the guard every child re runs your file and makes more children
forever . on linux it usually works anyway , which makes it a nasty bug
that only appears on your friends laptop
'''


def show_who_i_am(task):
    print("   ", task, "| process id:", os.getpid(),
          "| name:", current_process().name)


if __name__ == "__main__":

    print()
    print("THREADS -> same process id , different thread")
    ts = [Thread(target=show_who_i_am, args=(f"thread-{i}",)) for i in range(3)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()

    print()
    print("PROCESSES -> DIFFERENT process id each")
    ps = [Process(target=show_who_i_am, args=(f"process-{i}",)) for i in range(3)]
    for p in ps:
        p.start()
    for p in ps:
        p.join()

'''
look at the process id in the output

threads   -> all the SAME number . they live inside one process
processes -> all DIFFERENT numbers . each is its own program

that is the whole difference , visible on screen
'''


#-----------------------------memory is NOT shared-----------------------------#
'''
threads share memory . processes do not
here is the proof
'''

shared_list = []


def add_item(item):
    shared_list.append(item)


if __name__ == "__main__":

    print()
    shared_list.clear()
    t = Thread(target=add_item, args=("from thread",))
    t.start(); t.join()
    print("after THREAD  :", shared_list, " thread changed our list")

    shared_list.clear()
    p = Process(target=add_item, args=("from process",))
    p.start(); p.join()
    print("after PROCESS :", shared_list, " empty . the change was lost")

'''
the process did run . it did append
but it appended to ITS OWN COPY of the list , in its own memory
the parent never saw it

to send data between processes you need Queue , Pipe or Manager
we will not need that today . just remember the rule

        THREADS SHARE MEMORY .  PROCESSES DO NOT
'''


#-----------------------------quick comparison---------------------------------#
'''
                        THREAD                  PROCESS
    -------------------------------------------------------------
    memory              shared with others      its own private
    process id          same as parent          new one
    cost to create      cheap  (KB)             expensive (MB)
    starting speed      fast                    slow
    share a variable    yes , directly          no , must copy it
    if one crashes      can take down all       others keep running
    needs __main__      no                      YES
    good for            WAITING work            CALCULATING work


when do we use which ?

    your code is WAITING       -> use THREADS
    (network , downloads ,
     database , files , sleep)

    your code is CALCULATING   -> use PROCESSES
    (math , image resizing ,
     ML training , encryption)


we saw threads make 3 downloads 3x faster . downloads are WAITING work

but why does that rule exist ? why do threads NOT help calculating work ?
the answer is something called the GIL

that is the next file . first get comfortable with the code above
'''


#-----------------------------summary------------------------------------------#

if __name__ == "__main__":

    print()
    print("SUMMARY")
    print("1. program = file on disk , process = it running , thread = worker inside")
    print("2. threads SHARE memory , processes DO NOT")
    print("3. two ways to make a thread : subclass Thread , or Thread(target=fn)")
    print("4. always start() , never run()")
    print("5. join() = wait until this thread finishes")
    print("6. start ALL then join ALL . never start+join in one loop")
    print("7. args must be a tuple . one argument needs args=(x,) with comma")
    print("8. Process looks the same as Thread but needs __main__ guard")
    print("9. threads help WAITING work . 1.5s became 0.5s")
    print("10. why not for calculating work ? -> the GIL , next file")
    print()
    print("bye")
