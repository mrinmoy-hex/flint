.. Flint documentation master file, created by
   sphinx-quickstart on Mon Dec 23 18:16:03 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _home:


Flint Programming Language
===============================

.. image:: https://img.shields.io/github/stars/mrinmoy-hex/Flint?style=for-the-badge
   :target: https://github.com/mrinmoy-hex/Flint
   :alt: GitHub stars

.. image:: https://img.shields.io/github/commit-activity/m/mrinmoy-hex/Flint?style=for-the-badge
   :target: https://github.com/mrinmoy-hex/Flint/commits/master
   :alt: Commits Count

Flint is a dynamically-typed interpreted programming language created as a personal hobby project to explore and uncover the magic behind programming languages. Built with learning in mind, Flint is simple, lightweight, and ideal for quick prototyping. 

It offers an intuitive environment for experimenting with core programming concepts, making it perfect for those wanting to learn or test ideas without the complexity of more established languages. While Flint isn’t intended for professional use, it serves as an experimental playground to better understand the inner workings of programming languages. 

This documentation will guide you through Flint’s syntax, features, and examples to help you get started.


.. note::

   This project is under active development.


Key Features
------------

- **Variable Support**  

   Flint allows you to define and use variables with a simple syntax. Variables can hold different types of data, and their types are inferred automatically based on the assigned value. Example:
   
   .. code-block:: 

      var x = 10;  // Integer
      var name = "Flint";  // String


- **Function Declaration and Definition**

   Functions in Flint are declared and defined with a straightforward syntax. You can declare a function with its name, parameters. Function bodies are enclosed in braces, and the language supports both simple and advanced function signatures. 

   Example:

   .. code-block::

      fn add(a, b) {
         print a + b;
      }

   .. note::

      For now, Flint does not support function return types. All functions return `null` by default.

      For more information, see :ref:`examples`.


Contributing
-------------

I welcome you to contribute to the Flint project. You can contribute by:
   - reporting bugs, 
   - suggesting new features, 
   - or submitting pull requests.

If you like the project, give it a star on GitHub.

Github: `Flint <https://github.com/mrinmoy-hex/Flint>`_


Contents
---------

.. toctree::
   :maxdepth: 3
   
   usage
   examples
   modules

   

