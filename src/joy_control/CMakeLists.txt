cmake_minimum_required(VERSION 2.8.3)
project(joy_control)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  joy
  roscpp
  visualization_msgs
  std_msgs
  genmsg
)

catkin_package(
INCLUDE_DIRS include
)

include_directories(

  ${catkin_INCLUDE_DIRS}
)

add_executable(joy_control src/joy_control.cpp)
target_link_libraries(joy_control ${catkin_LIBRARIES})
