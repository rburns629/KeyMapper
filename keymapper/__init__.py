import json

class KeyMapper(dict):
    """
    Example:
        km = KeyMapper({'messages': {'message1': 'Hello World!'}}})
        print(km['messages.message1'])
    Variables:
        __delimiter is set to dot-notation by default, unless specified otherwise.
    """
    __delimiter = "."  # Default

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self.__dict__.update({k: v})
        if kwargs:
            self.__delimiter = kwargs['delimiter']

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
            if self.__delimiter in key:
                return self.mapper(self.__dict__, key.split(self.__delimiter), self.__getitem__.__name__)
            else:
                return self.get(key)
        except Exception as e:
            raise e

    def __setitem__(self, key, value):
        try:
            if self.__delimiter in key:
                self.mapper(self.__dict__, key.split(self.__delimiter), self.__setitem__.__name__, value)
            else:
                super().__setitem__(key, value)
                self.__dict__.update({key: value})
        except Exception as e:
            raise e

    def __delitem__(self, key):
        try:
            if self.__delimiter in key:
                self.mapper(self.__dict__, key.split(self.__delimiter), self.__delitem__.__name__)
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
        try:
            for i, s in enumerate(m):
                if s in d.keys():
                    if s != m[-1] or i != len(m) - 1:
                        if isinstance(d[s], dict): 
                            return cls.mapper(d[s], m[1:], callback, *args, **kwargs)
                        elif isinstance(d[s], (list, tuple, set)):
                            return cls.mapper(d[s][int(m[1].strip('][])()}{'))], m[2:], callback, *args, **kwargs)
                    elif s == m[-1] and i == len(m) - 1:
                        if callback == '__setitem__':
                            d[s] = args[0]; return None
                        elif callback == '__delitem__': 
                            del d[s]; return None
                        else: 
                            return d[s]
                else:
                    if i == len(m) - 1:
                        if callback == '__setitem__': 
                            d[m[-1]] = args[0]; return None
                    else: 
                        raise KeyError('{}'.format(m[i]))
        except Exception as e:
            raise e