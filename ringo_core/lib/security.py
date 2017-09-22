#!/usr/bin/env python
# -*- coding: utf-8 -*-
from passlib.context import CryptContext

pwd_context = CryptContext(
    # replace this list with the hash(es) you wish to support.
    # this example sets pbkdf2_sha256 as the default,
    # with support for legacy md5 hashes.
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",

    # vary rounds parameter randomly when creating new hashes...
    all__vary_rounds=0.1,

    # set the number of rounds that should be used...
    # (appropriate values may vary for different schemes,
    # and the amount of time you wish it to take)
    pbkdf2_sha256__default_rounds=8000,
)


def encrypt_password(password, scheme=None):
    """Will return a string with encrypted password using the passlib
    library. The returned string will have the following format:
    $algo$rounds$salt$hash

    :password: unencrypted password
    :scheme: string of an supported encryption algorithm. Defaults tthe
    CryptContext default
    :returns: encrypted password
    """
    return pwd_context.encrypt(password, scheme=scheme)


def verify_password(password, pwhash):
    """Will return True if the password is valid. Else False.

    :password: unencrypted password
    :pwhash: encrypted password
    :returns: True or False
    """
    return pwd_context.verify(password, pwhash)
