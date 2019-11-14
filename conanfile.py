#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools

class LibwebsocketsConan(ConanFile):
    name = "libwebsockets"
    version = "3.1.0"
    description = "Canonical libwebsockets.org websocket library"
    url = "https://github.com/memunix/conan-libwebsockets"
    homepage = "https://github.com/warmcat/libwebsockets"
    license = "LGPL-2.1"
    exports = "LICENSE.md"
    exports_sources = "CMakeLists.txt"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    options = {
        "shared": [True, False],
        "lws_with_libuv": [True, False],
        "lws_with_libevent": [True, False],
        "lws_with_zlib": [True, False],
        "lws_with_ssl": [True, False],
        "lws_wit_raw": [True, False],
        "lws_with_plugins": [True, False]
    }
    default_options = {
        'shared': False,
        'lws_with_libuv': True,
        'lws_with_libevent': True,
        'lws_with_zlib': True,
        'lws_with_ssl': True,
        'lws_wit_raw': True,
        'lws_with_plugins': False,
    }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def configure(self):
        del self.settings.compiler.libcxx

    def requirements(self):
        if self.options.lws_with_libuv:
            self.requires.add("libuv/1.31.0@bincrafters/stable")
        if self.options.lws_with_libevent:
            self.requires.add("libevent/2.1.11@bincrafters/stable")
        if self.options.lws_with_zlib:
            self.requires.add("zlib/1.2.9@conan/stable")
        if self.options.lws_with_ssl:
            self.requires.add("OpenSSL/1.1.1c@conan/stable")

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["LWS_WITHOUT_TESTAPPS"] = True
        cmake.definitions["LWS_LINK_TESTAPPS_DYNAMIC"] = True
        cmake.definitions["LWS_WITH_SHARED"] = self.options.shared
        cmake.definitions["LWS_WITH_STATIC"] = not self.options.shared
        cmake.definitions["LWS_WITH_SSL"] = self.options.lws_with_ssl
        cmake.definitions["LWS_WITH_LIBUV"] = self.options.lws_with_libuv
        cmake.definitions["LWS_WITH_LIBEVENT"] = self.options.lws_with_libevent
        cmake.definitions["LWS_WITH_ZLIB"] = self.options.lws_with_zlib
        cmake.definitions["LWS_ROLE_RAW_PROXY"] = self.options.lws_wit_raw
        cmake.definitions["LWS_WITH_PLUGINS"] = self.options.lws_with_plugins
        if not self.options.lws_with_zlib:
            cmake.definitions["LWS_WITHOUT_EXTENSIONS"] = True
            cmake.definitions["LWS_WITH_ZIP_FOPS"] = False
        # zlib is required for extensions

        cmake.definitions["CMAKE_INSTALL_PREFIX"] = self.package_folder
        cmake.configure(build_folder=self._build_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
       self.copy("*.h", dst="include", src=("%s/include" % self._source_subfolder))
       self.copy("*.so*", dst="lib/debug", keep_path=False)
       self.copy("*.so*", dst="lib/release", keep_path=False)
       self.copy("*.dylib*", dst="lib/debug", keep_path=False)
       self.copy("*.dylib*", dst="lib/release", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.debug.libdirs = ["lib/debug"]
        self.cpp_info.release.libdirs = ["lib/release"]        
        self.cpp_info.release.libdirs = ["lib"]        
