# Pupy

GitHub: https://github.com/n1nj4sec/pupy

## HTTP Listener

**Censys**

```text
services.http.response.body_hashes="sha256:c546c26d5c24925659d627b9621ab007e7d94c17629307ee15a1f1d84eec5efe" and services.http.response.headers.Server="nginx/1.13.8"
```

Combining the signatures reported below produces an interesting leads query.

### Service Banner

Anomalies to report:

* Hardcoded nginx server header with version: https://github.com/n1nj4sec/pupy/blob/a5d766ea81fdfe3bc2c38c9bdaf10e9b75af3b39/pupy/pupylib/PupyWeb.py#L32

### `/` index Response (default)

Hardcoded in the code: https://github.com/n1nj4sec/pupy/blob/a5d766ea81fdfe3bc2c38c9bdaf10e9b75af3b39/pupy/webstatic/nginx_index.html

## HTTPS Listener

### TLS Certificate

* Hardcoded Organizational Unit (OU) RDN value `CONTROL` https://github.com/n1nj4sec/pupy/blob/a5d766ea81fdfe3bc2c38c9bdaf10e9b75af3b39/pupy/pupylib/PupyCredentials.py#L232
* Harcoded certificate serial number: `2`

**Censys**

```text
services.tls.certificates.leaf_data.subject.organizational_unit="CONTROL"
```

**Shodan**

```text
ssl.cert.serial:2 ssl:"OU=CONTROL"
```
