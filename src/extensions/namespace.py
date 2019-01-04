from flask_restplus import Namespace as OriginalNamespace

from src.extensions.model import Model, OrderedModel


class Namespace(OriginalNamespace):
    def model(self, name=None, model=None, mask=None, **kwargs):
        '''
        Register a model

        .. seealso:: :class:`Model`
        '''
        cls = OrderedModel if self.ordered else Model
        model = cls(name, model, mask=mask)
        model.__apidoc__.update(kwargs)
        return self.add_model(name, model)