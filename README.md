# demonet

Simple botnet with C2 capabilities, for educational and demonstration purposes only.

Yes, aware most parameters are hardcoded. This project is early in its development so this will likely change.

NOTE: certificate and private key must be placed in "demonet-server/certs/" directory.
certificates were generated with:

```
openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:secp384r1 -days 3650 \
  -nodes -keyout zacsucks.local.key -out zacsucks.local.crt -subj "/CN=zacksucks.local" \
  -addext "subjectAltName=DNS:zacsucks.local,DNS:*.zacsucks.local,IP:127.0.0.1"
```
