from conans import ConanFile, CMake, tools
import os
import pip
import subprocess

from conans.tools import os_info, SystemPackageTool

class VirtualPlanetBuilderConan(ConanFile):
    name = "VirtualPlanetBuilder"
    version = "1.0"
    license = "https://raw.githubusercontent.com/openscenegraph/VirtualPlanetBuilder/master/LICENSE.txt"
    url = "https://github.com/VirtualPlanetBuilder/VirtualPlanetBuilder"
    description = "Tool for generating paged databases from geospatial imagery and heightfields"
    settings = "os", "compiler", "build_type", "arch"
    #do all options had to be wrapped to cmake?
    options = {"shared": [True, False]}
    default_options = "shared=True",
    generators = "cmake"
    #copy_source_to_build_dir = False
    build_policy = "missing" #"always" #
    short_paths = True #for win<10 naming
    requires = "OpenSceneGraph/3.4.2@demo/testing"

    #def requirements(self):  self.requires("OpenSceneGraph/3.4.2@demo/testing")

    def imports(self):
        #self.copy("*", "bin", "bin")
        #self.copy("*", "lib", "lib")
        #self.copy("*", "include", "include")

     def system_requirements(self):
        self.output.warn("system_requirements: ")
        pack_name = None
        if os_info.linux_distro == "ubuntu":
            #gstreamer seams missing after build-dep
            pack_name="libgstreamer1.0-dev libgstreamer1.0-dev"
        elif os_info.linux_distro == "fedora" or os_info.linux_distro == "centos":
            pack_name = "TODOpackage_names_in_fedora_and_centos"
        elif os_info.is_macos:
            pack_name = "TODOpackage_names_in_macos"
        elif os_info.is_freebsd:
            pack_name = "TODOpackage_names_in_freebsd"
        elif os_info.is_solaris:
            pack_name = "TODOpackage_names_in_solaris"

        if pack_name:
            installer = SystemPackageTool()
            installer.install(pack_name) # Install the package, will update the package database if pack_name isn't already installed


    def source(self):       
        self.run("git clone https://github.com/openscenegraph/VirtualPlanetBuilder.git")
        
    def build(self):
        cmake = CMake(self) 
        cmake.configure(source_dir="%s/VirtualPlanetBuilder" % self.source_folder)
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/VirtualPlanetBuilder %s' % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        
        self.copy("*", dst="include", src="VirtualPlanetBuilder/include")
        self.copy("*", dst="bin", src="bin")
        self.copy("*.so", dst="lib", src="lib")
        self.copy("*.dll", dst="lib", src="lib")
        #self.copy("*.dll", dst="bin", keep_path=False)
        #self.copy("*.so", dst="lib", keep_path=False)
        #self.copy("*.dylib", dst="lib", keep_path=False)
        #self.copy("*.a", dst="lib", keep_path=False)
        

        
    def package_info(self):
        self.cpp_info.libs = ["VPB"]
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
        self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        self.cpp_info.libs = []  # The libs to link against
        self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found
        self.cpp_info.bindirs = ['bin']  # Directories where executables and shared libs can be found
        self.cpp_info.defines = []  # preprocessor definitions
        self.cpp_info.cflags = []  # pure C flags
        self.cpp_info.cppflags = []  # C++ compilation flags
        self.cpp_info.sharedlinkflags = []  # linker flags
        self.cpp_info.exelinkflags = []  # linker flags
        
 
