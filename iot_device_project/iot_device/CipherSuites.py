from enum import Enum
import ssl

class CipherSuites(Enum):
    V1_3_SECURE = ("TLS_AES_256_GCM_SHA384", ssl.PROTOCOL_TLS)
    V1_3_PERFORMANCE = ("TLS_AES_128_GCM_SHA256", ssl.PROTOCOL_TLS)
    V1_3_MOBILE_DEVICES = ("TLS_CHACHA20_POLY1305_SHA256", ssl.PROTOCOL_TLS)
    V1_2_SECURE = ("ECDHE-ECDSA-AES256-GCM-SHA384", ssl.PROTOCOL_TLSv1_2)
    V1_2_PERFORMANCE = ("ECDHE-ECDSA-AES128-GCM-SHA256", ssl.PROTOCOL_TLSv1_2)
    V1_2_MOBILE_DEVICES = ("ECDHE-ECDSA-CHACHA20-POLY1305", ssl.PROTOCOL_TLSv1_2)

    def __init__(self, value, description):
        self._value_ = value  # Set the first value as the enum's value
        self.tls_version = description  # Store the second value as an attribute

    @classmethod
    def get_description(cls, value):
        # Iterate through the enum to find the matching value
        for suite in cls:
            if suite.value == value:
                return suite.tls_version
        return None  # Return None if the value isn't found

def is_cipher_suite(value):
    return value in {suite.value for suite in CipherSuites}

# On small resources constrained devices like microcontrollers, their CPU sometimes
# comes with HW accelerator blocks for AES algorithm.
#
# AES-CCM can be implemented using the same AES HW accelerator block to allow much faster and
# efficient encryption/decryption without using software only algorithms.
#
# AES-GCM is somewhat "new-ish" and required a different way to calculate the GHASH.
# So, on devices without HW accelerator for it, it has to be implemented in software
# which is somewhat slower and less efficient.

# https://blog.cloudflare.com/do-the-chacha-better-mobile-performance-with-cryptography/
# There are two types of ciphers typically used to encrypt data with TLS: block ciphers and stream ciphers.
# In a block cipher, the data is broken up into chunks of a fixed size and each block is encrypted.
# In a stream cipher, the data is encrypted one byte at a time. Both types of ciphers have their advantages,
# block ciphers are generally fast in hardware and somewhat slow in software, while stream ciphers often have
# fast software implementations.
#
# TLS has a secure block cipher, AES, that has been implemented in hardware and is generally very fast.
# One current problem with TLS is that there is no secure choice of stream cipher. The de facto stream cipher for TLS is RC4,
# which has been shown to have biases and is no longer considered secure.
#
# AES is a fine cipher to use on most modern computers. Intel processors since Westmere in 2010 come with AES hardware support
# that makes AES operations effectively free. This makes it an ideal cipher choice for both our servers and for web visitors
# using modern desktop and laptop computers. It’s not ideal for older computers and mobile devices.
# Phones and tablets don’t typically have cryptographic hardware for AES and are therefore required to use
# software implementations of ciphers. The AES-GCM cipher can be particularly costly when implemented in software.
# This is less than optimal on devices where every processor cycle can cost you precious battery life.
# A low-cost stream cipher would be ideal for these mobile devices, but the only option (RC4) is no longer secure.
#
# In order to provide a battery-friendly alternative to AES for mobile devices,
# several engineers from Google set out to find and implement a fast and secure stream cipher to add to TLS.
# Their choice — ChaCha20-Poly1305 — was included in Chrome 31 in November 2013,
# and Chrome for Android and iOS at the end of April 2014.
#
# Having the option to choose a secure stream cipher in TLS is a good thing for mobile performance.
# Adding cipher diversity is also good insurance.
# If someone finds a flaw in one of the AES-based cipher suites sometime in the future,
# it gives a safe and fast option to fall back to.
