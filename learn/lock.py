from threading import RLock


class _IdPool(object):
    def __init__(self, _start, _step=1):
        self._start = _start
        self._step = _step
        self._current = _start

    def get_free_id(self):
        self._current += self._step
        return self._current


class Hcd(object):
    def __init__(self):
        self._context_dict = {}
        self._context_dict_lock = RLock()
        self._context_id_poll = _IdPool(0x10000000)

    def teardown(self):
        with self._context_dict_lock:
            contexts = self._context_dict.values()
            for each in contexts:
                self.release_context(each)

    def get_context(self, context_id):
        if type(context_id) in (str, unicode):
            context_id = int(context_id)
        with self._context_dict_lock:
            return self._context_dict[context_id]

    def new_context(self):
        context_id = self._context_id_poll.get_free_id()
        with self._context_dict_lock:
            self._context_dict[context_id] = context_id
        return context_id

    def release_context(self, context):
        with self._context_dict_lock:
            self._context_dict.pop(context.context_id)

if __name__ == '__main__':
    hcd = Hcd()
    hcd.new_context()
    hcd.new_context()
    hcd.new_context()
    hcd.teardown()
