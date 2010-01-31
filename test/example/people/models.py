# -*- coding: utf-8 -*-

from django.db import models
from djqmixin import Manager, QMixin


class AgeMixin(QMixin):
    def minors(self):
        return self.filter(age__lt=18)
    
    def adults(self):
        return self.filter(age__gte=18)



class Group(models.Model):
    pass


class Person(models.Model):
    
    group = models.ForeignKey(Group, related_name='people')
    age = models.PositiveIntegerField()
    
    objects = Manager.include(AgeMixin)()
