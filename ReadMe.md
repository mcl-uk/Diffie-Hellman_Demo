Minimal 768bit Diffie-Hellman KX example in python / microPython
----------------------------------------------------------------

SJM / MCL Oct 2024

Share a 96B secret key from 96B public exchanges.  Works well on ESP32-based hardware.

The Diffie-Hellman key establishment mechanism is a beautifully simple piece of mathematics.
It allows Alice and Bob to share a secret over an open channel, safe in the knowledge that Eve cannot use the public data to clone the secret.
The shared secret can then be used as the key for a subsequent symetrically encrypted (eg AES) communications session.
Note that DHKX allows only for the establishment of a random shared key and not for the transmission of any particular plain-text message as such.

Before they start Alice and Bob must settle on a big prime and a small integer that they can both use in their maths.
These are not secret numbers and can be established by any public means. However, the big prime and the small integer (G) need to be fairly carefully chosen (see the script).

Once this numerical basis has been established, Alice and Bob work independently to calculate a random intermediate key for public exchange.
Note that the quality of thier random number sources is crucial to the security of the overall process.
They then swap these keys and from them calculate a final result in such a way that each side ends up with same answer - the shared secret key.
Provided the numbers are large enough it is not feasible for Eve to calculate the result knowing only the public data.
The maths for all this (as with RSA) hinges on modular exponentiation in which calculating a function one way is relatively easy but the inverse is exponentially difficult.
At least until, or if, quantum computers mature to the point of 'cryptographic relevence'.

The code presented here is an illustration of a 96 byte key exchange process, it is written to run on microPython on microcontroller hardware as well as regular Python3.
Illustration only, use at your own risk and not in any kind of production environment. 
