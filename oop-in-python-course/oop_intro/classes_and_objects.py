#Everything that you create in python is an object 
a = 10
name = "Ashok"

#name is an object created for str class , class will have 
#methods 

# Objects are made by classes. Classes are the blueprints for objects, meaning they describe what an object should look like. So, above, let's look at the `name` variable:

# - The `name` variable is assigned to a string object
# - the `str` class defines what each string object looks like

# These classes demonstrate some of Python's "built-in" classes, that we can use to create data structures like strings and ints. But we can also create our own classes, then create objects (also known as instances) from those classes:


print(type(name))
print(type(a))

l = [1]
print(type(l))

#objects are made by class , in python we have built in class
#you also creat you own classes they are user define classes
#class as a developer thing and objects are clint thing




#class which is blue print 
# Dog class describes what information ("attributes" or "data") and behaviours ("methods") every dog should have.
# First, lets create a very simple Dog class that has no data and just one behaviour
class Dog:
    #instance variables 
    # Now let's add some data to the Dog class, so each dog object (or "instance") can have a name and a breed:
    # __init__ is a special method that is ran only once when an object is instanciated (created). We can setup our object data in here
    def __init__(self,name,breed,owner):
        self.name = name
        self.breed = breed
        self.owner = owner #has a relation
    #instance method
    def bark(self):
        print("whoof whoof")

class Owner:
    def __init__(self,name, address):
        self.name = name
        self.address = address


#object is nothing but instance of a class

owner = Owner("Ashok","7/2 Peddapuram")

# Define a variable called `dog` and assign it to an instance of (or "an object made from") the Dog class.
dog1 = Dog("Leo","idea",owner) # object

print(dog1.owner.name)
dog1.bark()

# What is self?
# In Python, self is a special parameter that refers to the instance of the class (the object) you're working with. When you define a method within a class, the first parameter of that method is always self, by convention. This helps Python know that the method belongs to an instance of the class.

# Think of self as a way to refer to "this object" — the specific object that is calling the method. It gives each object its own set of attributes and allows access to methods that belong to it.

# Why Do We Need self?
# Without self, Python wouldn’t know which object you’re referring to when you use attributes or methods within a class. self ensures that each object can keep its own data separate and gives you a way to work with an object's attributes and methods.
