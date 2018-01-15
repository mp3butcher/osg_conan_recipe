# osg_conan_recipe
experiment conan with osg

# Instructions

## Google is your friend
- get Python
- pip install conan

## This project

### classic build package from recipes
conan create OpenSceneGraph demo/testing
conan create VirtualPlanetBuilder demo/testing
....

### Export Recipe and test package
conan export OpenSceneGraph demo/testing
conan install OpenSceneGraph/3.4.2@demo/testing
conan test OpenSceneGraph/test_package OpenSceneGraph/3.4.2@demo/testing 




 
