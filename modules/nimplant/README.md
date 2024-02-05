# NimPlant

## HTTP Listener

**Censys Detection (service)**

```text
services.software.vendor="NimPlant"
```

### Service Banner

Anomalies to note:

* Status reason is in all CAPS.
* Dead give away with server header
* Date header is at the bottom (should be after http version + status)

```text
HTTP/1.1 404 NOT FOUND
Content-Type: application/json
Content-Length: 23
Server: NimPlant C2 Server
Date: Sun, 04 Feb 2024 19:07:55 GMT
```

### Server Header (default)

```text
Server: NimPlant C2 Server
```

**Censys**

```text
services.http.response.headers: (key: `Server` and value.headers: `NimPlant C2 Server`)
```

### `/` Index Response (default)

NimPlant has a fairly unique default index response:

```text
{"status":"Not found"}\n
```

**Censys**

```text
services.http.response.body_hashes="sha256:636d68bd1bc19d763de95d0a6406f4f77953f9973389857353ac445e2b6fff87"
```
