from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import numpy
import os
import platform

ROOT = os.path.dirname(os.path.abspath(__file__))

include_dirs = [
    os.path.join(ROOT, "creversi_cpp"),
    os.path.join(ROOT, "simde"),   # simde submodule
    numpy.get_include(),
]

class my_build_ext(build_ext):
    def build_extensions(self):
        machine = platform.machine().lower()
        compiler = self.compiler.compiler_type

        for e in self.extensions:
            if compiler == 'unix':
                # Intel Mac or Linux x86_64
                if machine == 'x86_64':
                    e.extra_compile_args = ['-std=c++11', '-msse4.2', '-mbmi', '-mbmi2', '-mavx2']
                elif machine == 'aarch64' or machine == 'arm64':
                    # ARM64 (Apple Silicon or Linux ARM)
                    e.extra_compile_args = ['-std=c++11']

            elif compiler == 'msvc':
                # Windows x86
                if machine == 'amd64':
                    e.extra_compile_args = ['/arch:AVX2']
                else:
                    e.extra_compile_args = []

        build_ext.build_extensions(self)

ext_modules = [
    Extension('creversi.creversi',
        ['creversi/creversi.pyx',
         'creversi_cpp/bit_manipulations.cpp', 'creversi_cpp/hand.cpp', 'creversi_cpp/movable_generator.cpp', 'creversi_cpp/move_generator.cpp', 'creversi_cpp/state.cpp', 'creversi_cpp/utils.cpp', 'creversi_cpp/value.cpp'],
        language='c++',
        include_dirs = include_dirs),
    Extension('creversi.gym_reversi.envs.reversi_env',
        ['creversi/gym_reversi/envs/reversi_env.pyx'],
        language='c++'),
    Extension('creversi.gym_reversi.envs.reversi_vec_env',
        ['creversi/gym_reversi/envs/reversi_vec_env.pyx'],
        language='c++'),
]

setup(
    name='creversi',
    version='0.0.1',
    packages=['creversi', 'creversi.gym_reversi', 'creversi.gym_reversi.envs'],
    ext_modules=ext_modules,
    cmdclass={'build_ext': my_build_ext}
)
