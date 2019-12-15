#!/usr/bin/env python3

import os
from hashlib import sha1
from base64 import urlsafe_b64encode


def _file_iter(f, block_size):
    d = f.read(block_size)
    while d:
        yield d
        d = f.read(block_size)


_BLOCK_SIZE = 1024 * 1024


def _sha1(path) -> bytes:
    h = sha1()
    with open(path, 'rb') as f:
        for b in _file_iter(f, _BLOCK_SIZE):
            h.update(b)

    return h.digest()


def _etag(path) -> str:
    # Make hash 21 chars, which contains 21*8=168bits = 6 * 28
    # to avoid '=' character, which is not URL safe.
    return urlsafe_b64encode(b'\x16' + _sha1(path)).decode('ascii')


def calc(path) -> str:
    """
    :return: key hashed from file content.
    """
    _, ext = os.path.splitext(path)
    return _etag(path) + ext
