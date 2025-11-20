#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "cv_bridge/cv_bridge.h"
#include <opencv2/opencv.hpp>
#include "image_conversion/srv/image_conversion.hpp"
#include <chrono>

using namespace std::chrono_literals;

/*
    @brief converting the incomming commands form 
    the cli with appropriate commads for the server 
*/
bool parseBool(const std::string &arg)
{
    return (arg == "1" || arg == "true" || arg == "True" || arg == "TRUE");
}


int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);

    if(argc != 3) {
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "usage: add_two_ints_client X Y");
        return 1;
    }


    std::shared_ptr<rclcpp::Node> node = rclcpp::Node::make_shared("imageConversionclient");
    rclcpp::Client<image_conversion::srv::ImageConversion>::SharedPtr client;
    client = node->create_client<image_conversion::srv::ImageConversion>("/imageConversion");

    auto request = std::make_shared<image_conversion::srv::ImageConversion::Request>();
    
    request->greyscale = parseBool(argv[1]);
    request->color = parseBool(argv[2]);

    while(!client->wait_for_service(1s))
    {
        if(!rclcpp::ok())
        {
            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "interrupted");
            rclcpp::shutdown();
            return 0;
        }

        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "service not available, waiting again");
    }

    auto result = client->async_send_request(request);

    if(rclcpp::spin_until_future_complete(node, result) == rclcpp::FutureReturnCode::SUCCESS)
    {
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "resutl: %d", result.get()->converted);
    }

    rclcpp::shutdown();
    return 0;
}