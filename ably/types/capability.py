from collections import MutableMapping
import json

import six

class Capability(MutableMapping):
    def __init__(self, obj={}):
        self.__dict = dict(obj)
        for k, v in six.iteritems(obj):
            self[k] = v

    def __getitem__(self, key):
        return self.__dict[key]

    def __iter__(self):
        return iter(self.__dict)

    def __len__(self):
        return len(self.__dict)

    def __contains__(self, key):
        return key in self.__dict

    def __setitem__(self, key, value):
        # validate that the value is a list of ops and that the key is a string
        if not isinstance(key, six.string_types):
            raise ValueError('Capability keys must be strings')

        if isinstance(value, six.string_types):
            value = [value]

        operations = set()
        for val in iter(value):
            if not isinstance(val, six.string_types):
                raise ValueError('Operations must be strings')
            operations.add(val)
            
        self.__dict[key] = operations

    def __delitem__(self, key):
        del self.__dict[key]

    def setdefault(self, key, default):
        if not key in self:
            self[key] = default
        return self[key]

    def add_resource(self, resource, operations=[]):
        if isinstance(operations, six.string_types):
            operations = [operations]
        self[resource] = list(operations)

    def add_operation_to_resource(self, operation, resource):
        self.setdefault(resource, []).append(operation)

    def __unicode__(self):
        return Capability.c14n(self)

    def __str__(self):
        return unicode(self).encode('utf-8')

    @staticmethod
    def c14n(capability):
        sorted_ops = {k:sorted(v) for k, v in six.iteritems(capability)}
        return json.dumps(sorted_ops, sort_keys=True)