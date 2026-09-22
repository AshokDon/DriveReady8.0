# Java OOP & Advanced Concepts --- Tutorial Collection

This folder contains a polished, structured version of the 13 Java OOP,
concurrency, generics, collections, streams, and exception-handling
tutorials.

## Learning Path

  -----------------------------------------------------------------------
  \#                      Tutorial                Main Topics
  ----------------------- ----------------------- -----------------------
  01                      LLD Introduction        HLD vs LLD, scaling,
                                                  entities, OOP thinking

  02                      Classes & Objects       classes, objects,
                                                  references,
                                                  constructors, `this`,
                                                  `static`, encapsulation

  03                      Access & Inheritance    access modifiers,
                                                  `final`, immutability,
                                                  copying, inheritance,
                                                  `Object`

  04                      Polymorphism &          overriding,
                          Interfaces              overloading, abstract
                                                  classes, interfaces,
                                                  composition

  05                      OOP Lab                 Library Management
                                                  System

  06                      Concurrency-1           processes, threads,
                                                  scheduling, `Runnable`

  07                      Concurrency-2           executors, thread
                                                  pools, `Callable`,
                                                  `Future`

  08                      Concurrency-3           race conditions,
                                                  critical sections,
                                                  synchronization

  09                      Concurrency-4           semaphores, permits,
                                                  bounded buffers

  10                      Generics & Collections  generics, bounds,
                                                  wildcards, collections

  11                      Collections Lab         inventory,
                                                  `Comparable`,
                                                  `Comparator`,
                                                  `HashSet`, LRU-style
                                                  list

  12                      Streams & Lambdas       functional interfaces,
                                                  lambdas, streams,
                                                  `Optional`

  13                      Exceptions & Advanced   exception handling,
                          Java                    custom exceptions,
                                                  streams in services
  -----------------------------------------------------------------------

## Recommended Order

``` text
LLD
 |
 v
OOP Foundations
 |
 v
Inheritance + Polymorphism
 |
 v
OOP Lab
 |
 v
Concurrency
 |
 v
Generics + Collections
 |
 v
Streams + Lambdas
 |
 v
Exception Handling
```

## Teaching Pattern

Every tutorial follows the same learning structure:

``` text
Concept
   ↓
Mental Model
   ↓
Java Syntax
   ↓
Working Example
   ↓
Common Mistakes
   ↓
Interview Questions
   ↓
Practice
```

## Code Style

All Java snippets use fenced Markdown code blocks:

``` java
public class Example {
    public static void main(String[] args) {
        System.out.println("Hello Java");
    }
}
```

This makes the material easy to read in GitHub, HackMD, VS Code,
Obsidian, and other Markdown editors.
