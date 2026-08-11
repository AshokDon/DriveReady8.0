'''
The Story Swiggy's Slow Page . WHICH service is slow ?

last time we made the order page fast with threads
2.4 seconds became 0.4 seconds . everyone was happy

then one monday the page became slow again . 3 seconds

the manager asks a simple question

        "which of the six services is the slow one ?"

nobody knows . nothing is measured
so a developer adds timing to the menu service


    def get_menu(restaurant_id):
        start = time()                          <- added
        data = fetch_from_db(restaurant_id)
        end = time()                            <- added
        print("get_menu took", end - start)     <- added
        return data


3 extra lines . it works . they find the slow one . problem solved

then the manager says
        "good . now do it for ALL of them"

swiggy has 40 such functions

40 functions x 3 lines = 120 lines of copy pasted timing code

and one week later someone changes the log format . 40 edits
and one of those 40 was pasted wrong . it prints "get_menu"
inside get_reviews . for 3 months the dashboard blamed the wrong service


now the important question


First Principle Thinking
Ask your self

Q1) look at those 3 timing lines . do they have ANYTHING to do
    with menus ?

    No. nothing at all
    the menu code is 1 line . the timing code is 3 lines
    75 percent of that function is not about menus

Q2) if the same 3 lines appear in 40 functions , what should
    happen when the log format changes ?

    you should edit ONE place . not 40
    you already know this instinct . we used it in interfaces when
    the same if/elif was copied into 6 files

Q3) can i write the timing code ONCE , and somehow wrap it
    around any function i like ?

    that is exactly what a decorator is
    but before that we need to answer a stranger question

Q4) a function takes DATA and returns DATA
    5 goes in , 25 comes out

    can a function take a FUNCTION and return a FUNCTION ?

    hold that question . the whole topic depends on it

'''

import functools
from time import sleep, time


#-----------------------------vocabulary---------------------------------------#
'''
before decorators you must believe ONE thing

        IN PYTHON , A FUNCTION IS JUST AN OBJECT

same as an int , same as a list . it is a value you can move around

    x = 5              a number stored in a name
    f = greet          a FUNCTION stored in a name

four things you can do with any object , so you can do with a function

    1. store it in a variable
    2. put it in a list
    3. pass it into another function
    4. return it out of another function

number 3 and number 4 are the whole trick . lets prove all four
'''


def greet(name):
    return "hello " + name


# 1. store a function in a variable
say = greet                       # NOTE : no brackets . we are not calling it
print("1. stored  :", say("ashok"))

# 2. put functions in a list
def shout(name):
    return "HELLO " + name.upper()

funcs = [greet, shout]
print("2. in list :", funcs[1]("ashok"))

# 3. pass a function INTO a function
def call_twice(fn, value):
    return fn(value) + " | " + fn(value)

print("3. passed  :", call_twice(greet, "ashok"))


# 4. RETURN a function OUT of a function
def make_greeter(word):
    def inner(name):              # a function defined INSIDE a function
        return word + " " + name
    return inner                  # NOTE : no brackets . we return the function


hi = make_greeter("hi")
namaste = make_greeter("namaste")
print("4. returned:", hi("ashok"), "/", namaste("ashok"))

'''
look at number 4 carefully

make_greeter finished running . it is GONE
but hi still remembers word = "hi"
and namaste still remembers word = "namaste"

the inner function carries the outer variable with it
that is called a CLOSURE . it is why decorators can remember settings

    +-------- make_greeter("hi") --------+
    |   word = "hi"                      |
    |   +--------- inner ---------+      |
    |   |  uses word from outside |      |  <- inner carries "hi" with it
    |   +-------------------------+      |
    +------------------------------------+


ONE SENTENCE THAT MATTERS

        A FUNCTION CAN TAKE A FUNCTION AND RETURN A FUNCTION

that is the answer to Q4 . everything below is just that sentence
'''


#-----------------------------lambda-------------------------------------------#
'''
a lambda is a function with no name , written in one line
useful when the function is so small that naming it is silly
'''

double = lambda x: x * 2                    # same as def double(x): return x*2
print()
print("lambda     :", double(5))

# the real place you use lambda -> as a small argument to another function
orders = [("biryani", 250), ("dosa", 120), ("coke", 40)]

orders.sort(key=lambda item: item[1])       # sort by price
print("sorted     :", orders)

print("expensive  :", list(filter(lambda item: item[1] > 100, orders)))

'''
WARNING about lambda

a lambda can only hold ONE EXPRESSION . no if blocks , no loops , no prints

    lambda x: x * 2                 fine
    lambda x: print(x); return x    NOT allowed

so use lambda for tiny throwaway things like key= and filter()
for anything real use a normal def . python people prefer def
'''


#-----------------------------idea 1 ------------------------------------------#
'''
COPY PASTE THE TIMING . this is what swiggy had
'''


def get_menu(restaurant_id):
    start = time()                                  # timing
    sleep(0.3)                                      # the real work
    data = "menu-of-" + str(restaurant_id)
    end = time()                                    # timing
    print(f"   get_menu took {end - start:.2f} s")       # timing
    return data


def get_reviews(restaurant_id):
    start = time()                                  # timing again
    sleep(0.1)
    data = "reviews-of-" + str(restaurant_id)
    end = time()
    print(f"   get_reviews took {end - start:.2f} s")    # timing again
    return data


print()
print("IDEA 1 : copy pasted timing")
print("  ", get_menu(7))
print("  ", get_reviews(7))

'''
it works . the manager is happy

but count the lines
    real work   -> 2 lines
    timing      -> 4 lines

and this is only 2 functions . swiggy has 40

change the log format tomorrow -> 40 edits
paste it wrong once -> the dashboard lies for 3 months
'''


#-------------------------> Idea 2 <-------------------------------------------#
'''
PUT THE TIMING IN ONE FUNCTION

we know functions can be PASSED into functions
so lets write the timing once and hand it the function to run
'''


def get_menu_clean(restaurant_id):
    sleep(0.3)
    return "menu-of-" + str(restaurant_id)               # only the real work


def get_reviews_clean(restaurant_id):
    sleep(0.1)
    return "reviews-of-" + str(restaurant_id)


def measure(fn, arg):
    start = time()
    result = fn(arg)                                     # run whatever we got
    end = time()
    print(f"   {fn.__name__} took {end - start:.2f} s")
    return result


print()
print("IDEA 2 : one timing function")
print("  ", measure(get_menu_clean, 7))
print("  ", measure(get_reviews_clean, 7))

'''
BIG improvement

    before                              after
    timing code in 40 functions         timing code in 1 function
    change format = 40 edits            change format = 1 edit
    get_menu is 6 lines                 get_menu is 2 lines

the functions are clean again . they only do their own job


BUT look at what we broke

    before ->   get_menu(7)
    now   ->    measure(get_menu_clean, 7)

EVERY CALLER in the whole codebase must change
and if one caller forgets , that call is simply not measured . silently

we moved the mess . we did not remove it
'''


#-------------------------> Idea 3 <-------------------------------------------#
'''
THE TRICK . give back a FUNCTION instead of a result

what if measure did not RUN the function
what if it returned a NEW function that runs it with timing inside

then we can put that new function back under the OLD NAME
and every caller keeps working exactly as before
'''


def measure(fn):                       # takes a function
    def wrapper(arg):                  # builds a new function
        start = time()
        result = fn(arg)               # closure . wrapper remembers fn
        end = time()
        print(f"   {fn.__name__} took {end - start:.2f} s")
        return result
    return wrapper                     # returns the new function


def get_menu(restaurant_id):
    sleep(0.3)
    return "menu-of-" + str(restaurant_id)


get_menu = measure(get_menu)           # <-- THE WHOLE IDEA IS THIS LINE

print()
print("IDEA 3 : rebind the name")
print("  ", get_menu(7))               # caller did NOT change

'''
read that line again

        get_menu = measure(get_menu)

we took get_menu , wrapped it , and put the wrapper back in the SAME NAME

so anyone calling get_menu(7) now gets timing for free
they did not change . they do not even know

    get_menu  --->  wrapper  --->  original get_menu
                    (timing)       (the real work)

this is a decorator . you have already written one


small problem left . that rebinding line sits at the BOTTOM of the file
far away from the function . easy to miss , easy to forget
'''


#-------------------------> Idea 4 <-------------------------------------------#
'''
THE @ SYMBOL

python gives us shorter way to write that same line

        @measure
        def get_menu(...):

means EXACTLY

        get_menu = measure(get_menu)

nothing more . no magic . it is the same line , moved to the top
where you can see it
'''


def measure(fn):
    def wrapper(arg):
        start = time()
        result = fn(arg)
        end = time()
        print(f"   {fn.__name__} took {end - start:.2f} s")
        return result
    return wrapper


@measure                               # same as get_offers = measure(get_offers)
def get_offers(restaurant_id):
    sleep(0.2)
    return "offers-of-" + str(restaurant_id)


print()
print("IDEA 4 : the @ symbol")
print("  ", get_offers(7))

'''
that is a DECORATOR

        A DECORATOR IS A FUNCTION THAT TAKES A FUNCTION
        AND RETURNS A NEW FUNCTION

the @ is only shorthand for   name = decorator(name)

now the timing lives in ONE place
adding it to a 41st function is ONE line , not 3
'''


#-----------------------------works on any function----------------------------#
'''
our wrapper only accepts ONE argument . real functions take anything

        def pay(amount, method, coupon=None)

so the wrapper must accept ANY arguments and pass them through

        *args     catches any normal arguments  -> a tuple
        **kwargs  catches any keyword arguments -> a dict

you do not need to understand them deeply . just remember

        the wrapper takes everything and passes everything along
'''


def measure(fn):
    def wrapper(*args, **kwargs):                  # accept anything
        start = time()
        result = fn(*args, **kwargs)               # pass it all along
        end = time()
        print(f"   {fn.__name__} took {end - start:.2f} s")
        return result
    return wrapper


@measure
def place_order(item, amount, coupon=None):
    sleep(0.1)
    if coupon:
        amount = amount - 50
    return f"{item} for Rs{amount}"


print()
print("works with any arguments :")
print("  ", place_order("biryani", 250))
print("  ", place_order("dosa", 120, coupon="FIRST50"))
print("  ", place_order(item="coke", amount=40))


#-----------------------------the problem nobody warns you about---------------#
'''
our decorator secretly damaged the function

remember what @measure really did

        place_order = measure(place_order)

place_order is no longer the function you wrote . it is wrapper
so its NAME and its DOCSTRING are wrappers name and docstring
'''


def broken_timer(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper


@broken_timer
def charge_customer(amount):
    """Charge the customer and return a transaction id."""
    return "TXN-1"


print()
print("WITHOUT functools.wraps")
print("   name     :", charge_customer.__name__)
print("   docstring:", charge_customer.__doc__)

'''
the name says "wrapper" . the docstring is gone

why this actually hurts you
    - error tracebacks say "wrapper" so you cannot find the real function
    - help(charge_customer) shows nothing
    - flask , django and pytest look at __name__ to route and to name tests
      two decorated functions both called "wrapper" and things break

THE FIX -> functools.wraps
one line , copies the name and docstring across
'''


def good_timer(fn):
    @functools.wraps(fn)               # <-- the fix . always add this
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper


@good_timer
def charge_customer(amount):
    """Charge the customer and return a transaction id."""
    return "TXN-1"


print("WITH functools.wraps")
print("   name     :", charge_customer.__name__)
print("   docstring:", charge_customer.__doc__)

'''
RULE -> every decorator you ever write gets @functools.wraps(fn)
        it costs one line . forget it and you lose your own function name
'''


#-----------------------------the #1 beginner mistake--------------------------#
'''
WHEN does the decorator body run ?

most people think "when i call the function"
it actually runs when python READS the def . before you call anything
'''


def noisy(fn):
    print("      >> decorator ran now , at def time")
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print("      >> wrapper ran now , at call time")
        return fn(*args, **kwargs)
    return wrapper


print()
print("watch the order :")
print("   about to define the function")


@noisy
def cancel_order(order_id):
    return "cancelled " + str(order_id)


print("   function is defined . not called yet")
print("   now calling it")
cancel_order(99)

'''
so the decorator body runs ONCE , when python reads the file
the wrapper runs EVERY time you call the function

that is why registries work . flask routes , pytest tests , django signals
all collect functions at import time using exactly this
'''


#-------------------------> Idea 5 <-------------------------------------------#
'''
DECORATORS WITH ARGUMENTS . this pays off Q4 from the top

we want to say

        @retry(times=3)
        def charge(...)

but @something means   charge = something(charge)
so retry(times=3) must ITSELF return a decorator

that means THREE layers . read it slowly

        retry(times=3)      returns ->  decorator
        decorator(fn)       returns ->  wrapper
        wrapper(*args)      runs    ->  the real function

it looks scary . it is just the same trick done twice
'''


def retry(times=3, delay=0.1):
    def decorator(fn):                        # layer 2 : the real decorator
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):         # layer 3 : the replacement
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    print(f"      attempt {attempt} failed : {e}")
                    if attempt == times:
                        raise                 # last try . give up honestly
                    sleep(delay)
        return wrapper
    return decorator                          # layer 1 gives back layer 2


calls = {"n": 0}


@retry(times=4)
def charge_gateway(amount):
    calls["n"] = calls["n"] + 1
    if calls["n"] < 3:
        raise ConnectionError("gateway timeout")
    return f"charged Rs{amount}"


print()
print("IDEA 5 : decorator with arguments")
print("  ", charge_gateway(450))
print("   total calls made :", calls["n"])

'''
the payment succeeded on attempt 3 . the caller never knew it failed twice

and notice the shape

        no arguments   ->  @measure          2 layers
        with arguments ->  @retry(times=3)   3 layers

that is the ONLY difference . one extra layer to hold the settings

TRAP -> if your decorator takes arguments you must always write the brackets

        @retry(times=3)     correct
        @retry              WRONG . fn gets passed in as "times"
'''


#-------------------------> Idea 6 <-------------------------------------------#
'''
CACHE . remember the answer instead of computing it again

if a function is slow and always gives the same answer for the same input
just remember it

python already wrote this decorator for you -> functools.cache
'''


def slow_fib(n):
    if n < 2:
        return n
    return slow_fib(n - 1) + slow_fib(n - 2)


@functools.cache                       # the ONLY line we added
def fast_fib(n):
    if n < 2:
        return n
    return fast_fib(n - 1) + fast_fib(n - 2)


print()
print("IDEA 6 : functools.cache")

start = time()
slow_fib(32)
end = time()
slow_time = end - start
print(f"   without cache : {slow_time:.3f} s")

start = time()
fast_fib(32)
end = time()
fast_time = end - start
print(f"   with cache    : {fast_time:.5f} s")
print(f"   times faster  : {slow_time / fast_time:.0f}x")
print("   cache info    :", fast_fib.cache_info())

'''
ONE LINE . thousands of times faster

why ? because the plain version repeats itself insanely

    slow_fib(32) makes about 7 MILLION calls in total
    slow_fib(2) alone runs 1.3 million times
    slow_fib(1) alone runs 2.1 million times

    the same tiny answers , recomputed millions of times

fast_fib computes each number ONCE and remembers it
33 real calls instead of 7 million . that is the whole gain


WHEN YOU CAN USE A CACHE

    same input always gives the same output      yes
    the function reads a database that changes   NO
    the function has a random number             NO
    the arguments are lists or dicts             NO . they must be hashable

functools.cache      remembers everything , forever
functools.lru_cache(maxsize=100)   remembers the last 100 only
'''


#-----------------------------build the three yourself-------------------------#
'''
now the three you were asked to write . all in one place
'''


# ---------- 1. TIMER ----------
def timer(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time()
        result = fn(*args, **kwargs)
        end = time()
        print(f"      [timer] {fn.__name__} took {end - start:.3f} s")
        return result
    return wrapper


# ---------- 2. RETRY ----------
def retry(times=3, delay=0.05):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    print(f"      [retry] attempt {attempt} failed : {e}")
                    if attempt == times:
                        raise
                    sleep(delay)
        return wrapper
    return decorator


# ---------- 3. CACHE (our own , to see how it works) ----------
def cache(fn):
    store = {}                              # closure . lives between calls

    @functools.wraps(fn)
    def wrapper(*args):
        if args in store:
            print(f"      [cache] HIT  for {args}")
            return store[args]
        print(f"      [cache] MISS for {args} . computing")
        result = fn(*args)
        store[args] = result
        return result
    return wrapper


@timer
@cache
def get_restaurant(restaurant_id):
    sleep(0.3)                          # pretend database call
    return "Paradise Biryani"


print()
print("USING ALL THREE")
print("   first call  :", get_restaurant(7))
print("   second call :", get_restaurant(7))     # cache hit . much faster


attempts = {"n": 0}


@timer
@retry(times=3)
def flaky_payment(amount):
    attempts["n"] = attempts["n"] + 1
    if attempts["n"] < 2:
        raise ConnectionError("network blip")
    return f"paid Rs{amount}"


print("   payment     :", flaky_payment(450))

'''
LOOK AT THE SECOND CALL of get_restaurant

    first  -> cache MISS -> 0.3 seconds
    second -> cache HIT  -> almost 0 seconds

we did not touch get_restaurant . we added two lines above it


STACKING ORDER MATTERS

        @timer
        @cache
        def get_restaurant(...)

python applies the CLOSEST one first . so it becomes

        get_restaurant = timer(cache(get_restaurant))

    timer is OUTSIDE  -> it measures the cache lookup too . GOOD
    if you swap them  -> cache is outside , timer never runs on a hit

read decorators BOTTOM UP
'''


#-----------------------------where you already meet them----------------------#
'''
you have used decorators for months without knowing

    @property                   makes a method look like an attribute
    @staticmethod               method that needs no self
    @classmethod                method that receives cls
    @abstractmethod             the interfaces file . remember ?
    @functools.wraps            fixes the name
    @functools.cache            remembers results

    flask       @app.route("/orders")        registers a url
    django      @login_required              blocks logged out users
    pytest      @pytest.fixture              sets up test data
    celery      @app.task                    makes a background job

all of them are the same one line

        name = decorator(name)


WHEN SHOULD YOU WRITE ONE ?

    write a decorator when the SAME wrapper code surrounds MANY functions
    and that code is NOT about what the function actually does

    good reasons        timing , retry , cache , logging , login check ,
                        counting calls , rate limiting , transactions

    bad reason          only one function needs it -> just write the code inside
                        the logic is different every time -> not a wrapper


ADVANTAGES
    + the wrapper code lives in ONE place . change it once
    + the real function stays clean and only does its own job
    + adding it to a new function is one line
    + you can turn it off by deleting one line
    + you can stack several

DISADVANTAGES
    - one more layer to read when you are debugging
    - tracebacks get longer
    - forget functools.wraps and you lose the function name
    - decorators with arguments take a while to get comfortable with
    - a badly written decorator breaks EVERY function that uses it
'''


#-----------------------------summary------------------------------------------#

print()
print("SUMMARY")
print("1.  a function is an object . store it , pass it , return it")
print("2.  a closure = inner function remembering the outer variable")
print("3.  a decorator takes a function and returns a new function")
print("4.  @measure is only short for   name = measure(name)")
print("5.  the wrapper uses *args and **kwargs so it fits any function")
print("6.  ALWAYS add @functools.wraps(fn) or you lose the name")
print("7.  the decorator body runs at def time . the wrapper at call time")
print("8.  decorator with arguments needs 3 layers , not 2")
print("9.  @retry needs brackets . @retry(times=3) not @retry")
print("10. stacked decorators apply bottom up . read them upwards")
print("11. functools.cache is free speed when input always gives same output")
print("12. lambda is a one expression function . use it only for tiny things")
print()
print("bye")
