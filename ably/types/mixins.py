import six
import json
import base64

import logging

from ably.util.crypto import CipherData

log = logging.getLogger(__name__)


class EncodeDataMixin(object):

    def __init__(self, encoding):
        self.encoding = encoding

    @staticmethod
    def decode(data, encoding='', cipher=None):
        encoding = encoding.strip('/')
        encoding_list = encoding.split('/')

        while encoding_list:
            encoding = encoding_list.pop()
            if encoding == 'json':
                if isinstance(data, six.binary_type):
                    data = data.decode()
                if isinstance(data, list) or isinstance(data, dict):
                    continue
                data = json.loads(data)
            elif encoding == 'base64' and isinstance(data, six.binary_type):
                data = base64.b64decode(data)
            elif encoding == 'base64':
                data = base64.b64decode(data.encode('utf-8'))
            elif encoding.startswith('%s+' % CipherData.ENCODING_ID):
                if not cipher:
                    log.error('Message cannot be decrypted as the channel is '
                              'not set up for encryption & decryption')
                    encoding_list.append(encoding)
                    break
                data = cipher.decrypt(data)
            elif encoding == 'utf-8' and isinstance(data, six.binary_type):
                data = data.decode('utf-8')
            elif encoding == 'utf-8':
                pass
            else:
                log.error('Message cannot be decoded. '
                          "Unsupported encoding type: '%s'" % encoding)
                encoding_list.append(encoding)
                break

        encoding = '/'.join(encoding_list)
        return {'encoding': encoding, 'data': data}

    @property
    def encoding(self):
        return '/'.join(self._encoding_array).strip('/')

    @encoding.setter
    def encoding(self, encoding):
        if not encoding:
            self._encoding_array = []
        else:
            self._encoding_array = encoding.strip('/').split('/')
