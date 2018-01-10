from conans import ConanFile, CMake, tools
import os
import pip
import subprocess



class OpenSceneGraphConan(ConanFile):
    name = "OpenSceneGraph"
    version = "3.4.0"
    license = "http://www.openscenegraph.org/images/LICENSE.txt"
    url = "https://github.com/openscenegraph/OpenSceneGraph"
    description = "The OpenSceneGraph is an open source high performance 3D graphics toolkit, used by application developers in fields such as visual simulation, games, virtual reality, scientific visualization and modelling. Written entirely in Standard C++ and OpenGL it runs on all Windows platforms, OSX, GNU/Linux, IRIX, Solaris, HP-Ux, AIX and FreeBSD operating systems. The OpenSceneGraph is now well established as the world leading scene graph technology, used widely in the vis-sim, space, scientific, oil-gas, games and virtual reality industries."
    settings = "os", "compiler", "build_type", "arch"
    #do all options had to be wrapped to cmake?
    options = {"shared": [True, False],"dev_deploy": [True, False]}
    default_options = "shared=True","dev_deploy=True"
    generators = "cmake"
    build_policy = "missing" #"always" #
    short_paths = True #for win<7 naming

    def source(self):
        self.run("git clone https://github.com/mp3butcher/OpenSceneGraph.git")
        self.customDependenciesDownload()
        self.run("cd OpenSceneGraph && git checkout origin/OpenSceneGraph-3.4")
        
        # && git checkout static_shared")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to s   et it properly

       # tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(MyHello)", '''PROJECT(MyHello)
#include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
#conan_basic_setup()''')

        
    def build(self):
        
        cmake = CMake(self)
        cmake.configure(source_dir="%s/OpenSceneGraph" % self.source_folder)
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s' % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        #3rd party
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            self.copy("*", dst="3rdParty", src="3rdParty")
        
        self.copy("*", dst="include", src="include")
        self.copy("*", dst="bin", src="bin")
        self.copy("*", dst="lib", src="lib")
        #self.copy("*.dll", dst="bin", keep_path=False)
        #self.copy("*.so", dst="lib", keep_path=False)
        #self.copy("*.dylib", dst="lib", keep_path=False)
        #self.copy("*.a", dst="lib", keep_path=False)
        
    def deploy(self):
     
        #custom nexus install rule:
        #-all modules install should be called in a common directory
        #(this will then merge all modules in commons bin,lib,include directory  yeah! i'm dirty )
        #can't see how to do without environment variables and path mod
        #i think i may not have understand how deployement suppose to work...
        
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":            
            #3rd party dll and exe
            self.copy("*", dst="bin", src="3rdParty/bin")
        self.copy("*", dst="bin", src="bin")

        if self.options.dev_deploy:            
            #custom install devstuff out of conan cache nexus ..PATH has to be updated by the user
            self.copy("*", dst="lib", src="lib")
            self.copy("*", dst="include", src="include")
            if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
                self.copy("*", dst="lib", src="3rdParty/lib")
                self.copy("*", dst="include", src="3rdParty/include")
        
    def package_info(self):
        self.cpp_info.libs = ["osg"]
        
    def customDependenciesDownload(self):
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

            if url == "": raise Exception("Binary does not exist for these settings edit customDependenciesDownload() in OSG conan files in order to set 3rd Party url")   
            
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

