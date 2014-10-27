cmake_minimum_required(VERSION 2.8.3)
project(learning_joy)

find_package(catkin REQUIRED COMPONENTS
  joy
  roscpp
  turtlesim
)

catkin_package(
INCLUDE_DIRS include

)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(turtle_teleop_joy src/turtle_teleop_joy.cpp)
target_link_libraries(turtle_teleop_joy ${catkin_LIBRARIES})
