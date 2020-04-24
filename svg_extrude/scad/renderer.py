import os
import subprocess
from contextlib import contextmanager
from io import IOBase
from tempfile import mkstemp
from typing import Iterator, Optional


class Renderer:
    def __init__(self):
        pass

    def _define_args(self, defines: Optional[dict]):
        result = []
        if defines:
            for key, value in defines.items():
                result.append("-D")
                result.append(f"{key}={value}")
        return result

    @contextmanager
    def render_file(self, output_file_name: str, *, defines: Optional[dict]=None, verbose=False) -> Iterator[IOBase]:
        # Create a temporary file
        handle, path = mkstemp(suffix=".scad")

        try:
            with os.fdopen(handle, "w") as scad_file:
                yield scad_file

            if verbose:
                with open(path, "r") as f:
                    print(f.read())

            # Call OpenSCAD
            # noinspection SpellCheckingInspection
            define_args = self._define_args(defines)
            command = ["openscad", "-o", output_file_name, *define_args, path]
            subprocess.run(command, capture_output=True, check=True)
        finally:
            os.remove(path)
