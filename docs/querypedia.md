# Querypedia

*Note: Intentionally limited at the moment while I determine the best way to automate docs...but here is an example*

# Cobalt Strike

## TLS

### Server Certificates

**Censys**

```
services.tls.certificates.leaf_data.subject_dn="C=Earth, ST=Cyberspace, L=Somewhere, O=cobaltstrike, OU=AdvancedPenTesting, CN=Major Cobalt Strike" 
or services.tls.certificates.leaf_data.issuer_dn="C=Earth, ST=Cyberspace, L=Somewhere, O=cobaltstrike, OU=AdvancedPenTesting, CN=Major Cobalt Strike"
```

**Shodan**

```
ssl.cert.serial:146473198
```

## HTTP

**Censys**

```
services.service_name="COBALT_STRIKE"
```

**Shodan**

```
product:"Cobalt Strike Beacon"
```

### Default

**Censys**

```
services.banner_hashes="sha256:8d83eccca809d058a7c7d18f630f7341ea8b88f699cb4c6c30623787caf431a9"
```

**Shodan**

```
"HTTP/1.1 404 Not Found Date:"
"GMT Content-Type: text/plain Content-Length: 0"
-"Connection:"
-"Server:" 
-product:"Cobalt Strike Beacon"
-ssl.cert.serial:1110208595,146473198
```

Proxy

```
"HTTP/1.1 404 Not Found Date:"
"GMT Content-Type: text/plain Content-Length: 0"
"Connection:"
"Server:"
-http.headers_hash:"-645009794"
-product:"Cobalt Strike Beacon"
-ssl.cert.serial:1110208595,146473198
```

### Malleable Profile (default)

**Censys**

```
"HTTP/1.1 404 Not Found Date:" 
"GMT Server: Apache Content-Length: 0 Keep-Alive: timeout=10, max=100 Connection: Keep-Alive Content-Type: text/plain"
```

**Shodan**

```
product:"Cobalt Strike Beacon"
```
