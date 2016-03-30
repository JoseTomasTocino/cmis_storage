=============================
cmis_storage
=============================

.. image:: https://badge.fury.io/py/cmis_storage.png
    :target: https://badge.fury.io/py/cmis_storage

**cmis_storage** is a storage engine for Django to integrate CMIS-compatible services, like Alfresco.
It's currently compatible with Django 1.7+ and Python 2.7, and uses Apache cmislib. Python 3.x is not
currently supported because cmislib does not support it yet.

Documentation
-------------

The full documentation can be found at https://cmis_storage.readthedocs.org.

Installation
------------

First, install **cmis_storage** from pip using

::

    pip install cmis_storage

Next, add ``cmis_storage`` to ``INSTALLED_APPS`` in your ``settings.py`` file:

::

    INSTALLED_APPS = (
        ...
        'cmis_storage',
    )

You also need to add the configuration for your CMIS-compatible server in your ``settings.py`` file,
like this, for example:

::

    CMIS_STORAGE_OPTIONS = {
        'repositoryUrl': 'http://localhost:8080/alfresco/api/-default-/public/cmis/versions/1.0/atom',
        'username': 'admin',
        'password': 'admin',
        'baseFolder': '/'
    }

The config parameters are self-explanatory.


Usage
------------

**cmis_storage** offers the class ``CMISStorage``, which is a storage engine
that you can use in any ``FileField`` field within your models, for example:

::

    from django.db import models

    from cmis_storage.storage import CMISStorage


    class TestModel(models.Model):
        document = models.FileField(storage=CMISStorage())

From that point on, all the file handling involving ``TestModel.document`` will happen on the CMIS-compatible
server. You shouldn't need to directly interact with the `CMISStorage`, only in case you
need to manually delete a file. You can do it like this:

::

    storage = CMISStorage()
    storage.delete(instance.document.path)

Optional views
^^^^^^^^^^^^^^

The module offers an optional view so you can directly serve files of your content management system
from a certain URL. To use it, simply add a corresponding url to the view in your ``urls.py`` file:

::

    urlpatterns = [
        ...
        url(r'^get/(?P<path>.+)$', cmis_storage.views.get_file,  name='cmis_storage_get_file'),
    ]

Beware though, the view **should not be used as-is**, because it does not make any kind of authentication
or authorization check.

Credits
---------

This module was built by José Tomás Tocino and other authors that may be referenced in the AUTHORS file, and was financed by the University of Cádiz (Spain) for the development of several internal projects.
