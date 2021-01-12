import shelve


class ShelveDB:
    def __init__(self, path=None):
        if not path:
            raise NotImplementedError

        self.__shelve = shelve.open(path)

        all_ids = self.__get_all_ids()
        if not all_ids:
            self.__max_id = 0
        else:
            self.__max_id = max(int(i) for i in all_ids)

    def __get_all_ids(self):
        return list(self.__shelve.keys())

    def get_next_id(self):
        self.__max_id += 1
        return self.__max_id

    def get(self, key):
        key = str(key)

        if key not in self.__shelve:
            raise KeyError

        return self.__shelve[key]

    def get_all(self):
        all_ids = self.__get_all_ids()
        return [self.get(key) for key in all_ids]

    def create(self, item, key_name):
        item = item.dict()
        key = str(item[key_name])

        if key in self.__shelve:
            raise KeyError

        self.__shelve[key] = item

    def update(self, key, value):
        key = str(key)
        if key not in self.__shelve:
            raise KeyError

        self.__shelve[key] = value

    def delete(self, key):
        key = str(key)
        if key not in self.__shelve:
            raise KeyError

        del self.__shelve[key]
