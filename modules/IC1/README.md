# IC1: Infrastructure Cluster 1

IC1 represents a cluster of infrastructure believed to be operated by APT28 (FANCY BEAR). Research was started after public reporting by CERT-UA.

REF: https://cert.gov.ua/article/4905829

*Note: This is a cluster of infrastructure that has not been attributed to a specific service but is perceived to be a possible threat. False positives are likely!*


## IC1-1: Suspected C2 HTTP Listener 

### HTTP Banner

```text
HTTP/1.1 404 Not Found
Access-Control-Allow-Origin: *
Cache-Control: no-cache, no-store, must-revalidate
Content-Type: text/plain; charset=utf-8
Expires: 0
Pragma: no-cache
X-Content-Type-Options: nosniff
Date: <REDACTED> GMT
Content-Length: 19
```

**Censys**

```text
services.banner_hashes="sha256:dfe5574717fa51535df774105f82349026aa9d1a846e4a6741cb664f0f5adb3a"
```

### HTTP `/` Index Response

```text
404 page not found\n
```

**Note: This is a very popular default response as there are 1.5million other services that share this response.**

