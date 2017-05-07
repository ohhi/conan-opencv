import os, sys
import platform

def system(command):
    retcode = os.system(command)
    if retcode != 0:
        raise Exception("Error while executing:\n\t %s" % command)

if __name__ == "__main__":
    system('conan export ohhi/stable')
    params = " ".join(sys.argv[1:])

    if platform.system() == "Windows":
        system('conan test_package -s compiler="Visual Studio" -s compiler.runtime=MD -s build_type=Release -o OpenCV:shared=False %s' % params)
        system('conan test_package -s compiler="Visual Studio" -s compiler.runtime=MT -s build_type=Release -o OpenCV:shared=False %s' % params)
        system('conan test_package -s compiler="Visual Studio" -s compiler.runtime=MD -s build_type=Release -o OpenCV:shared=True %s' % params)
        system('conan test_package -s compiler="Visual Studio" -s compiler.runtime=MT -s build_type=Release -o OpenCV:shared=True %s' % params)
        system('conan test_package -s compiler="Visual Studio" -s compiler.runtime=MDd -s build_type=Debug -o OpenCV:shared=False %s' % params)
        system('conan test_package -s compiler="Visual Studio" -s compiler.runtime=MDd -s build_type=Debug -o OpenCV:shared=True %s' % params)
        system('conan test_package -s compiler="Visual Studio" -s compiler.runtime=MTd -s build_type=Debug -o OpenCV:shared=False %s' % params)
    else:
        system('conan test_package -s build_type=Release -o OpenCV:shared=False %s' % params)
        system('conan test_package -s build_type=Debug -o OpenCV:shared=False %s' % params)
        system('conan test_package -s build_type=Release -o OpenCV:shared=True %s' % params)
        system('conan test_package -s build_type=Debug -o OpenCV:shared=True %s' % params)
