# Empire

## HTTP

### Listener

#### Service >= v2.4.x

**Censys**

```text
services.banner_hashes="sha256:587d06a936c1dcb9094a58913fb610c623ee805184ea413e8bae16d9d7edaebe"
```

**Shodan**

```text
"HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 682
Cache-Control: no-cache, no-store, must-revalidate
Pragma: no-cache
Expires: 0
Server: Microsoft-IIS/7.5"
```

#### v3.4.x <= Service < 4.5.3

**Censys**

```text
services.banner_hashes="sha256:35542376d600faba10cad8e01683afb3aba7c6b81b3490fd5fea3d34c5355927"
```


**Shodan**

```text
"HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 689
Cache-Control: no-cache, no-store, must-revalidate
Pragma: no-cache
Expires: 0
Server: Microsoft-IIS/7.5"
```

#### 4.5.3 <= Service < 4.7.1

**Censys**

```text
services.banner_hashes="sha256:ba5f1b6df7cff7a8d4daa9c9a807e8db277d4a10e1a645b95b3f5598f19caa97"
```

**Shodan**

```text
"HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 836
Cache-Control: no-cache, no-store, must-revalidate
Pragma: no-cache
Expires: 0
Server: Microsoft-IIS/7.5"
```

#### 4.7.1 <= Service < 5.2.x

**Censys**

```text
services.banner="HTTP/1.1 200 OK\r\nServer: Werkzeug/* Python/*\r\nDate:  <REDACTED>\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: 836\r\nCache-Control: no-cache, no-store, must-revalidate\r\nPragma: no-cache\r\nExpires: 0\r\nServer: Microsoft-IIS/7.5\r\nConnection: close\r\n"
```


**Shodan**

```text
"Server: Werkzeug"
"Content-Type: text/html; charset=utf-8
Content-Length: 836
Cache-Control: no-cache, no-store, must-revalidate
Pragma: no-cache
Expires: 0"
```

#### Service >= 5.2.x

**Censys**

```text
services.banner_hashes="sha256:3f6cb566615ad38a76acea7957ff7f2b5475198d1493fad3eabffb42d6145c67"
```


**Shodan**

```text

```
