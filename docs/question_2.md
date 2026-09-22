# Question 2

## Prompt

Extend your pgoram so it displays additional information:

1. The name of the subway route with the most stops and the count of its stops
2. The name of the subway route with the fewest stops and the count of its stops
3. A list of the stops that connect two or more subway routes and the route names for each of those stops

## Decisions & Considerations

- Continue with the same considerations in the previous questions (unless otherwise noted)
- Leverage what has already been built and continue supporting all previous use cases still applicable
- Separate into a different command to make it transparent for users what each command does and what applies for their use case
- Keep duplication to a minimum by not repeating code (i.e. DRY) and reusing code when possible
- Add additional tests with more targeted mocking of functions not under test or API requests
- Chose to display all routes with their stop counts at once rather than only selecting highest or lowest stop routes for a more generalizable and usable result
- Opt to interpret route ID not found by API request as 0 stops for user transparency purposes
    - This would only occur if a route ID is provided but unrecognized, leading to an HTTP 200 Success with no stop data
    - Functionally, this is only possible in testing scenarios, or when a route ID is manually provided (which is not currently supported)
- Separate commands for enumerating routes with stop counts from enumerating connecting stops since they have different use cases

## Solution

At the top level of this repository, run any of the following commands in a shell after setting up the repository locally (see [README.md]):

```bash
# Help commands for CLI
stops --help
connections --help

# Short flag version of solutions
stops -lh
connections -lh

# Long flag version of solutions
stops --light-rail --heavy-rail
connections --light-rail --heavy-rail
```