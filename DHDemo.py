#  Minimal 768bit Diffie-Hellman KX example in python / microPython
#  SJM / MCL Oct 2024
#
# Share a 96B secret key from 96B public exchanges.  Works well on ESP32-based hardware.
# Inspired by https://github.com/TOPDapp/py-diffie-hellman
#
# The code presented here is an illustration of a 96 byte key exchange process, it is written to run on microPython on microcontroller hardware as well as regular Python3.
# Illustration only, use at your own risk and not in any kind of production environment. 

import os

#import base64 utilities
try: # regular Python
    from base64 import b64encode
    from base64 import b64decode
except: # microPython
    from ubinascii import b2a_base64 as b64encode
    from ubinascii import a2b_base64 as b64decode

# --- Diffie-Hellman math -------------------------------

# Minimal Diffie-Hellman KX class based on: https://github.com/TOPDapp/py-diffie-hellman
# Produces a 96B common shared secret key (as a byte string) from 96B public exchanges
# Be careful: the process requires a good quality true-random source.
class DH:
    # A large 'safe' prime, 768bits, 96bytes, 232decimal-digits, ideally this would be somewhat bigger ~2048bits.
    bigPrime = 0xde5dbace4cef238153419d79cb586c77150a717d113045c902413d28a52d3e251bdf0df3d120992edb7d48234ebc37bc597c1ba464aa1979021e93cf1828433bd1d1c8aaf8060c0d39daba46e0c27463c840041a5f19da2117b4aee3ea26215b
    G = 2 # G must be 'primitive' to bigPrime, see https://www.garykessler.net/library/crypto.html#dhmath
          # So we choose a 'safe' prime (look-up "Sophie-Germain primes"), for which (p-1)/2 is also prime.
          # Discovering such primes is not feasible on a microcontroller and can take minutes on a modern PC.
          # But this trick makes establishing primitivity a simple matter: pow(2,(p-1)//2, p) != 1.
    def __init__(self) -> None:
        self._priKy = int.from_bytes(os.urandom(75), "big") # private key is 75 rnd bytes, to provide 540 bits
        # Check the quality of your hardware/software random source.
    def pubKey(self) -> bytes:
        return pow(self.G, self._priKy, self.bigPrime).to_bytes(96, "big") # Key for the public exchange
    def comKey(self, pubKy2:bytes) -> bytes:
        return pow(int.from_bytes(pubKy2, "big"), self._priKy, self.bigPrime).to_bytes(96, "big")

# --- some supporting functions ---------------------------

# microPython does not support int.bit_length
def bitLen(n):
    return len(bin(n))-2

def bytLen(n):
    return (len(hex(n))-1)//2

# As the name suggests, but dont use with -ve numbers
def bigInt2Bytes(bigI):
    return bigI.to_bytes(bytLen(bigI), 'big')

# Base64 encode a (long) +ve integer
def bigInt2B64(bigInt):
    return b64encode(bigInt2Bytes(bigInt)).decode('utf-8')

# Decode a base64 string to a (long) integer (+ve only)
def B642bigInt(strIn):
    return int.from_bytes(b64decode(strIn), 'big')

# Split a long string into chunks for printing
def chunkify(txt, width):
    chunks = []
    for i in range(0, len(txt), width):
        chunks.append(txt[i:i+width])
    return '\n'.join(chunks)

# --- main ---------------------------------------------------

# Setup two independent DH blocks
AlicesDH = DH()
BobsDH = DH()

# Intermediate key generation...
AlicesIntermediateKey = AlicesDH.pubKey()
BobsIntermediateKey = BobsDH.pubKey()

# Pulic channel intermediate key echange
print(f"Alice's intermediate key:\n{chunkify(b64encode(AlicesIntermediateKey).decode('utf-8'), 40)}\n")
print(f"Bob's intermediate key:\n{chunkify(b64encode(BobsIntermediateKey).decode('utf-8'), 40)}\n")

# Shared key creation
AlicesCopyOfSharedKey = AlicesDH.comKey(BobsIntermediateKey)
BobsCopyOfSharedKey = BobsDH.comKey(AlicesIntermediateKey)

# Check the two results match
assert AlicesCopyOfSharedKey == BobsCopyOfSharedKey
print(f"Shared secret:\n{chunkify(b64encode(AlicesCopyOfSharedKey).decode('utf-8'),40)}")
