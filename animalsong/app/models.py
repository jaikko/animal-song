from django.db import models
from django.db.models.base import ModelBase

# Create your models here.

class InheritanceMetaclass(ModelBase):
    def __call__(cls, *args, **kwargs):
        obj = super(InheritanceMetaclass, cls).__call__(*args, **kwargs)
        return obj.get_object()

class Animal(models.Model):
    __metaclass__ = InheritanceMetaclass
    type = models.CharField(max_length=255)
    object_class = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.object_class:
            self.object_class = self._meta.module_name
        super(Animal, self).save( *args, **kwargs)
    def get_object(self):
        if not self.object_class or self._meta.module_name == self.object_class:
            return self
        else:
            return getattr(self, self.object_class)

class Dog(Animal):
    def make_sound(self):
        print "Woof!"


class Cat(Animal):
    def make_sound(self):
        print "Meow!"