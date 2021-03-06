#!/usr/bin/env python
import os, sys

import subprocess
from setuptools import setup, Extension
from setuptools.dist import Distribution
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install

with open("%%README%%", 'r') as fp:
    readme_text = fp.read()

def check_cmake():
    try:
        out = subprocess.check_output(['cmake', '--version'])
        return True
    except OSError:
        return False

class cmake_extension(Extension):
    def __init__(self, name):
        Extension.__init__(self, name, sources=[])


class cmake_build(build_ext):
    def run(self):
        if not check_cmake():
            raise RuntimeError('CMake is not available. CMake 3.12 is required.')

        import nest

        nest_install_dir = os.path.sep.join(nest.__path__[0].split(os.path.sep)[:-4])
        mod = os.getenv("NEST_MODULE_PATH", "")
        mod_dir = os.path.join(nest_install_dir, "lib", "nest")
        if mod_dir not in mod:
            raise Exception(
                f"Please make sure the 'NEST_MODULE_PATH' env var contains '{mod_dir}' for the installation to succeed.\n"
                + f"Current value: '{mod}'"
            )


        # Installation dir of nest, required for the cmake command
        nest_config = os.path.join(nest_install_dir, "bin", "nest-config")
        # Name of the extension, will be used to determine folder name
        ext_name = self.extensions[0].name
        # The path where CMake will be configured and Arbor will be built.
        build_directory = os.path.abspath(self.build_temp)
        # The path where the package will be copied after building.
        lib_directory = os.path.abspath(self.build_lib)
        # The path where the built libraries end up
        source_path = build_directory
        # Where to copy the package after it is built, so that whatever the next phase is
        # can copy it into the target 'prefix' path.
        dest_path = os.path.join(lib_directory, ext_name)

        cmake_args = [
            '-DCMAKE_BUILD_TYPE=Release', # we compile with debug symbols in release mode.
            "-Dwith-nest=" + nest_config
        ]
        build_args = ['--config', 'Release']

        env = os.environ.copy()
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        cmake_list_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), ext_name)
        print('-'*20, 'Configure CMake')
        subprocess.check_call(['cmake', cmake_list_dir] + cmake_args,
                              cwd=self.build_temp, env=env)

        print('-'*20, 'Build')
        cmake_cmd = ['cmake', '--build', '.'] + build_args
        subprocess.check_call(cmake_cmd,
                              cwd=self.build_temp)

        cmake_cmd = ['make', 'install']
        subprocess.check_call(cmake_cmd,
                              cwd=self.build_temp)

        # Copy from build path to some other place from whence it will later be installed.
        # ... or something like that
        # ... setuptools is an enigma monkey patched on a mystery
        if not os.path.exists(dest_path):
            os.makedirs(dest_path, exist_ok=True)
        self.copy_tree(source_path, dest_path)

setup(
    name="%%NAME%%",
    version="%%VERSION%%",
    description="%%DESCRIPTION%%",
    license="%%LICENSE%%",
    author="%%AUTHOR%%",
    author_email="%%EMAIL%%",
    url="%%REPO%%",
    long_description=readme_text,
    long_description_content_type="text/markdown",
    zip_safe=False,
    packages=%%MODULES%%,
    package_data=%%PKG_DATA%%,
    ext_modules=%%CMAKE_EXTENSIONS%%,
    cmdclass={
        'build_ext': cmake_build,
    },
    include_package_data = True,
)
