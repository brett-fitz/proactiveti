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


## Modules

Lead module schema is defined at `modules/schema.yml` and there is a handy template located at `modules/template.yml`.

### Design Practices

All field sets are meant to be a 1-1 with ECS field sets so no translation is required.

* service
* threat

#### Threat Software Meta

Threat software meta is based on MITRE ATT&CK software and must be filled in when available.

!!! warning "Name"
    `name:` must be the exact name (including capitalization) used by the threat actor vs what some security company/marketing team decide to call it.
    This is purely for accuracy when reporting. 

