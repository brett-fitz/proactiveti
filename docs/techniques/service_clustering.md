# Service Clustering

Service clustering is a technique to group similar configurations of the same service. This can help 

When performing service clustering, you should create buckets of observables like TLS implementation, application protocol, extracted C2 config, etc. 

## Clustering Techniques

### SSH Public Key Fingerprint

SSH Public Key fingerprint is the most trivial form of service clustering. When you find other servers with an ssh service with the same public key fingerprint - they are owned by the same actor, company/group or "tribe of groups".

**:warning: NOTE**

Sophisticated actors will likely NEVER reuse the same ssh key across hosts. I have rarely seen a well-funded state sponsored actor perform this unless they deployed infra using sloppy infrastructure as code or they missed their OpSec 101 course LOL. It doesn't mean that it still doesn't happen, it does... just typically its more reserved for less sophisticated actors/those that care less about operational security. 

