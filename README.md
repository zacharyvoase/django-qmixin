# `django-qmixin`

`django-qmixin` is a reusable Django application for extending managers and the
querysets they produce.

A mixin is a subclass of `djqmixin.QMixin` which defines some related methods
that operate on a `QuerySet` or `Manager` instance. Mixins can be ‘mixed in’ to
a manager class, and their methods will be made available on all instances of
that class (whether on the model itself or via a relation), as well as the
`QuerySet` instances it produces.

What this achieves is the ability to add queryset-level functionality to your
model with the minimum amount of work possible.


## Mixins? Heresy!

Well, not quite. `Manager.include()` doesn't monkey patch, and there's very
little magic involved. Overall, there are only 38 lines of code in this library,
and they're all quite heavily commented, so you can find out for yourself if you
like.


## Installation

The usual:

    easy_install django-qmixin # OR
    pip install django-qmixin

The only other thing you'll need is Django itself; this library has been tested on versions 1.0 and 1.1.


## Usage

Basic usage is as follows:

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
        GENDERS = dict(m='Male', f='Female', u='Unspecified').items()
        
        group = models.ForeignKey(Group, related_name='people')
        gender = models.CharField(max_length=1, choices=GENDERS)
        age = models.PositiveIntegerField()
        
        objects = Manager.include(AgeMixin)()
    
    # The `minors()` and `adults()` methods will be available on the manager:
    assert isinstance(Person.objects.minors(), models.query.QuerySet)
    
    # They'll be available on subsequent querysets:
    assert isinstance(Person.objects.filter(gender='m').minors(),
                      models.query.QuerySet)
    
    # They'll also be available on relations, if they were mixed in to the
    # default manager for that model:
    group = Group.objects.all()[0]
    assert isinstance(group.people.minors(), models.query.QuerySet)

A test project is located in `test/example/`; consult this for a more
comprehensive example.


## (Un)license

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
