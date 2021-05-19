
class DeliveryRouter(object):

    app_label = 'delivery'
    db_name = 'delivery'

    def db_for_read(self, model, **hints):

        if self._is_delivery_method_model(model):
            return None

        if model._meta.app_label == self.app_label:
            return self.db_name

        return None

    def db_for_write(self, model, **hints):

        if self._is_delivery_method_model(model):
            return None

        if model._meta.app_label == self.app_label:
            return self.db_name

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if model_name == 'deliverymethod':
            return None

        if app_label == self.app_label:
            return False

        return None

    def _is_delivery_method_model(self, model):
        return model.__name__.lower() == 'deliverymethod'
