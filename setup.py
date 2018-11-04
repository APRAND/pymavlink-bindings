import os
import re
import sys
import platform
import subprocess

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: "
                + ", ".join(e.name for e in self.extensions)
            )

        if platform.system() == "Windows":
            # Remove windows support for now
            raise RuntimeError("Windows is not currently supported")
            cmake_version = LooseVersion(
                re.search(r"version\s*([\d.]+)", out.decode()).group(1)
            )
            if cmake_version < "3.1.0":
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        # TODO:
        print("Cloning git submodules...")
        args = "git submodule update --init --recursive"
        ret = self.run_cmd(args.split(" "))
        (returncode, output) = ret
        if returncode != 0:
            # TODO: log this
            print(ret, args)
            raise RuntimeError(
                "git submodules failed to update: {r} {o}".format(
                    r=returncode, o=output
                )
            )
        print(output)

        # Generate C++11 headders
        print("\nGenerating mavlink headders...")
        args = "{python} ./mavlink/pymavlink/tools/mavgen.py --lang C++11 ./mavlink/message_definitions/v1.0/ardupilotmega.xml -o ./generated/mavlink --wire-protocol=2.0".format(
            python=sys.executable
        )
        ret = self.run_cmd(args.split(" "))
        (returncode, output) = ret
        if returncode != 0:
            # TODO: log this
            print(ret, args)
            raise RuntimeError(
                "mavlink headder generation failed: {r} {o}".format(
                    r=returncode, o=output
                )
            )
        print(output)

        # Write out the python bindings for the current message definitions
        print("\nGenerating and compiling binding code...")
        import generate_bindings
        generate_bindings.generate()

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + extdir,
            "-DPYTHON_EXECUTABLE=" + sys.executable,
        ]

        cfg = "Debug" if self.debug else "Release"
        build_args = ["--config", cfg]

        if platform.system() == "Windows":
            cmake_args += [
                "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir)
            ]
            if sys.maxsize > 2 ** 32:
                cmake_args += ["-A", "x64"]
            build_args += ["--", "/m"]
        else:
            cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]
            build_args += ["--", "-j2"]

        env = os.environ.copy()
        env["CXXFLAGS"] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get("CXXFLAGS", ""), self.distribution.get_version()
        )
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(
            ["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env
        )
        subprocess.check_call(
            ["cmake", "--build", "."] + build_args, cwd=self.build_temp
        )

    def run_cmd(self, args, shell=False):
        try:
            p = subprocess.check_output(
                args, stderr=subprocess.STDOUT, shell=shell
            ).decode("utf-8")
            return (0, p.strip())
        except subprocess.CalledProcessError as e:  # non zero return
            # print(e.returncode) # the non zero return code
            # print(e.cmd) # the cmd that caused it
            # print(e.output) # the error output (if any)
            return (e.returncode, e.output.strip())


setup(
    name="MAVLink_binder",
    version="0.0.1",
    author="Samuel Dudley",
    author_email="dudley.samuel@gmail.com",
    description="Python bindings for mavlink C++ code",
    long_description="",
    ext_modules=[CMakeExtension("MAVLink_binder")],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
)
