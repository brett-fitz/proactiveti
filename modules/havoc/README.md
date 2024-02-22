# Havoc

## Listener

### HTTP

#### HTTP Header

Looks for the header and key value pair: `X-Havoc: true`

**Censys**

```text
services.banner="*X-Havoc: true*"
```

**Shodan**

```text
"X-Havoc: true"
```

### HTTPS

#### TLS Certificate (default)

**Censys**

```text
same_service(
    services.tls.certificates.leaf_data.subject_dn="C=*, ST=*, L=*, street=*, O=*, CN=*"
    and
    services.tls.certificates.leaf_data.subject_dn="C=*, ST=*, L=*, street=*, O=*, CN=*")
```
