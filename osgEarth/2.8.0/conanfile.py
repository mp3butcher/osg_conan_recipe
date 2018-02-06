from conans import ConanFile, CMake, tools
import os
import pip
import subprocess

from conans.tools import os_info, SystemPackageTool

class OpenSceneGraphConan(ConanFile):
    name = "osgEarth"
    version = "2.8"
    license = "https://github.com/gwaldron/osgearth/blob/master/LICENSE.txt"
    url = "https://github.com/gwaldron/osgearth"
    description = "The OpenSceneGraph is an open source high performance 3D graphics toolkit, used by application developers in fields such as visual simulation, games, virtual reality, scientific visualization and modelling. Written entirely in Standard C++ and OpenGL it runs on all Windows platforms, OSX, GNU/Linux, IRIX, Solaris, HP-Ux, AIX and FreeBSD operating systems. The OpenSceneGraph is now well established as the world leading scene graph technology, used widely in the vis-sim, space, scientific, oil-gas, games and virtual reality industries."
    settings = "os", "compiler", "build_type", "arch"
    #do all options had to be wrapped to cmake?
    options = {"shared": [True, False], "dev_deploy": [True, False]}
    default_options = "shared=True", "dev_deploy=True"
    generators = "cmake"
    copy_source_to_build_dir = False
    build_policy = "missing" #"always" #
    short_paths = True #for win<10 naming
    requires = "OpenSceneGraph/3.4.2@demo/testing"
    
    #Manually-specified variables were not used by the project:
    #CONAN_COMPILER
    #CONAN_COMPILER_VERSION
    #CONAN_CXX_FLAGS
    #CONAN_C_FLAGS
    #CONAN_EXPORTED
    #CONAN_LIBCXX
    #CONAN_SHARED_LINKER_FLAGS

    def system_requirements(self):
        self.output.warn("system_requirements: ")
        pack_name = None
        if os_info.linux_distro == "ubuntu":
            self.run('sudo apt-get build-dep openscenegraph', True)
            #gstreamer seams missing after build-dep
            pack_name="libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libasio-dev libcollada-dom2.4-dp-dev libdcmtk-dev libfltk1.3-dev libnvtt-dev libboost-filesystem-dev"
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
        self.checkWin32Dependencies()

        #retrieve OSG 3.4 (seams 3.4.2)	
        self.run("git clone https://github.com/gwaldron/osgearth.git")        
        self.run("cd osgearth && git checkout origin/2.8")
        
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to s   et it properly
        # tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(MyHello)", '''PROJECT(MyHello)
        #include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
        #conan_basic_setup()''')

        
    def build(self):
        cmake = CMake(self)
        cmake.definitions['BUILD_SHARED_LIBS']="ON" if self.options.shared else "OFF"
        cmake.definitions['BUILD_OSGEXAMPLES']='OFF'
        cmake.definitions['BUILD_DOCUMENTATION']='ON'
        cmake.definitions['BUILD_OSGAPPLICATIONS']='ON'
        
        if self.settings.compiler == "Visual Studio":
            cmake.definitions['BUILD_WITH_STATIC_CRT']= "ON" if "MT" in str(self.settings.compiler.runtime) else "OFF"

        cmake.configure(source_dir="%s/osgearth" % self.source_folder)
        cmake.build()

    def package(self):
        #3rd party
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            self.copy("*", dst=".", src="3rdParty")
        
        self.copy("*", dst="include", src="include")
        self.copy("*", dst="include", src="OpenSceneGraph/include")
        self.copy("*", dst="bin", src="bin")
        self.copy("*.so", dst="lib", src="lib")
        self.copy("*.dll", dst="lib", src="lib")
        if not self.options.shared:
            self.copy("*.lib", "lib", "3rdparty/lib", keep_path=False)
            self.copy("*.a", "lib", "3rdparty/lib", keep_path=False)


        #self.copy("*.dll", dst="bin", keep_path=False)
        #self.copy("*.so", dst="lib", keep_path=False)
        #self.copy("*.dylib", dst="lib", keep_path=False)
        #self.copy("*.a", dst="lib", keep_path=False)

        
    def package_info(self):
        self.cpp_info.libs = ["osgEarth"]
        if self.settings.os != "Windows":
            self.env_info.LD_LIBRARY_PATH.append( os.path.join(self.package_folder, "lib"))
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":     
            self.env_info.PATH.append(os.path.join(self.package_folder, "3rdParty/bin"))
      
        
    def checkWin32Dependencies(self):return
        #TODO if  self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            

