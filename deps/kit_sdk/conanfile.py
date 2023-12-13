import os

from conan import ConanFile
from conan.tools.files import copy, download


class KitSDKConan(ConanFile):
    name = "kit_sdk"
    version = "105.1.0"
    settings = "os", "compiler", "build_type", "arch"
    description = "Kit SDK binary dependency"
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
            download_link = "https://d4i3qtqj3r0z5.cloudfront.net/kit-sdk%40105%2E1%2E0%2Brelease%2E51%2Ea7407fb5%2Etc%2Elinux-x86_64%2Erelease%2E7z"
            expected_sha256 = "57d69c91f185491cc1f8181062c908f5389d5e2b780efd20aa9ed6187e12328d"
        elif self.settings.arch == "x86_64" and self.settings.os == "Windows":
            download_link = "https://d4i3qtqj3r0z5.cloudfront.net/kit-sdk%40105%2E1%2E0%2Brelease%2E51%2Ea7407fb5%2Etc%2Ewindows-x86_64%2Erelease%2E7z"
            expected_sha256 = "aa561b1037c434fe1dc450238f99c077327ca47482e34e0cf0cb96b5a4d5e037"
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
        pass
