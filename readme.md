This is my own implementation of sha1. It's part of a presentation I did for a class 'cryptography'.

Here's an example for hashing 'hello world'
```python
from sha import sha1_hex
sha1_hex(b'hello world')  # outputs: 2aae6c35c94fcfb415dbe95f408b9ce91ee846ed
```

Here's an example for hashing a file:
```python
from sha import sha1_of_file
sha1_of_file('shattered/shattered-1.pdf')  # outputs: 38762cf7f55934b34d179ae6a4c80cadccbb7f0a
```
Note: the documents shattered-1.pdf and shattered-2.pdf do collide in sha-1