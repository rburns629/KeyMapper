import json, re


class KeyMapper(dict):
    """
    Example:
        km = KeyMapper({'messages': {'message1': 'Hello World!'}}})
        print(km['messages.message1'])
    Variables:
        __delimiter__ is set to dot-notation by default, unless specified otherwise.
    """
    __delimiter__ = "."  # Default

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self.__dict__.update({k: v})
        if kwargs:
            self.__delimiter__ = kwargs['delimiter']

    def __getattr__(self, attr):
        try:
            return self.get(attr)
        except Exception as e:
            raise e

    def __setattr__(self, key, value):
        try:
            self.__setitem__(key, value)
        except Exception as e:
            raise e

    def __delattr__(self, item):
        try:
            self.__delitem__(item)
        except Exception as e:
            raise e

    def __getitem__(self, key):
        try:
            if self.__delimiter__ in key:
                return self.mapper(self.__dict__, key.split(self.__delimiter__), self.__getitem__.__name__)
            else:
                return self.get(key)
        except Exception as e:
            raise e

    def __setitem__(self, key, value):
        try:
            if self.__delimiter__ in key:
                self.mapper(self.__dict__, key.split(self.__delimiter__), self.__setitem__.__name__, value)
            else:
                super().__setitem__(key, value)
                self.__dict__.update({key: value})
        except Exception as e:
            raise e

    def __delitem__(self, key):
        try:
            if self.__delimiter__ in key:
                self.mapper(self.__dict__, key.split(self.__delimiter__), self.__delitem__.__name__)
            else:
                super().__delitem__(key)
                del self.__dict__[key]
        except Exception as e:
            raise e

    def pprint(self, *args):
        try:
            if len(args) > 0:
                return json.dumps(args[0], indent=4, ensure_ascii=False)
            return json.dumps(self, indent=4, ensure_ascii=False)
        except Exception as e:
            raise e

    @classmethod
    def mapper(cls, d, m, callback, *args, **kwargs):
        for i, k in enumerate(m):
            key = k if not re.search(r'[0-9]+', k) else int(k)
            try:
                if str(key) in d or type(key) == int and d[key]:
                    if str(key) != m[-1] or i != len(m) - 1:
                        return cls.mapper(d[key], m[1:], callback, *args, **kwargs)
                    elif str(key) == m[-1] and i == len(m) - 1:
                        if callback == '__setitem__':
                            d[key] = args[0]
                            return None
                        elif callback == '__delitem__':
                            del d[key]
                            return None
                        else:
                            return d[key]
            except Exception as e:
                raise e
            else:
                if i == len(m) - 1:
                    if callback == '__setitem__':
                        d[m[-1]] = args[0]
                        return None
                else:
                    raise KeyError('{}'.format(m[i]))
        else:
            if callback == '__getitem__':
                return d
