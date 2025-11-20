cmake_minimum_required(VERSION 3.8)
project(image_conversion)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(OpenCV REQUIRED)

set(srv_files
  "srv/ImageConversion.srv"
)

rosidl_generate_interfaces(${PROJECT_NAME}
  ${srv_files}
)

ament_export_dependencies(rosidl_default_runtime)

rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} rosidl_typesupport_cpp)
ament_export_dependencies(rosidl_default_runtime)


add_executable(server src/imageConversionServer.cpp)
ament_target_dependencies(server rclcpp sensor_msgs cv_bridge OpenCV)
target_link_libraries(server "${cpp_typesupport_target}")

add_executable(client src/imageConversionClient.cpp)
ament_target_dependencies(client rclcpp sensor_msgs cv_bridge OpenCV)
target_link_libraries(client "${cpp_typesupport_target}")


install(TARGETS 
  server
  client
  DESTINATION   lib/${PROJECT_NAME}
)

install(DIRECTORY 
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
