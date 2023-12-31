import os

from conan import ConanFile
from conan.tools.files import copy, download


class PythonConan(ConanFile):
    name = "python"
    version = "3.10.13+nv3"
    settings = "os", "compiler", "build_type", "arch"
    description = "Python binary dependency"
    license = "MIT"

    def build_requirements(self): # windows only unfortunately
        if self.settings.os == "Windows":
            self.tool_requires("7zip/19.00")

    # https://github.com/conan-io/conan/issues/3287#issuecomment-993960784
    # workaround for unsupported proprietary 7z
    def system_requirements(self):
        if self.settings.os == "Linux":
            import importlib.util
            import subprocess
            import sys

            # Check if py7zr is installed
            if importlib.util.find_spec("py7zr") is None:
                # Install py7zr if not installed
                subprocess.check_call([sys.executable, "-m", "pip", "install", "py7zr"])
            else:
                # Skip installation if already installed
                pass

    def build(self):

        # Note: we don't pull debug deps for this package
        if self.settings.arch == "x86_64" and self.settings.os == "Linux":
            download_link = "https://d4i3qtqj3r0z5.cloudfront.net/python%403.10.13%2Bnv3-linux-x86_64.7z"
            expected_sha256 = "78d6ce9ae76a89c3ecfa8df05b98160715632ad40b68c96c7c3ebee1cc85da32"
        elif self.settings.arch == "x86_64" and self.settings.os == "Windows":
            download_link = "https://d4i3qtqj3r0z5.cloudfront.net/python%403.10.13%2Bnv3-windows-x86_64.7z"
            expected_sha256 = "6ee9529d2f6d9d80ab88f9d129e2f18aa165f15f0aef6721869a20b56a2d23e1"
        else:
            raise ConanInvalidConfiguration(f"Unsupported triple {self.settings.arch}-{self.settings.os}")

        download(self, download_link, filename=self.name, sha256=expected_sha256)

        if self.settings.os == "Windows":
            self.run(f"7z x {self.name}")
        elif self.settings.os == "Linux":
            import py7zr
            with py7zr.SevenZipFile(self.name, mode='r') as z:
                z.extractall(path=".")

        os.unlink(self.name)

    def package(self):
        copy(self, "*", self.build_folder, self.package_folder)

    def package_info(self):
        self.cpp_info.bindirs = ['bin']
        if self.settings.os == "Windows": # Fix packman mispackaging
            self.cpp_info.includedirs = ['include']
            self.cpp_info.libdirs = ['libs']
            self.cpp_info.libs = ['python3', 'python310']
        else:
            self.cpp_info.includedirs = ['include/python3.10']
            self.cpp_info.libdirs = ['lib']
            self.cpp_info.libs = ['python3', 'python3.10']
