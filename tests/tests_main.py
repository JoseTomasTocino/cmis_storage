#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cmis_storage
------------

Tests for `cmis_storage`
"""
import os

from django.core.files.base import File
from django.test import TestCase

from cmis_storage.storage import CMISStorage
from tests.models import TestModel


class TestCmisStorage(TestCase):
    def setUp(self):
        pass

    def test_it_all(self):
        storage = CMISStorage()

        # Get absolute path to test document in current folder
        document_path = os.path.join(os.path.dirname(__file__), 'sample_document.txt')
        document_file = open(document_path)

        # Test file upload
        instance = TestModel()
        instance.document = File(document_file)
        instance.save()

        self.assertEqual(instance.pk, 1)
        self.assertIn('sample_document', instance.document.path)
        self.assertTrue(instance.document.path.startswith(u'//'))

        # Test file existence
        self.assertTrue(storage.exists(instance.document.path))

        # Test file download
        other_instance = TestModel.objects.get()
        document = other_instance.document.read()
        self.assertEqual(document, 'This is a sample document\n')

        # Test file download from view
        response = self.client.get(other_instance.document.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'This is a sample document\n')

        # Test file deletion
        storage.delete(instance.document.path)
        self.assertFalse(storage.exists(instance.document.path))

    def tearDown(self):
        pass
