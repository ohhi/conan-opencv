from conans import ConanFile, CMake
import os, fnmatch

# Function to recursively match a pattern through a directory hieracy
def rfnmatch(dirname, pattern):
    matches = []
    for root, dirnames, filenames in os.walk(dirname):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches
# Strip the lib name from a filename
def libname(filename):
    return os.path.splitext(os.path.basename(filename))[0]

class OpenCVConan(ConanFile):
    description = "OpenCV: Open Source Computer Vision Library. This is meant"
        + " to be a cross-platform package for the OpenCV library that builds"
        + " the same regardless the implicit dependencies of OpenCV. The "
        + " missing features might be added to this package at some point "
        + " through explicit Conan package dependencies."
    name = "OpenCV"
    version = "3.2.0"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False]
    }
    default_options = "shared=False"
    url = "https://github.com/ohhi/conan-opencv"
    license = "http://http://opencv.org/license.html"
    generators = "cmake"
    short_paths = True
    build_policy = "missing"

    def source(self):
        self.run("git clone https://github.com/opencv/opencv.git")
        self.run("cd opencv && git checkout tags/3.2.0")

    def build(self):
        cmake = CMake(self.settings)
        cmake_options = {
            "WITH_IPP": True,
            "WITH_QT": False,
            "WITH_OPENGL": False,
            "WITH_CUDA": False,
            "BUILD_SHARED_LIBS": self.options.shared,
            "BUILD_WITH_STATIC_CRT": self.settings.compiler.runtime in ["MT","MTd"],
            "BUILD_TESTS": False,
            "BUILD_PERF_TESTS": False,
            "BUILD_opencv_apps": False,
            "CPACK_BINARY_NSIS": False
        }
        cmake.configure(self, defs=cmake_options, source_dir="opencv")
        cmake.build(self, target="install")

    def package(self):
            self.copy(pattern="*.h*", dst="include", src =os.path.join("install", "include"), keep_path=True)

            self.copy(pattern="*.lib", dst="lib", src="3rdparty", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
            self.copy(pattern="*.exe", dst="bin", src="bin", keep_path=False)

            self.copy(pattern="*.dylib", dst="lib", src="bin", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", src="bin", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs.extend(map(libname, rfnmatch("lib", "*.lib")))
            self.cpp_info.libs.extend(map(libname, rfnmatch("3rdparty", "*.lib")))
        else:
            self.cpp_info.libs.extend(map(libname, rfnmatch("lib", "*.so*")))
            self.cpp_info.libs.extend(map(libname, rfnmatch("3rdparty", "*.so*")))
