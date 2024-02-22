# Acunetix

*Acunetix vulnerability scanner.*

## Management Service (HTTP/S)

### Default Setup

**Censys**

```text
services.http.response.html_tags="<title>Acunetix</title>"
```

### Cracked Versions

#### Docker Container

**Censys**

```text
services.tls.certificates.leaf_data.subject_dn="CN=awvs.lan"
or
services.http.response.body_hashes="sha256:c54253d5b97cc096e944e7ea9185c4fe2fd5ac9303db044735d3ebd76b08d21f"
```

#### Known IDs

**Censys**

```text
services.tls.certificates.leaf_data.issuer.common_name="Acunetix WVS Root Authority (v1slc)"
or
services.tls.certificates.leaf_data.issuer.common_name="Acunetix WVS Root Authority (aFhKE)"
```

### TLS Certificate

**Censys**

```text
services.tls.certificates.leaf_data.subject.organizational_unit="Acunetix Web Vulnerability Scanner"
```
