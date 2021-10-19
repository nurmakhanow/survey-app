from django.db import models


class CreatedUpdatedModelMixin(models.Model):
    """
    Abstract base class with creation and modification datetime
    """
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')


class MultiSerializerViewSetMixin(object):
    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.
        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            try:
                return self.serializer_action_classes[self.request.method]
            except KeyError:
                if self.request.method == 'PATCH':
                    try:
                        return self.serializer_action_classes['GET']
                    except KeyError:
                        try:
                            return self.serializer_action_classes['list']
                        except KeyError:
                            raise AttributeError
            except AttributeError:
                return super(
                    MultiSerializerViewSetMixin, self
                ).get_serializer_class()
