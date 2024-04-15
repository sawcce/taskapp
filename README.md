# Taskaratus!
Task-Apparatus (taskaratus) is a tool to automate running CLIs and other tasks
so you can build, iterate and ship your projects faster.

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
For instance, `bar`'s task definition would bear the name "foo_bar". 