.. _examples:


Code Examples
===============

Provide some simple code examples to showcase the language’s functionality. Link to more examples if needed.

.. note::

   **Extension:** file_name.flint

   **Single-comments:** // this is a single line Comments
   
   **Multi-comments:** /* this is a multi-line comment */

Code Examples
--------------

Here are some simple Flint code examples:

**Variables declaration and printing:**  

.. code-block:: 

    var greeting = "Hello, Flint!";
    print greeting;     // prints: Hello, Flint!

**Simple arithmetic operations:**

.. code-block:: 

    var a = 10;
    var b = 20;
    var sum = a + b;
    print sum;        // prints: 30

**Conditional statements:**

.. code-block:: 

    var a = 10;
    var b = 20;
    if (a > b) {
        print "a is greater than b";
    } else {
        print "b is greater than a";
    }

**Loops:**

1. **while loop:**

.. code-block::

    var i = 0;
    while (i < 5) {
        print i;
        i = i + 1;
    }

2. **for loop (while loop with syntactic sugar):**

.. code-block::

    for (var i = 0; i < 5; i = i + 1) {
        print i;
    }

**Functions:**

.. code-block::

    fn add(a, b) {
        return a + b;
    }

    var sum = add(10, 20);  // function call
    print sum;

**Recursion:**

.. code-block::

    fn factorial(n) {
        if (n == 0) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }

    var result = factorial(5);
    print result;

