# osg_conan_recipe
experiment conan with osg

# Setup 

## get Python
https://www.python.org/

## get Conan
http://docs.conan.io/en/latest/installation.html

Easiest way is through Pypi : 

pip install conan

# Instructions

2 simple ways to create package

## 1) Automated package creation

conan create OpenSceneGraph/3.4.2 demo/testing

conan create VirtualPlanetBuilder/1.0 demo/testing

....

## 2) Manual Export Recipe (local), install and test package
conan export OpenSceneGraph/3.4.2 demo/testing

conan install OpenSceneGraph/3.4.2@demo/testing

conan test OpenSceneGraph/3.4.2/test_package OpenSceneGraph/3.4.2@demo/testing 




 
