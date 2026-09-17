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
- Prefer re-requesting data to be aware of latest data set rather than downloading and storing a local copy and operating off of stale data
- Deduplicate and sort output shown to user in the presentation layer
- Avoid sorting intermediate data as extra work

## Solution

At the top level of this repository, run one of the following commands in a shell after setting up the repository locally (see [README.md]):

```bash
# Short flag version
mbta -hl

# Long flag version
mbta --include-heavy-rail --include-light-rail
```