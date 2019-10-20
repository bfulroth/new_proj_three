from contextlib import contextmanager
import os
import shutil


@contextmanager
def atomic_write(file, mode="w", as_file=True, **kwargs):
    """Write a file atomically

    :param file: str or :class:`os.PathLike` fp to write

    :param bool as_file:  if True, the yielded object is a :class:File.
        (eg, what you get with `open(...)`).  Otherwise, it will be the
        temporary file path string

    :param kwargs: anything else needed to open the file

    :raises: FileExistsError if fp exists

    Example::

        with atomic_write("hello.txt") as f:
            f.write("world!")

    """

    # Error checking
    # Check that the file path is a string with an extension
    try:

        # Convert an os.Pathlike object to a path str if needed.
        file = os.fspath(file)

        index = file.find(".")

        # No ext dot found, raise a TypeError.
        if index == -1:
            raise TypeError("The provided file path doesn't not have a required file extension.")

        temp_file_path = file[:index] + "~" + file[index:]

    except TypeError:
        raise TypeError("Got an unexpect type for parameter file. Expected string or os.Pathlike object.")

    # Check that the file doesn't already exist.
    if os.path.exists(file):
        raise FileExistsError(
            "This file already exists. This file was not overwritten. Exiting."
        )

    try:
        # Use a context manager to open a temp file
        if as_file:
            with open(temp_file_path, mode=mode, **kwargs) as f:
                yield f
        else:
            yield temp_file_path

        # Make a copy of the temp file and name it the original file path.
        if as_file:
            shutil.copy(temp_file_path, file)

    # Remove the temporary file.
    finally:
        if as_file:
            try:
                os.remove(temp_file_path)
            except:
                raise IOError("Could not remove temporary file.")
