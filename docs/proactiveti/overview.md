# proactiveti

`proactiveti` is a Python package and cli for proactive threat intelligence.

## Providers

Providers are sources of intelligence. Here are the current list of supported providers:

* censys
* shodan

*Future provider support*

* urlscan.io
* FOFA
* BinaryEdge
* ZoomEye

### Code Layout

Each provider must have these two files:

* `/search.py`: Implements a generalized search function for the respective provider
* `/transform.py`: Implements a ETL transform function to parse results into elastic common schema (ECS).


## Intelligence Fromats

All raw intelligence and observables are transformed into Elastic Common Schema (ECS). ECS aids security professionals by creating a common set of field names that can be used
across security appliances. ECS is widely adopted and OpenTelemetry is now merging with them.
