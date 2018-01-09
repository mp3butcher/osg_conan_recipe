# osg_conan_recipe
experiment conan with osg

# instructions

## google is your friend
get Python
pip install conan

## this project
cd OpenSceneGraph
conan export demo/testing
cd ..
### build from source or retrieve from conan.io
conan install OpenSceneGraph/3.4.0@demo/testing
cd test ; mkdir build;
conan install ..

###force built
cd test ; mkdir build;
conan install .. --build OpenSceneGraph


 
