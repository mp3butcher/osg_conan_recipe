project(osgrequire)
cmake_minimum_required(VERSION 2.8.12)

#add_definitions("-std=c++11")
find_package(OpenSceneGraph 3.2.0 REQUIRED
    osg
    osgDB
    osgUtil
    osgViewer
    osgAnimation
    osgGA
	)
INCLUDE_directories(${OSG_INCLUDE_DIR})
#include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
#conan_basic_setup()

#target_link_libraries(osgrequire)${CONAN_LIBS}
add_executable(osgrequire osgrequire.cpp)
target_link_libraries(osgrequire   ${OPENTHREADS_LIBRARIES}  ${OPENSCENEGRAPH_LIBRARIES} ${OSGVOLUME_LIBRARIES} ${OSGDB_LIBRARIES}
${OSGVIEWER_LIBRARIES}
${OSGUTIL_LIBRARIES}
 ${OSGGA_LIBRARIES})
