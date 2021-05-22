

class SizeStorage(object):

    def __init__(self, session):

        self._session = session
        self._session_key = 'CLOTHES_SIZE'

        self._items = self._get_items_from_session()

    def _get_items_from_session(self):

        data = self._session.get(self._session_key)

        if not data:
            return {}

        try:
            return {int(k): v for k, v in data.items()}
        except Exception as e:
            print(e)
            return {}

    def commit(self):
        self._session[self._session_key] = self._get_commit_data()
        self._session.modified = True

    def _get_commit_data(self):
        return self._items

    def set(self, product_id, data):

        self._items[product_id] = data
        self.commit()

    def get(self, product_id):
        return self._items.get(product_id) or {}

    def clear(self):
        self._items = {}
        self.commit()
