# Censys Techniques / Info

## HTTP

### Headers

#### Date Header

One of the key advantages to censys's implementation of a "service banner" is that they redact the Date value which is typically generated at request time and not hardcoded.

The downside to this is that there are some services like a responder listener that will have a hardcoded date value. Any hardcoded value can easily help distinguish the service. 

## TLS


