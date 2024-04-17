from taskapp.task import Fail, prelude, task

# When `taskapp compile` is ran, the route matching
# engine acts as if there was a:
# - compile(catch):
#   - compile
# route. Try it yourself! You'll see that the same
# thing happens. This makes it trivial to have
# "default routes" so that you don't have to
# declare subroutes that have the same name as
# their parent.

@task("compile")
def default_build():
    return debug_build()


@task("target.debug")
def debug_build():
    print("Debug build!")
    return "debug"


@task("target.production")
def prod_build():
    print("Production build!")
    return "prod"


@task("target.optimized")
def optimized_build():
    return optimized()


def optimized(level: int = 1):
    return f"Optimized build at {level=}"

# This is the task's prelude, it is executed **before**
# the task is ran. As we'll see in another example,
# the `Prelude` class allows us to add some additional
# behavior to the way the task is ran. Here, `Fail`
# will cancel the task's execution.
@prelude(name="target.optimized.wildcard")
def opt_build_prelude(level: str):
    if not level in ["0", "1", "2", "3"]:
        return Fail(f'Invalid opt-level: "{level=}" must be either one of 0, 1, 2, 3')

# This correspond to the `taskapp target optimized *` route
# since there's only one wilard in that route, the function
# only takes one argument
@task("target.optimized.wildcard")
def optimized_build_any(level: str):
    return optimized(int(level))
