#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `new_proj_three` package."""

from unittest import TestCase
from tempfile import TemporaryDirectory
import os
from new_proj_three.hash_str import hash_str

# If the option to install automatics writes is false then import the atomic write from pset 1
# Otherwise import atomic_writes from csci_utils
if "yes" == "no":
    from new_proj_three.io import atomic_write
else:
    from csci_utils.io.io import atomic_write

class Tests(TestCase):
    def test_fake_test(self):
        pass

class FakeFileFailure(IOError):
    pass

class HashTests(TestCase):
    def test_basic(self):
        self.assertEqual(hash_str("world!", salt="hello, ").hex()[:6], "68e656")

class AtomicWriteTests(TestCase):
    def test_atomic_write(self):
        """Ensure file exists after being written successfully"""

        # Create a new temporary directory
        with TemporaryDirectory() as tmp:
            # Join the tmp file directory to the made up file name and store as a file path
            fp = os.path.join(tmp, "asdf.txt")

            # use the atomic_write method as a context manager.
            with atomic_write(fp, "w") as f:
                assert not os.path.exists(fp)
                tmpfile = f.name
                f.write("asdf")

            # After the atomic_write method finishes, make sure the tmpfile is removed.
            assert not os.path.exists(tmpfile)

            # Make sure that the non-temp file exists after the atomic_write context manager finishes
            assert os.path.exists(fp)

            # Check that the new atomically written file was written correctly.
            with open(fp) as f:
                self.assertEqual(f.read(), "asdf")

    def test_atomic_failure(self):
        """Ensure that file does not exist after failure during write"""

        # Create a new temporary file in a temporary directory
        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            # Create a fake failure. Temp file exists but before writing a FakeFailFailure() is raised.
            with self.assertRaises(FakeFileFailure):
                with atomic_write(fp, "w") as f:
                    tmpfile = f.name
                    assert os.path.exists(tmpfile)
                    raise FakeFileFailure()

            # After the FakeFailFailure(), ensure that the temporary file path and permanent file path do not exist.
            assert not os.path.exists(tmpfile)
            assert not os.path.exists(fp)

    def test_file_exists(self):
        """Ensure an error is raised when a file exists"""

        # Create a new temporary file in a temporary directory
        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            # Create a fake file with the same name in the same temp directory.
            with open(fp, "w") as existing_file:
                existing_file.write("I Exist")

            # Use assertRaises as a context manager testing if atomic_writer raises an exception when the file exists.
            with self.assertRaises(FileExistsError):
                # Try atomically writing to another file with the same name.
                with atomic_write(fp) as file:
                    file.write("This file should not be written")

    def test_str_returned(self):
        """
        1. Test that a string is returned if the as_file argument is False.
        2. Test that the object returned is not a string when as_file is True.
        """

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with atomic_write(fp, as_file=False) as file:
                self.assertEqual(type(file), str)

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with atomic_write(fp, as_file=True) as file:
                self.assertNotEqual(type(file), str)

    def test_other_kwargs(self):
        """ Test that the atomic_write method can accept other keyword arguments.

        """

        # Create a new temporary file in a temporary directory
        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            # Write a character using UTF-8 encoding
            with atomic_write(fp, encoding='UTF-8') as file:
                first_ln = chr(57344)
                file.write(first_ln)

            # Read back what was written to the file and ensure it is in UTF-8.
            with open(fp, 'r') as opened_file:
                line_file = opened_file.read()
                self.assertEqual(line_file, '\ue000')