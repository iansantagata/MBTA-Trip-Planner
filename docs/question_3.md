# Question 3

## Prompt

Extend your program again so the user can provide any two stops along the subway routes you listed for question 1.

The program should list a rail route you could travel from one stop to the other.  We aren't evaluating your solution on the efficiency or cleverness of your route-finding mechanism.  Pick a simple solution that answers the question.  We will want you to understand and be able to explain how your algorithm performs.

Some examples:

1. Davis to Kendall → Red Line
2. Ashmont to Arlington → Red Line, Green Line

How you handle input, represent train routes, and present output is your choice.

## Decisions & Considerations

- Continue with the same considerations in the previous questions (unless otherwise noted)
- Utilize arguments for required CLI parameters rather than options or flags for this new travel plan type command
- Allow for any capitalization on inputs, but require they are spelled the same as existing stops
    - On failure to map to an existing stop, output the list of valid stop names to prompt corrective usage
- Allow for arguments with spaces, but need to be captured with double quotes (ideally not escaped with slashes)
- Utilize a breadth-first search style approach to be able to return a route as soon as it is found
    - The API does not make apparent the adjacency of stations on the same route
    - This hinders the ability to do true breadth-first search and guarantee the shortest path is used
    - However, by assuming that "on the same route" is close enough to "adjacency" for graph traversal, then a path is guaranteed to be found (if at least one path exists)
    - Adjacent stations are visited in alphabetical order, so the solution is deterministic, even if not necessarily the shortest path
- Slim the list of routes available from each stop (based on the set intersection of routes with the next stop) in order to give usable directions
- Add additional tests for new utility functionality, graph modeling, and newest CLI command


## Solution

At the top level of this repository, run any of the following commands in a shell after setting up the repository locally (see [README.md](../README.md)):

```bash
# Help commands for CLI
travel --help

# Short flag version of solutions
travel -lh "Ashmont" "Arlington"

# Long flag version of solutions
travel --light-rail --heavy-rail "Ashmont" "Arlington"
```