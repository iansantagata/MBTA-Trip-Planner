# Question 1

## Prompt

Write a problem that retrieves data representing what weʼll call “subway” routes:
“Light Rail” and “Heavy Rail” (types 0 and 1 in the API, respectively).
The program should print their names to the console.

A partial example of output:

```
Red Line, Blue Line, Orange Line, ...
```

There are two ways to filter results for subway-only routes:

1. Download all data from the API ( `https://api-v3.mbta.com/routes` ) and filter locally on your computer
2. Filter data with the API ( `https://api-v3.mbta.com/routes?filter[type]=0,1` ) and download just the filtered data to your computer

Please document your decision and your reasons for it.

## Decisions & Considerations

- Utilize filters on the HTTP request to reduce the size of HTTP responses with minimally required data set
- Allow the solution to extend to all supported types of routes as requested by the user to be more generalizable
    - Includes light rail, heavy rail, commuter rail, bus, and ferry route types
- Prefer re-requesting to use latest data set rather than downloading and storing a local copy that can become stale
- Deduplicate and sort data shown to user in the presentation layer
- Separate interacting with the API from interacting with the CLI to keep responsibilities separate
- Added basic tests with mocking of the API request so that tests do not trigger API requests

## Solution

At the top level of this repository, run any of the following commands in a shell after setting up the repository locally (see [README.md](README.md)):

```bash
# Help command for CLI
routes --help

# Short flag version of solution
routes -hl

# Long flag version of solution
routes --heavy-rail --light-rail
```