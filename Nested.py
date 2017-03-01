import logging


logger = logging.getLogger('nested')

def log_msg(**kwargs):
    msg = "\n\t\t"
    for k, v in kwargs.iteritems():
        if isinstance(v, dict) or isinstance(v, list):
            v = "\n" + pp.pformat(v)
        msg += '%s: %s, ' % (k, v)
    return msg

class Nested(object):
    """
    """

    def __init__(self):
        self.by_hash_dir_file = {}
        self.dir_list = list()
        self.all_hashes = set(' ') # must be created with at least one element

    def nested_lookup(self, key, document):
        """Lookup a key in a nested document, return a list of values"""
        items = list(self._nested_lookup(key, document))
        return items

    def _nested_lookup(self, key, document):
        """Lookup a key in a nested document, yield a value"""
        if isinstance(document, list):
            if len(document) > 0:
                for d in document:
                    for result in self._nested_lookup(key, d):
                        yield result

        if isinstance(document, dict):
            for k, v in iteritems(document):
                if k == key:
                    yield v
                elif isinstance(v, dict):
                    for result in self._nested_lookup(key, v):
                        yield result
                elif isinstance(v, list):
                    if len(v) > 0:
                        for d in v:
                            for result in self._nested_lookup(key, d):
                                yield result

class NestClean(object):
    """
    """

    def __init__(self):
        pass

    def remove_item(self, key, document):
        """Lookup a key in a nested document, return a list of values"""
        items = list(self._nested_lookup(key, document))
        return items

    def _nested_lookup(self, key, document):
        """Lookup a key in a nested document, yield a value"""
        if isinstance(document, list):
            if len(document) > 0:
                for d in document:
                    for result in self._nested_lookup(key, d):
                        yield result

        if isinstance(document, dict):
            for k, v in iteritems(document):
                if k == key:
                    yield v
                elif isinstance(v, dict):
                    for result in self._nested_lookup(key, v):
                        yield result
                elif isinstance(v, list):
                    if len(v) > 0:
                        for d in v:
                            for result in self._nested_lookup(key, d):
                                yield result