from conans import ConanFile, CMake
import os

class MyTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "OpenCV/3.4.0-0@ohhi/stable"
    generators = "cmake", "txt"

    def imports(self):
          self.copy("*.dll", dst="bin", src="bin")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build(build_dir=".")
    def test(self):
        self.run(os.path.join(".","bin", "mytest"))
