#!/usr/bin/env python
""" generated source for module SignupUtil """
# package: com.tagged.util
import logging
import hashlib

from toiney.errors import ToineyError

logger = logging.getLogger(__name__)


class SignupUtil(object):
    """ generated source for class SignupUtil """
    def __init__(self):
        """ generated source for method __init__ """

    @classmethod
    def calculateRegHash(cls, token):
        """ generated source for method calculateRegHash """
        try:
            # md = MessageDigest.getInstance(Constants.SHA256)
            md = hashlib.sha256()
            md.update(token + b"Copyright Tagged 2012. All rights reserved.")
            hasher = md.hexdigest()
            return hasher  # return regTokenHash
        except Exception as e:
            raise logger.error(ToineyError(e))


if __name__ == '__main__':
    tokenHash = print(SignupUtil().calculateRegHash(
        b"c94d9fa7d0440d8bb8a572c59a9d49d72189d0ba2f14b3f45999203dc715b086"))
