# -*- coding: utf-8 -*-

__version__ = '0.1'

from django.db import models


class QMixin(dict):
    
    """Abstract superclass for defining mixins."""
    
    class __metaclass__(type):
        def __new__(mcls, name, bases, attrs):
            # Circumvent an error in the creation of `QMixin` itself.
            if bases == (dict,):
                return type.__new__(mcls, name, bases, attrs)
            
            # A `QMixin` subclass is transformed into a `QMixin` instance.
            return QMixin(attrs)
    
    def __repr__(self):
        return 'QMixin(%r)' % (dict(self),)


class Manager(models.Manager):
    
    # If this is the default manager for a model, use this manager class for
    # relations (i.e. `group.people`, see README for details).
    use_for_related_fields = True
    
    class QuerySet(models.query.QuerySet):
        pass
    
    @classmethod
    def _with_qset_cls(cls, qset_cls):
        return type(cls.__name__, (cls,), {'QuerySet': qset_cls})
    
    @classmethod
    def include(cls, *mixins):
        
        """
        Create a new `Manager` class with the provided mixins.
        
        Call this method with one or more `QMixin` instances to return a new
        manager class. Don't forget to instantiate this afterwards, like so:
        
            objects = Manager.include(A, B, C)()
        
        `QMixin` instances can be easily created by subclassing `QMixin`; some
        metaclass hackery is used to achieve this:
        
            class AgeMixin(QMixin):
                def minors(self):
                    return self.filter(age__lt=18)
            
            assert isinstance(AgeMixin, QMixin)
        
        If more than one mixin is supplied, they are combined into one. The
        behavior for conflicts is to resolve from left-to-right. For example:
        
            class A(QMixin):
                def method(self):
                    return 'a'
            
            class B(QMixin):
                def method(self):
                    return 'b'
            
            class Person(models.Model):
                objects = Manager.include(A, B)()
            
            assert Person.objects.method() == 'a'
        
        """
        
        mixin = merge_mixins(mixins)
        # Create a new QuerySet class, inheriting from the current one, with the
        # 
        qset_cls = type('QuerySet', (cls.QuerySet,), mixin)
        return cls._with_qset_cls(qset_cls)
    
    def get_query_set(self, *args, **kwargs):
        return self.QuerySet(model=self.model)
    
    def __getattr__(self, attr):
        try:
            return getattr(self.get_query_set(), attr)
        except AttributeError:
            raise



def merge_mixins(mixins):
    
    """
    Given a sequence of mixins, return a single, merged mixin.
    
    Resolution is from left-to-right, so due to the behavior of `dict.update()`,
    the sequence of mixins is reversed (using `sequence[::-1]`) and then a
    new mixin is `update()`d with each.
    """
    
    if not mixins:
        raise ValueError("No mixins given")
    elif len(mixins) == 1:
        return mixins[0]
    
    combined = QMixin()
    for mixin in mixins[::-1]:
        combined.update(mixin)
    return combined
