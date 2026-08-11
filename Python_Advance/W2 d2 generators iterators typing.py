'''
The Story Swiggy's 8 GB Order Log

every night swiggy writes one log file . every order , one line

    ORD-1001|450|SUCCESS
    ORD-1002|320|FAILED
    ORD-1003|780|SUCCESS
    ...

by friday the file is 8 GB . 40 million lines

monday morning the analytics team needs one number

        "how many payments FAILED yesterday ?"

a developer writes the obvious code


    def read_orders(filename):
        f = open(filename)
        lines = f.readlines()          <- read the whole file
        f.close()
        return lines

    orders = read_orders("orders.log")
    for line in orders:
        ...


it worked perfectly on his laptop with the 200 line test file

on the server it printed

        MemoryError

the laptop had 16 GB . the file is 8 GB . but python needs about
5 times that to hold 40 million string objects

the job died . nobody got the number


now the important question


First Principle Thinking
Ask your self

Q1) to COUNT the failed orders , how many lines do we need
    in memory at the same time ?

    ONE.
    read a line , check it , throw it away , read the next
    we never need line 5 and line 4000000 together

Q2) then why did we load all 40 million ?

    because readlines() gives us a LIST
    and a list means "everything , right now , all in memory"

    we asked for the wrong shape of answer

Q3) what if a function could give us ONE line , then PAUSE ,
    and continue only when we ask for the next one ?

    a normal function cannot do that
    a normal function runs to the end and returns ONCE

Q4) and a second problem . that code says f.close()
    what happens if the loop crashes before reaching it ?

    hold that question . part 2 of this file is about exactly that

'''

import sys
import tracemalloc
import itertools
from time import time
from contextlib import contextmanager


#=============================================================================#
#                    PART 1  --  GENERATORS AND ITERATORS                     #
#=============================================================================#

#-----------------------------vocabulary---------------------------------------#
'''
you have written  for x in something  a thousand times
you never asked HOW the for loop actually works

it is two steps , and python does them for you

    1. it asks the object   "give me an iterator"     -> __iter__
    2. then again and again "give me the next item"   -> __next__
    3. when there is nothing left the iterator raises StopIteration
       and the for loop quietly stops

lets do it BY HAND once . after this the for loop is never mysterious again
'''

menu = ["dosa", "idli", "vada"]

it = iter(menu)                       # step 1 . ask for an iterator
print("manual next 1 :", next(it))    # step 2 . ask for items one by one
print("manual next 2 :", next(it))
print("manual next 3 :", next(it))

try:
    next(it)                          # step 3 . nothing left
except StopIteration:
    print("manual next 4 : StopIteration . the for loop stops here")

'''
so this

        for item in menu:
            print(item)

is really this

        it = iter(menu)
        while True:
            try:
                item = next(it)
            except StopIteration:
                break
            print(item)


TWO WORDS THAT PEOPLE MIX UP

    ITERABLE   something you CAN loop over        list , str , dict , file
    ITERATOR   the thing doing the counting       remembers where it is

a list is iterable but it is NOT an iterator . calling iter() gives you one

ONE SENTENCE THAT MATTERS

        AN ITERATOR REMEMBERS ITS POSITION AND HANDS OUT ONE ITEM AT A TIME

that is the whole cure for the 8 GB file
'''


#-----------------------------idea 1 ------------------------------------------#
'''
RETURN A LIST . this is what swiggy had
'''


def get_order_amounts_list(count):
    result = []
    for i in range(count):
        result.append(i * 10)
    return result                     # everything , at once , in memory


print()
print("IDEA 1 : return a list")

small = get_order_amounts_list(5)
print("   small file works fine :", small)

tracemalloc.start()
big = get_order_amounts_list(2000000)
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"   2 million orders     : {peak / 1024 / 1024:.1f} MB of RAM")
print("   size of the list     :", sys.getsizeof(big), "bytes")

del big

'''
it works . it is readable . nothing is wrong with this code
for 5 orders it is perfect

for 2 million it eats 77 MB
for 40 million it kills the server

and remember Q1 -> we only ever needed ONE line at a time
'''


#-------------------------> Idea 2 <-------------------------------------------#
'''
WRITE YOUR OWN ITERATOR

we now know the rules . __iter__ gives an iterator , __next__ gives one item
so lets build a class that hands out one order at a time
'''


class OrderAmounts:
    def __init__(self, count):
        self.count = count
        self.i = 0                    # remember our position

    def __iter__(self):
        return self                   # i am my own iterator

    def __next__(self):
        if self.i >= self.count:
            raise StopIteration       # tell the for loop to stop
        value = self.i * 10
        self.i = self.i + 1           # move the position
        return value                  # ONE item . then we pause


print()
print("IDEA 2 : your own iterator class")

for amount in OrderAmounts(5):
    print("   ", amount)

tracemalloc.start()
total = 0
for amount in OrderAmounts(2000000):
    total = total + amount
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"   2 million orders     : {peak / 1024:.2f} KB of RAM")
print("   total                :", total)

'''
77 MB became less than 1 KB . the memory problem is SOLVED

we never hold more than one number at a time


BUT look at the cost

    the real logic   ->  value = self.i * 10          1 line
    the boilerplate  ->  __init__ , __iter__ ,
                         __next__ , self.i , raise    9 lines

we wrote 9 lines of machinery to hand out ONE number
and every new iterator needs all 9 again
'''


#-------------------------> Idea 3 <-------------------------------------------#
'''
YIELD . python writes those 9 lines for you

put the word yield in a function and python turns it into an iterator
automatically . __iter__ , __next__ , the position , StopIteration . all of it

    return    gives a value and the function is FINISHED
    yield     gives a value and the function PAUSES , keeping everything
              exactly where it was , waiting to be asked again

that is the answer to Q3
'''


def order_amounts(count):
    for i in range(count):
        yield i * 10                  # give one , then PAUSE here


print()
print("IDEA 3 : yield")

for amount in order_amounts(5):
    print("   ", amount)

tracemalloc.start()
total = 0
for amount in order_amounts(2000000):
    total = total + amount
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"   2 million orders     : {peak / 1024:.2f} KB of RAM")
print("   total                :", total)

'''
same memory as the class . TWO LINES instead of eleven

    class version   11 lines
    yield version    2 lines
    same result , same memory


WATCH THE PAUSE HAPPEN . this is the part people do not believe
'''


def noisy_orders():
    print("      >> starting")
    yield 10
    print("      >> woke up after the first yield")
    yield 20
    print("      >> woke up after the second yield")
    yield 30
    print("      >> finished")


print()
print("proof that it PAUSES :")
g = noisy_orders()
print("   generator created . notice NOTHING printed yet")
print("   asking for item 1 :", next(g))
print("   asking for item 2 :", next(g))
print("   asking for item 3 :", next(g))

'''
read that output carefully

creating the generator ran NO code at all
each next() runs the function only until the next yield , then freezes it

the function is sleeping in the middle of itself , holding its variables
that is impossible for a normal function . that is the whole feature
'''


#-----------------------------the #1 beginner mistake--------------------------#
'''
A GENERATOR IS USED UP . you can only go through it ONCE
'''


def three_orders():
    yield "ORD-1"
    yield "ORD-2"
    yield "ORD-3"


g = three_orders()

print()
print("first  loop :", end=" ")
for o in g:
    print(o, end=" ")
print()

print("second loop :", end=" ")
for o in g:
    print(o, end=" ")            # nothing . it is exhausted
print("(EMPTY . the generator is used up)")

'''
a LIST you can loop 100 times . a GENERATOR only once

why ? the iterator remembered its position and that position is now at the end
there is nothing to rewind

    len(g)      does not work
    g[0]        does not work
    sum(g) then max(g)   the second one gets nothing

if you need it twice , either
    call the function again  ->  three_orders()
    or make a list           ->  orders = list(three_orders())

but if you are making a list , ask yourself why you used a generator
'''


#-------------------------> Idea 4 <-------------------------------------------#
'''
GENERATOR EXPRESSION . one character difference

    [x * 10 for x in range(n)]     SQUARE brackets -> builds a LIST . all of it
    (x * 10 for x in range(n))     ROUND brackets  -> a GENERATOR . one at a time

that is it . one character
'''

print()
print("IDEA 4 : square brackets vs round brackets")

as_list = [x * 10 for x in range(100000)]
as_gen = (x * 10 for x in range(100000))

print("   list      :", sys.getsizeof(as_list), "bytes")
print("   generator :", sys.getsizeof(as_gen), "bytes")
print("   both give the same answer :", sum(as_list) == sum(x * 10 for x in range(100000)))

'''
800 thousand bytes versus 192 bytes . for the SAME numbers

RULE
    if you are going to loop over it once and throw it away -> round brackets
    if you need to keep it , index it , loop twice          -> square brackets

    sum(x for x in data)        good . never builds a list
    sum([x for x in data])      wasteful . builds the whole list first
'''


#-------------------------> Idea 5 <-------------------------------------------#
'''
THE PIPELINE . this is where generators become beautiful

each generator takes a generator and gives a generator
nothing is stored . data flows through like water in a pipe

lets solve the ACTUAL swiggy problem now
'''

FAKE_LOG = [
    "ORD-1001|450|SUCCESS",
    "ORD-1002|320|FAILED",
    "ORD-1003|780|SUCCESS",
    "bad line with no pipes",
    "ORD-1004|150|FAILED",
    "ORD-1005|900|SUCCESS",
    "ORD-1006|250|FAILED",
]


def read_lines(lines):
    for line in lines:
        yield line.strip()


def keep_valid(lines):
    for line in lines:
        if line.count("|") == 2:
            yield line


def parse(lines):
    for line in lines:
        order_id, amount, status = line.split("|")
        yield {"id": order_id, "amount": int(amount), "status": status}


def only_failed(orders):
    for order in orders:
        if order["status"] == "FAILED":
            yield order


print()
print("IDEA 5 : the pipeline")

# build the pipe . NOTHING has run yet
pipe = only_failed(parse(keep_valid(read_lines(FAKE_LOG))))
print("   pipeline built . no line has been read yet")

failed_count = 0
lost_money = 0
for order in pipe:
    failed_count = failed_count + 1
    lost_money = lost_money + order["amount"]
    print("   failed :", order["id"], "Rs", order["amount"])

print("   total failed  :", failed_count)
print("   money at risk : Rs", lost_money)

'''
        FAKE_LOG -> read_lines -> keep_valid -> parse -> only_failed -> for loop
                       one          one         one        one           one
                       line         line        line       line          line

at any moment there is exactly ONE line in memory

this works identically on a 200 line file and on an 8 GB file
change FAKE_LOG to open("orders.log") and the code does not change at all

that is the real power . not speed . SHAPE
each step does one small thing and you can test each one alone
'''


#-----------------------------itertools----------------------------------------#
'''
python ships a box of ready made generators . import itertools

these are the five you will actually use
'''

print()
print("itertools :")

# islice -> take only the first n . works on infinite things
print("   islice   :", list(itertools.islice(order_amounts(1000000), 5)))

# chain -> glue several iterables into one stream
monday = ["ORD-1", "ORD-2"]
tuesday = ["ORD-3"]
print("   chain    :", list(itertools.chain(monday, tuesday)))

# count -> numbers forever . never ends
counter = itertools.count(start=100, step=1)
print("   count    :", next(counter), next(counter), next(counter))

# cycle -> repeat forever . used for round robin
riders = itertools.cycle(["ravi", "sita", "arjun"])
print("   cycle    :", next(riders), next(riders), next(riders), next(riders))

# groupby -> group NEIGHBOURING equal items
statuses = ["SUCCESS", "SUCCESS", "FAILED", "FAILED", "FAILED", "SUCCESS"]
for status, group in itertools.groupby(statuses):
    print("   groupby  :", status, "appeared", len(list(group)), "times in a row")

'''
WARNING about groupby

it only groups items that are NEXT TO EACH OTHER
it is NOT the same as SQL group by

if the list is not sorted you get nonsense . sort it first , or use a dict

WARNING about count and cycle

they NEVER END . these will hang your machine

        list(itertools.count())      never finishes
        for x in itertools.cycle(a)  never finishes

always cut them with islice or a break
'''


#=============================================================================#
#                     PART 2  --  CONTEXT MANAGERS                            #
#=============================================================================#
'''
this pays off Q4 from the top

        f = open("orders.log")
        lines = f.readlines()
        f.close()               <- what if the line above crashes ?

if readlines() raises , close() never runs . the file stays open

one leaked file is nothing . a server leaking one per request runs out of
file handles in a few hours and stops accepting connections

remember the exceptions chapter . the reserved stock that was never released
same disease . cleanup that only happens when nothing goes wrong
'''


class FakeConnection:
    def __init__(self, name):
        self.name = name
        self.closed = False

    def query(self, sql):
        if "BAD" in sql:
            raise ValueError("bad sql")
        return f"rows for {sql}"

    def close(self):
        self.closed = True


#-----------------------------idea 1 ------------------------------------------#
'''
OPEN AND CLOSE BY HAND
'''

print()
print("PART 2 . IDEA 1 : close by hand")

conn = FakeConnection("db-1")
result = conn.query("SELECT orders")
conn.close()
print("   happy path . closed ?", conn.closed)

conn2 = FakeConnection("db-2")
try:
    result = conn2.query("SELECT BAD")     # this raises
    conn2.close()                          # never reached
except ValueError:
    pass
print("   after error . closed ?", conn2.closed, "  <- LEAKED")

'''
the connection is still open and nobody holds a reference to it any more
it will sit there until the server dies
'''


#-------------------------> Idea 2 <-------------------------------------------#
'''
TRY / FINALLY . finally always runs , error or not
'''

print()
print("IDEA 2 : try / finally")

conn3 = FakeConnection("db-3")
try:
    result = conn3.query("SELECT BAD")
except ValueError:
    pass
finally:
    conn3.close()                          # ALWAYS runs
print("   after error . closed ?", conn3.closed, "  <- safe")

'''
correct . the leak is fixed

but now every single place that opens a connection must remember to write
try / finally . five lines of ceremony around one line of work
and the day someone forgets , the leak is back
'''


#-------------------------> Idea 3 <-------------------------------------------#
'''
WITH . make the object clean up after itself

two magic methods

    __enter__   runs when the with block STARTS . what it returns goes to "as"
    __exit__    runs when the with block ENDS . always . even on an exception
'''


class Connection:
    def __init__(self, name):
        self.name = name
        self.closed = False

    def __enter__(self):
        print(f"      opened {self.name}")
        return self                        # this is what "as conn" gets

    def __exit__(self, exc_type, exc_value, tb):
        self.closed = True
        print(f"      closed {self.name}")
        return False                       # False = let the error continue

    def query(self, sql):
        if "BAD" in sql:
            raise ValueError("bad sql")
        return f"rows for {sql}"


print()
print("IDEA 3 : with , using __enter__ and __exit__")

with Connection("db-4") as conn:
    print("   ", conn.query("SELECT orders"))

print("   now with an error inside :")
try:
    with Connection("db-5") as conn:
        conn.query("SELECT BAD")
except ValueError as e:
    print("    error escaped correctly :", e)

'''
look at the second one . "closed db-5" still printed
the cleanup happened , THEN the error carried on to us

the three arguments of __exit__ are the exception details
on success they are all None . on failure they hold the error

    return False   the error keeps travelling      <- what you want
    return True    the error is SWALLOWED silently <- almost never what you want

that True is the same trap as  except: pass  from the exceptions chapter
'''


#-------------------------> Idea 4 <-------------------------------------------#
'''
@contextmanager . a context manager written as a generator

remember yield PAUSES a function ?
that is exactly what a with block needs

        everything before yield  ->  setup     (__enter__)
        the yield itself         ->  hand control to the with block
        everything after yield   ->  cleanup   (__exit__)

this is why part 1 came first . the two topics are the same idea
'''


@contextmanager
def timer(label):
    start = time()
    print(f"      {label} started")
    try:
        yield                              # the with block runs HERE
    finally:
        end = time()
        print(f"      {label} took {end - start:.3f} s")


print()
print("IDEA 4 : @contextmanager , the Timer you were asked to build")

with timer("loading menu"):
    total = 0
    for i in range(300000):
        total = total + i

print("   and it still times things that fail :")
try:
    with timer("failing job"):
        raise ValueError("something broke")
except ValueError:
    pass

'''
6 lines and you have a reusable Timer

the try / finally around the yield is what makes it safe
without finally , a crash inside the with block would skip your cleanup


COMPARE THE TWO WAYS

    class with __enter__ / __exit__      more code , but the object can hold
                                         state and be reused

    @contextmanager                      short , reads top to bottom , best
                                         for simple setup / cleanup

use @contextmanager unless you need a real object
'''


#-----------------------------the file line reader-----------------------------#
'''
now both halves together . the actual thing you were asked to build
a generator that reads a file line by line , with guaranteed closing
'''


def read_file_lines(filename):
    with open(filename) as f:              # guaranteed close
        for line in f:                     # a file is ALREADY a generator
            yield line.rstrip("\n")        # one line , then pause


# make a small file to prove it
with open("/tmp/orders_demo.log", "w") as f:
    for line in FAKE_LOG:
        f.write(line + "\n")

print()
print("file line reader :")
for line in read_file_lines("/tmp/orders_demo.log"):
    print("   ", line)

print()
print("and the whole pipeline on a REAL file :")
pipe = only_failed(parse(keep_valid(read_file_lines("/tmp/orders_demo.log"))))
for order in pipe:
    print("    failed :", order["id"], "Rs", order["amount"])

'''
that function handles a 200 line file and an 8 GB file with the SAME code
and the same memory . the story at the top is now solved

NOTE -> a file object is already a generator of lines
        for line in f    reads one line at a time , always
        f.readlines()    reads ALL of them . that was the original bug
'''


#=============================================================================#
#                        PART 3  --  TYPE HINTS                               #
#=============================================================================#
'''
a different problem now

        def apply_discount(order, percent):
            return order - percent

what is order ? a number ? a dict ? an Order object ?
what is percent ? 10 or 0.10 ?

the only way to know is to read the whole function . or guess

six months later someone passes a string . it crashes in production
'''


def apply_discount_unclear(order, percent):
    return order - percent


print()
print("PART 3 . IDEA 1 : no hints")
print("   works :", apply_discount_unclear(500, 50))
try:
    print(apply_discount_unclear("500", 50))
except TypeError as e:
    print("   crashes at RUNTIME :", e)

'''
python found the bug . but only when that line finally ran
maybe in a rare branch . maybe on a friday night
'''


#-------------------------> Idea 2 <-------------------------------------------#
'''
TYPE HINTS . write down what you meant

        def apply_discount(order: float, percent: float) -> float:

read it as
        order is a float , percent is a float , it gives back a float

IMPORTANT -> python does NOT check these . they are notes , not rules
             the checking is done by a separate tool called mypy
'''


def apply_discount(order: float, percent: float) -> float:
    return order - percent


print()
print("IDEA 2 : with hints")
print("   works        :", apply_discount(500, 50))
print("   python STILL allows a string :", end=" ")
try:
    print(apply_discount("500", 50))
except TypeError:
    print("crashes , the hint did not stop it")

print("   the hints are just stored :", apply_discount.__annotations__)

'''
so what did we gain if python ignores them ?

    1. your editor autocompletes and warns you as you type
    2. mypy reads them and finds the bug BEFORE you run anything
    3. the next developer knows what to pass without reading the body
    4. they never go stale like a comment does

run   mypy yourfile.py   and it prints

        error: Argument 1 has incompatible type "str" ; expected "float"

this is the same move as the interfaces chapter
        move the error from the customer to the developer
'''


#-----------------------------the common shapes--------------------------------#
'''
the hints you will actually write
'''

from typing import Optional


def get_names(orders: list[str]) -> list[str]:
    return orders


def get_prices(menu: dict[str, float]) -> float:
    total = 0.0
    for price in menu.values():
        total = total + price
    return total


def find_order(order_id: str) -> Optional[str]:
    '''Optional means it returns a str OR None . be honest about None'''
    if order_id == "ORD-1":
        return "found"
    return None


print()
print("common shapes :")
print("   list[str]        :", get_names(["dosa", "idli"]))
print("   dict[str, float] :", get_prices({"dosa": 120.0, "idli": 80.0}))
print("   Optional[str]    :", find_order("ORD-1"), "/", find_order("ORD-9"))

'''
    x: int                      one number
    x: str                      one string
    x: list[str]                a list of strings
    x: dict[str, float]         keys are str , values are float
    x: tuple[int, int]          exactly two ints
    x: Optional[str]            a str OR None
    def f() -> None:            returns nothing

Optional is the important one . if your function can return None , SAY SO
half of all None bugs come from a function that quietly returned None
'''


#-------------------------> Idea 3 <-------------------------------------------#
'''
GENERICS . when the type depends on what you put in

a Stack of orders should give back orders
a Stack of names should give back names

writing OrderStack and NameStack separately is copy paste
we want ONE Stack that remembers what it holds

TypeVar means "some type . i do not know which yet . but it stays the same"
'''

from typing import TypeVar, Generic

T = TypeVar("T")                          # T is a placeholder for any type


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def size(self) -> int:
        return len(self._items)


print()
print("IDEA 3 : generics")

order_stack: Stack[str] = Stack()
order_stack.push("ORD-1")
order_stack.push("ORD-2")
print("   Stack[str] pop  :", order_stack.pop())

number_stack: Stack[int] = Stack()
number_stack.push(10)
number_stack.push(20)
print("   Stack[int] pop  :", number_stack.pop())

order_stack.push(999)                     # WRONG type . python allows it
print("   python allowed an int into Stack[str] :", order_stack.pop())

'''
that last line is the lesson

    python ran it happily . mypy would have refused

        error: Argument 1 to "push" of "Stack" has incompatible type "int"

TYPE HINTS ARE ONLY AS STRONG AS THE TOOL YOU RUN

    no mypy in your project -> hints are documentation
    mypy in your project    -> hints are enforcement , before the code runs

if your team writes hints but never runs mypy , you have paid the cost
and got none of the benefit
'''


#-----------------------------exceptions recap---------------------------------#
'''
custom errors were covered in their own file . the short version

    class SwiggyError(Exception): ...        one root for your whole app
    class RetryableError(SwiggyError): ...   timeout , 503 . try again
    class TerminalError(SwiggyError): ...    declined , no funds . never retry

put the retry POLICY in the class tree , not in an if/elif on messages

and the two rules that matter most
    never write   except: pass
    never write   return   inside a finally block
'''


#-----------------------------how to decide------------------------------------#
'''
WHEN DO I USE A GENERATOR ?

    use it when                              use a list when
    -------------------------------------    ----------------------------
    the data is big or endless               it is small and you know it
    you loop once and throw it away          you loop several times
    you are building a pipeline              you need len() or [0]
    you are reading a file                   you need to sort it
    the source is slow (network , disk)      you need it in memory anyway

    rule of thumb -> if you are about to write list(generator) ,
                     ask why you made a generator


WHEN DO I WRITE A CONTEXT MANAGER ?

    whenever something must be UNDONE . every time . no exceptions

    files          open   -> close
    connections    open   -> close
    locks          acquire-> release
    timers         start  -> stop
    transactions   begin  -> commit or rollback
    temp files     create -> delete

    if you find yourself writing try/finally twice , make it a with


ADVANTAGES OF GENERATORS
    + memory stays flat no matter how big the data is
    + you get the first result immediately , no waiting for all of it
    + they can be infinite
    + pipelines are easy to read and easy to test one stage at a time

DISADVANTAGES OF GENERATORS
    - single use . loop it twice and the second loop is empty
    - no len() , no indexing , no slicing
    - harder to debug . you cannot just print it to see what is inside
    - if you need the whole thing in memory anyway , a list is simpler


ADVANTAGES OF TYPE HINTS
    + the error moves from production to your editor
    + autocomplete actually works
    + documentation that cannot go stale
    + refactoring large code becomes far safer

DISADVANTAGES OF TYPE HINTS
    - python ignores them . useless without mypy in your build
    - they make simple code longer
    - complex types get ugly fast
    - a wrong hint is worse than no hint . it lies to the next reader
'''


#-----------------------------summary------------------------------------------#

print()
print("SUMMARY")
print("1.  for loop = iter() then next() until StopIteration")
print("2.  return finishes a function . yield PAUSES it")
print("3.  a generator holds ONE item , never the whole data")
print("4.  77 MB became 0.4 KB . same answer")
print("5.  a generator is single use . loop it twice and it is empty")
print("6.  [x for x in y] builds a list . (x for x in y) is a generator")
print("7.  chain generators into a pipeline . one item flows through")
print("8.  itertools has islice chain count cycle groupby . count never ends")
print("9.  __enter__ and __exit__ make your object work with  with")
print("10. __exit__ returning True SWALLOWS the error . return False")
print("11. @contextmanager turns a generator into a with block")
print("12. type hints are notes , not rules . mypy is what checks them")
print("13. Optional[str] means it can return None . say so honestly")
print("14. TypeVar + Generic = one class that remembers what it holds")
print()
print("bye")
