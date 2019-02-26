# fuse abstraction layer

# General

This is a simple abstraction layer framework based on a virtual filesystem with fuse written in python. Basicly the framework enables running one or multiple independent modules to create an abstraction layer for any kind of task. For each module it creates specified virtual character files in the filesystem. Each read and each write is delegated to the specific module, which then can take any action (e.g. do a complicated calculation) and return some data. Therefore each user on the system can interact with the virtual character files as normal files without specific knowledge about the implementation behind. See the examples below for concrete usage of this framework.

# Definitions

## Abstraction Layer

The framework is an abstraction layer for any possible task, so whenever i say abstraction layer, i mean this framework. It is supposed to act like a kernel abstraction (e.g. invoke native drivers), which is useful if you don't want to write own drivers for specific hardware or to edit the native drivers source code. The usecase is not restricted  to kernel abstraction. You can use it for anything you want to use.

The abstraction layer is able to run several modules. For each module it creates specified (by the module) virtual character devices. This happens in a virtual filesystem (fuse) which is mounted in the root file system.  

Any read and any write to a virtual character device is registered and get's delegated to the according module. The module can take any action and only must return some data (Interface definition)

## Module

A module is a component which is integrated in the abstraction layer. When the abstraction layer is started, it initializes each module and delegates read and write events to the module. Basicly the abstraction layer is a runtime environment for all modules. A module specifies a folder name, which then appears in the virtual filesystem. Further more, there can be multiple files defined by a module, which are shown as the virtual character devices inside the modules folder. 

A module can implement any reasonable logic. Starting from a simple hello world module, you can write complex applications with several dependencies. Everything happens in userspace, so if there is a missing a dependenciy, you simply install it (instead of compiling and loading new kernel modules).

# Work todo

# References
Fuse, fusepy, etc.

