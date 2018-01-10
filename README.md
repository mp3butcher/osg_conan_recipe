# osg_conan_recipe
experiment conan with osg

# Instructions

## Google is your friend
- get Python
- pip install conan

## This project
cd OpenSceneGraph

conan export demo/testing

cd ..
### Build from source or retrieve from bintray
conan install OpenSceneGraph/3.4.0@demo/testing

cd test ; mkdir build;

conan install ..

### forced built
cd test ; mkdir build;

conan install .. --build OpenSceneGraph


 
