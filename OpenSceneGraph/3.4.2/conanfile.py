from conans import ConanFile, CMake, tools
import os
import pip
import subprocess

from conans.tools import os_info, SystemPackageTool

class OpenSceneGraphConan(ConanFile):
    name = "OpenSceneGraph"
    version = "3.4.2"
    license = "http://www.openscenegraph.org/images/LICENSE.txt"
    url = "https://github.com/openscenegraph/OpenSceneGraph"
    description = "The OpenSceneGraph is an open source high performance 3D graphics toolkit, used by application developers in fields such as visual simulation, games, virtual reality, scientific visualization and modelling. Written entirely in Standard C++ and OpenGL it runs on all Windows platforms, OSX, GNU/Linux, IRIX, Solaris, HP-Ux, AIX and FreeBSD operating systems. The OpenSceneGraph is now well established as the world leading scene graph technology, used widely in the vis-sim, space, scientific, oil-gas, games and virtual reality industries."
    settings = "os", "compiler", "build_type", "arch"
    #do all options had to be wrapped to cmake?
    options = {"shared": [True, False], "dev_deploy": [True, False]}
    default_options = "shared=True", "dev_deploy=True"
    generators = "cmake"
    copy_source_to_build_dir = False
    build_policy = "missing" #"always" #
    short_paths = True #for win<10 naming
    
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
        self.run("git clone https://github.com/openscenegraph/OpenSceneGraph.git")        
        self.run("cd OpenSceneGraph && git checkout origin/OpenSceneGraph-3.4")
        
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

        cmake.configure(source_dir="%s/OpenSceneGraph" % self.source_folder)
        cmake.build()

    def package(self):
        #3rd party
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            self.copy("*", dst=".", src="3rdParty")
        
        self.copy("*", dst="include", src="include")
        self.copy("*", dst="include", src="OpenSceneGraph/include")
        self.copy("*", dst="bin", src="bin")
        self.copy("*.so*", dst="lib", src="lib")
        self.copy("*.dll", dst="lib", src="lib")
        if not self.options.shared:
            self.copy("*.lib", "lib", "3rdparty/lib", keep_path=False)
            self.copy("*.a", "lib", "3rdparty/lib", keep_path=False)

        self.run("git clone https://github.com/openscenegraph/OpenSceneGraph-Data.git "+ os.path.join(self.package_folder, "OpenSceneGraph-Data"))  
        #self.copy("*.dll", dst="bin", keep_path=False)
        #self.copy("*.so", dst="lib", keep_path=False)
        #self.copy("*.dylib", dst="lib", keep_path=False)
        #self.copy("*.a", dst="lib", keep_path=False)

        
    def package_info(self):
        self.cpp_info.libs = ["osg"]
        self.env_info.OSG_ROOT = self.package_folder
        self.env_info.OSG_FILE_PATH.append( os.path.join(self.package_folder, "OpenSceneGraph-Data"))
        if self.settings.os != "Windows":
            self.env_info.LD_LIBRARY_PATH.append( os.path.join(self.package_folder, "lib"))
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        if self.settings.os == "Windows":     
            self.env_info.PATH.append(os.path.join(self.package_folder, "3rdParty/bin"))
      
        
    def checkWin32Dependencies(self):
        if  self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            #TODO check if 3rd already there self.settings.arch
            self.output.warn('retrieve p7zip win32')
            p7zipurl="http://www.7-zip.org/a/7za920.zip"
            dest_file = "p7zipurl.zip"
            tools.download(p7zipurl, dest_file)
            tools.unzip(dest_file)

            serv="https://download.osgvisual.org/"
            url = ""
            if self.settings.arch == 'x86_64':
                if self.settings.compiler.version ==11: url=serv+"3rdParty_VS2012.3_v110_x86_x64_V8b_full.7z"
                elif self.settings.compiler.version == 12: url=serv+"3rdParty_VS2013.5_v120_x64_V10_full.7z"
                elif self.settings.compiler.version == 14: url=serv+"3rdParty_VS2017_v141_x64_V11_full.7z"

            if url == "": 
                raise Exception("Binary does not exist for these settings edit checkWin32Dependencies() in OSG conan files in order to set 3rd Party url")   
            
            self.output.warn('retrieve built dependency at: '+serv)
            self.output.warn("Downloading: %s" % url)
            dest_file = "OSG3rdParty.7z"
            tools.download(url, dest_file)
            subprocess.call(['7za.exe','x',dest_file])
            if self.settings.arch == 'x86_64':                
                if self.settings.compiler.version == 11 :
                    os.system('move 3rdParty_x86_x64\\x64 3rdParty')
                elif self.settings.compiler.version == 14 or self.settings.compiler.version == 12:
                    os.system('move 3rdParty_x64\\x64 3rdParty')

