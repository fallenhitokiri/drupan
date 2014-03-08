# -*- coding: utf-8 -*-
import unittest
import tempfile
import shutil
import sys
import os
import io

sys.path.insert(0, os.path.abspath('..'))
from drupan.inout.filesystem import Reader


class InOutFilesystemTestCase(unittest.TestCase):
    def setUp(self):
        """create a temporary directory and some files"""
        self.dir = tempfile.mkdtemp()
        self.config = {"dir": self.dir, "extension": None}

        self.content1 = u"abc"
        self.content2 = u"123"

        name1 = os.path.join(self.dir, "one")
        name2 = os.path.join(self.dir, "two")

        with io.open(name1, 'w', encoding='utf-8') as output:
            output.write(self.content1)

        with io.open(name2, 'w', encoding='utf-8') as output:
            output.write(self.content2)

    def tearDown(self):
        """remove the temporary directory created for this test"""
        shutil.rmtree(self.dir)

    def test_get(self):
        """should read two files"""
        reader = Reader(self.config)
        results = reader.get()

        possible = (self.content1, self.content2)

        self.assertEqual(len(results), 2)

        for result in results:
            exists = result in possible
            self.assertTrue(exists)

    def test_optional_config(self):
        """should set the extension and encoding"""
        reader = Reader(self.config)

        # test defaults
        self.assertEqual(reader.extension, None)
        self.assertEqual(reader.encoding, "utf-8")

        self.config["extension"] = "foo"
        self.config["encoding"] = "bar"
        reader = Reader(self.config)

        self.assertEqual(reader.extension, "foo")
        self.assertEqual(reader.encoding, "bar")

    def test_wrong_extension(self):
        """should correctly validate the extension"""
        reader = Reader(self.config)

        self.assertEqual(reader.wrong_extension("asdf"), False)

        self.config["extension"] = "foo"
        reader = Reader(self.config)

        self.assertEqual(reader.wrong_extension("asdf"), True)
        self.assertEqual(reader.wrong_extension("asdf.foo"), False)
