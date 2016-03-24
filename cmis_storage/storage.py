# coding: utf-8

import logging
import os.path

import cmislib
from cmislib.exceptions import ObjectNotFoundException
from cmislib.model import CmisClient
from django.conf import settings
from django.core.files import File
from django.core.files.storage import Storage
from django.core.urlresolvers import reverse
from django.utils.deconstruct import deconstructible

logger = logging.getLogger(__name__)


@deconstructible
class CMISStorage(Storage):
    """
    Storage engine to upload and fetch files from a CMIS-enabled content management system, like Alfresco
    """

    def __init__(self, base_folder=None):
        self.options = settings.CMIS_STORAGE_OPTIONS

        if 'baseFolder' not in self.options:
            self.options['baseFolder'] = '/'

        if base_folder:
            self.options['baseFolder'] = base_folder

        self.client = CmisClient(**self.options)
        self.repo = self.client.getDefaultRepository()

    def _open(self, name, mode='rb'):
        return File(self.open_stream(name), name=name)

    def open_stream(self, name):

        # Build the full path of the file
        full_path = os.path.join(self.options['baseFolder'], name.strip('./'))

        # Get the object from the CMS
        obj = self.repo.getObjectByPath(full_path)  # type: cmislib.model.Document

        # Return the stream
        return obj.getContentStream()

    def _save(self, name, content):
        logger.debug("Saving file {}".format(name))

        # Build the full path of the file
        full_path = os.path.join(self.options['baseFolder'], name.strip('.'))

        logger.debug("Full path at {}".format(full_path))

        # Split the path
        dirname, filename = os.path.split(full_path)

        # Get the folder
        folder = self.repo.getObjectByPath(dirname)

        # Create the document
        newfile = folder.createDocument(filename, contentFile=content)

        # Get the new path for the file
        newfile_path = newfile.getPaths()[0]

        logger.debug("New path: {}".format(newfile_path))

        return newfile_path

    def delete(self, name):
        logger.debug("Deleting file '{}'".format(name))

        # Build the full path of the file
        full_path = os.path.join(self.options['baseFolder'], name.strip('./'))

        try:
            obj = self.repo.getObjectByPath(full_path)
            obj.delete()
        except cmislib.exceptions.ObjectNotFoundException:
            pass

    def exists(self, name):
        logger.debug("Checking if file exists '{}'".format(name))

        # Build the full path of the file
        full_path = os.path.join(self.options['baseFolder'], name.strip('./'))

        try:
            self.repo.getObjectByPath(full_path)
        except cmislib.exceptions.ObjectNotFoundException:
            return False

        return True

    def path(self, name):
        return name

    def _props(self, name):
        # Build the full path of the file
        full_path = os.path.join(self.options['baseFolder'], name.strip('./'))

        # Get the object from the CMS
        obj = self.repo.getObjectByPath(full_path)  # type: cmislib.model.Document

        return obj.getProperties()

    def modified_time(self, name):
        """
        Returns the last modification date for the specified file
        """
        return self._props(name).get('cmis:lastModificationDate', None)

    def accessed_time(self, name):
        return None

    def created_time(self, name):
        return self._props(name).get('cmis:creationDate', None)

    def size(self, name):
        return self._props(name).get('cmis:contentStreamLength', 0)

    def listdir(self, path):
        try:
            folder = self.repo.getObjectByPath(path)

            if not isinstance(folder, cmislib.models.Folder):
                return []

            return [x.getName() for x in folder.getChildren()]

        except ObjectNotFoundException as e:
            return []

    def url(self, name):
        return reverse('cmis_storage_get_file', kwargs={'path': name})
