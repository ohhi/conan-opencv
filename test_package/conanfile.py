from conans import ConanFile, CMake
import os

class MyTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "OpenCV/3.2.0@ohhi/stable"
    generators = "cmake", "txt"

    def imports(self):
          self.copy("*.dll", dst="bin", src="bin")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=self.conanfile_directory, build_dir=".")
        cmake.build(build_dir=".")
    def test(self):
        self.run(os.path.join(".","bin", "mytest"))
