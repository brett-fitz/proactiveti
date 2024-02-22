# Covenant

## Management Service (HTTP/S)

### Favicon

**Censys**

```text
services.http.response.favicons.md5_hash="dd80f14145f075264b3067801f511c2f"
```

**Shodan**

```text
http.favicon.hash:-737603591
```

### TLS Certificate

**Censys**

```text
services.tls.certificates.leaf_data.issuer_dn="CN=Covenant" 
  and services.http.response.headers.Server="Kestrel"
```

**Shodan**

```text
ssl.cert.issuer.cn:"Covenant"
  "Content-Type: text/html; charset=utf-8"
  "Server: Kestrel"
```
