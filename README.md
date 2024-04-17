# Taskaratus!
Task-Apparatus (taskaratus) is a tool to automate running CLIs and other tasks
so you can build, iterate and ship your projects faster.

## Features
Taskapp provides you with the tools to automate boring tasks.
That's why it gives you the following tools:
- A structured way to declare your tasks
- Basic pattern matching for your routes
- File dependencies
    - Only recompute tasks when a file changes
    - Possibility to override this using `--force-recompute`
- Task dependencies
    - A task will first call a set of tasks before executing
    - If these tasks aren't recomputed this one won't recompute (W.I.P)
- Preludes to validate input when a task is run

## Taskaratus 101
This tool is cenetered around tasks organized as routes:

```
app
├─ deploy
├─ build
├─ dev
│  ├─ web
│  ├─ native
├─ format
backend
├─ ...
```

In this example, if you want to run your app as a web dev preview,
you would use the following syntax: `taskapp app dev web`

## Lingo
A "route" corresponds to a virtual location within the build system,
the "task" is an implementation associated to a route. A task has a specific implementation within the filesystem in the form of a python method in a file.

The term "route" refers to the path that will be used to identify the
task when invoking it, whereas in coding terms, the task is implemented
in a location that isn't mapped 1-to-1 to its route.

### Explanation
The task (and route) system is tied to where your implementation is
located.

These are the main things you should keep in mind:
- Each route may have one or multiple subroutes
- A task may only have one route associated with it
- A route may represent a "physical" directory or a task

```
build
deploy(catch)
    => pip
    => foo
        => bar
```

Here `build` is both a route and a task, its implementation
will be in `tasks/build.py`.

`deploy` is a `catch` route, meaning it "ends" the route tree:
each subsequent subroute's task will defined in `tasks/deploy.py`.
For instance, `bar`'s task definition would be defined using `@task(name="foo.bar)`.

## How to use
This repository uses Taskapp! Feel free to look at the examples.

### The root file

The structure of your taskapp project is defined in `task.app.yaml`.
This yaml file should contain the following fields:
```yaml
name: "..."
description: "..."

routes:
    - ...
```

### A simple project
Let's say you have a project that can be:
- Installed
    - User-only (local)
    - System wide (system)
- Compiled
    - For a specific target
        - Debug
        - Optimized (opt-level 1 by default)
        - Production
    - Default (debug)

Here what your routes would look like:
```yaml
routes:
    - install(catch):
        - local
        - system
    - compile(catch):
        - target:
            - debug
            - optimized:
                - "*"
            - production
```

Now what does catch mean?

Catch indicates that each subroute's task will be implemented in `tasks/x.py` or `tasks.install.py` in
the case of the install route.

Now, let's see what the implementation could look like, let's take a look at
`example/tasks/install.py`

Great! So now you've seen how we can make a simple script.

Let's now look at `example/tasks/compile.py`.

### More complex examples
...

W.I.P