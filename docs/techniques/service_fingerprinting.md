# Service Fingerprinting

## General Techniques

### RTFM

Read the fucking manual. When the service you are attempting to fingerprint is open-source, or the code is available (Cobalt Strike)... read the fucking code.
Chances are there is zero/bad authentication or easy methods to fingerprint the service :wink:.

### HTTP

#### Service Banner

A banner grab for HTTP is essentially a GET request for the `/` resource. 

**Example Banner Grab using cURL**

```
> GET / HTTP/1.1
> Host: google.com
> User-Agent: curl/8.1.2
> Accept: */*
>
< HTTP/1.1 301 Moved Permanently
< Location: http://www.google.com/
< Content-Type: text/html; charset=UTF-8
< Content-Security-Policy-Report-Only: object-src 'none';base-uri 'self';script-src 'nonce-yAIYqFeNI2mANIKJL-FZKw' 'strict-dynamic' 'report-sample' 'unsafe-eval' 'unsafe-inline' https: http:;report-uri https://csp.withgoogle.com/csp/gws/other-hp
< Date: Mon, 23 Oct 2023 15:15:43 GMT
< Expires: Wed, 22 Nov 2023 15:15:43 GMT
< Cache-Control: public, max-age=2592000
< Server: gws
< Content-Length: 219
< X-XSS-Protection: 0
< X-Frame-Options: SAMEORIGIN
<
```

!!! note
    Some network scan providers will follow redirects. Make note of this behavior if it does occur and
    what the true location of resource that was served. 

##### Headers & Cookies

**Technique 1: Unique Headers or Cookies**

Some services add unique custom headers or cookies keys/values that you can explicity look for. This is the easiest and most simplistic detection.

*Example: Havoc adds the header key "X-Havoc"*

```
HTTP/1.1 404 Not Found
Content-Type: text/html
Server: nginx
X-Havoc: true
Date: Mon, 23 Oct 2023 14:51:07 GMT
Content-Length: 146
```

**Example: Responder adds a hardcoded "Date" value**

**Technique 2: Header Keys + Order**

* Hash all header keys
* Retain order --> This is very important as some C2 services put headers in unorthodox orders.

**Technique 3: Header Keys + Values + Order**

* Hash all header keys + values
* Retain order
* Redact problematic values
  * Date value --> Unless specifically called out, redact this value as it is the time of the response. There are a few frameworks like Responder that hardcode this value and that by itself is an indicator.  


!!! note
    Some values could be unique to each instance of a service. Inspect similar services and attempt to identify any of these 
    headers or cookies and remove them from your query.

**Technique 4: Date header location**

The location of the "Date" header is accutely important for service fingerprinting as the order of the headers can indicate one service from another when all else is similar. 

*Example: Search date order*

```
# Given the following banner...

HTTP/1.1 404 Not Found
Content-Type: text/html
Server: nginx
X-Havoc: true
Date: Mon, 23 Oct 2023 14:30:16 GMT
Content-Length: 146

# Shodan Search
"X-Havoc: true Date:" "GMT Content-Length: 146"
```

By capturing the header key + value before and after, we have forced the search to only find that specific order of header keys. You may have to include additional logic/wildcards depending on your use-case. 

**Technique 5: Capitalization**

Observe the capitilzation of specific headers. Some services will miss a capital or have all header keys lowered. This is another observable that can be used in a search.

### TCP

#### Banner Grab

A simple banner grab (read buffer after tcp connection established) and provide unique return content that can be fingerprinted.

*Example: DarkComet*

```
BF7CAB464EFB
```

### TLS 

#### Protocol Implementation

#### Server Certificate

The following techniques are for analyzing **self-signed** certifcates. Analyzing certificates produced by Certificate Authorities provide little to no intelligence however, mature
organizations can still codify what algorithms, key-length, etc the actor chose to use for a specific provider (assuming they are configurable). This is called an infrastructure TTP.

??? info "RFCs for Reference"
    * https://datatracker.ietf.org/doc/html/rfc4519
    * https://www.rfc-editor.org/rfc/rfc5280.txt
    * https://www.rfc-editor.org/rfc/rfc8399


**List of Observables**

* Issuer DN: Information about the certificate authority that issued the certificate.
* Subject DN: Information about the entity that was issued the certificate.
* Extensions: Additional fields that extend the X.509 spec.
* Validity Period: The dates from which and to which the certificate can be used.
* Serial Number: The issuer-specific identifier of the certificate.
* Public Key: The public key of the key pair that is associated with the certificate.
* Signature Algorithm: The algorithm used to sign the certificate.
* Signature Value: Bit string containing the digital signature.

**Technique 1: Serial Number**

The serial number of a certificate may be hardcoded and can therefore easily be identified.

*Example: Cobalt Strike*

```
tls.server.x509.serial_number: 146473198
```

**Technique 2: Unique Distinguished Names (DNs)**

*A distinguished name for an X.509 certificate consists of a sequence of relative distinguished names (RDN) where each RDN is expressed as an attribute type/value pair.*

We can hash the entire string for an issuer, subject or both distinguished names.

*Example: Cobalt Strike Management Certificate*

```
Issuer | Server DN: "C=Earth, ST=Cyberspace, L=Somewhere, O=cobaltstrike, OU=AdvancedPenTesting, CN=Major Cobalt Strike" 
hash: f363a7789bb316f7d665b160973580ffaa0baddee84f6826d6eee3601b8d2322
```


**Technique 3: Unique RDNs, OIDs, and Values**

RDNs make up the issuer and subject distinguished names (DNs).

*General Format*

```
<type>=<value>(;<type>=<value>)*[;]
```

* Unique OIDs, values, and RDNs (oid + value pair) can all be used to formulate a cert fingerprint
* Identify any anomalies in the string like odd delimeters, spacing, etc (recommended: run ZLint on certificate)

*Example: DcRat*

```
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            db:43:7d:0f:42:81:6e:fd:77:fc:13:29:22:3e:8d:2f:7d:10:cc:75
        Signature Algorithm: sha512WithRSAEncryption
        Issuer: CN=Server, OU=qwqdanchun, O=DcRat By qwqdanchun, L=SH, C=CN
        Validity
            Not Before: Nov 23 10:29:35 2020 GMT
            Not After : Sep  2 10:29:35 2031 GMT
        Subject: CN=DcRat
```

**Technique 4: DN Format Algorithm**

The format for the DN can be algorithmically computed to produce a fingerprint.

*Component 1: Issuer DN*

* Extract the following components
  * OID keys with delimeter between OID and value
  * Order of the OID keys
  * Delimters between RDNs 

*Component 2: Subject DN*

*Component 3: Extensions (Optional)*

* Hash the extensions in order

!!! warning "LICENSE"
    The above algorithm is not authorized for commerical use. Please contact me if you would like to license the above.

**Technique 5: ZLint Hash**

* Hash the ZLint errors, warnings and notices to produce different hashes to use in various combinations.

*Core: Hash Failed Lints - Example using DcRat*

```
Failed Lints
    e_ca_country_name_missing
    e_ca_key_usage_missing
    e_ca_organization_name_missing
    e_ext_authority_key_identifier_missing
    e_ext_authority_key_identifier_no_key_identifier
    e_mp_modulus_must_be_2048_bits_or_more
    e_rsa_mod_less_than_2048_bits
    e_serial_number_longer_than_20_octets
    e_sub_ca_certificate_policies_missing
    e_sub_ca_crl_distribution_points_missing
    n_mp_allowed_eku
    n_sub_ca_eku_missing
    w_sub_ca_aia_does_not_contain_issuing_ca_url
    w_sub_ca_aia_missing
```

!!! warning "LICENSE"
    The above algorithm is not authorized for commerical use. Please contact me if you would like to license the above.
