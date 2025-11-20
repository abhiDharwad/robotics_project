#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "cv_bridge/cv_bridge.h"
#include <opencv2/opencv.hpp>
#include "image_conversion/srv/image_conversion.hpp"
#include <memory>
#include <functional>
#include <chrono>



class ImageConvertServer : public rclcpp::Node {
public: 
    ImageConvertServer() : Node("OpencvImageConverter"), publishGray_(false), publishColor_(false), converted_(false)
    {
        this->declare_parameter<std::string>("cameraTopic", "/camera1/image_raw");
        this->declare_parameter<std::string>("imageOutputTopic", "/convertedImage");

        cameraTopic = this->get_parameter("cameraTopic").as_string();
        imageTopic = this->get_parameter("imageOutputTopic").as_string();

        subscriber_ = this->create_subscription<sensor_msgs::msg::Image>(cameraTopic, 10,
        [this](const sensor_msgs::msg::Image::SharedPtr msg)
        {
            this->converterCallback(msg);
        });

        publisher_ = this->create_publisher<sensor_msgs::msg::Image>(imageTopic, 10);

        server_ = this->create_service<image_conversion::srv::ImageConversion>("/imageConversion", 
        [this](const std::shared_ptr<image_conversion::srv::ImageConversion::Request> req,
            const std::shared_ptr<image_conversion::srv::ImageConversion::Response> res){this->serverCallback(req, res);});

        RCLCPP_INFO(this->get_logger(), "server is ready!");
    }
private:

    /*
        @brief subscriber callback function convert the image into opecv Mat format 
            and back to ros msg format, then publishing the message continously 
            according to the client call 
    */
    void converterCallback(const sensor_msgs::msg::Image::SharedPtr msg) {

        try{
            cv::Mat frame = cv_bridge::toCvShare(msg, "bgr8")->image;
            cv::Mat outPutImg;

            if(publishGray_) {
                cv::cvtColor(frame, outPutImg, cv::COLOR_BGR2GRAY);
                cv_bridge::CvImage cv_image(std_msgs::msg::Header(), "mono8", outPutImg);
                auto rosmsg = cv_image.toImageMsg();
                publisher_->publish(*rosmsg);
                RCLCPP_INFO(this->get_logger(), "Publishing grayscale image");
                converted_ = true;
            }

            if(publishColor_) {
                cv_bridge::CvImage cv_image(std_msgs::msg::Header(), "bgr8", frame);
                auto rosmsg = cv_image.toImageMsg();
                publisher_->publish(*rosmsg);
                RCLCPP_INFO(this->get_logger(), "Publishing color image");
                converted_ = true;
            }

        } catch(cv_bridge::Exception& ex){
            RCLCPP_INFO(this->get_logger(), "cv_bridge execption %s", ex.what());
        }

    }

    /*
        @brief servercallback function for setting the request grayscale or the color
            according to the service client call
    */
    void serverCallback(const std::shared_ptr<image_conversion::srv::ImageConversion::Request> req,
                        const std::shared_ptr<image_conversion::srv::ImageConversion::Response> res)
        {
            RCLCPP_INFO(this->get_logger(), "req->greyscale: %d", req->greyscale);

            if (req->color == true) {
                publishGray_ = false;
                publishColor_ = true;
                } else if (req->greyscale == true) {
                publishColor_ = false;
                publishGray_ = true;
                } else {
                publishGray_ = false;
                publishColor_ = false;
                }

            res->converted = publishGray_ || publishColor_;

            RCLCPP_INFO(this->get_logger(), "response: %d", res->converted);
        }

    rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr subscriber_;
    rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr publisher_;
    rclcpp::Service<image_conversion::srv::ImageConversion>::SharedPtr server_;
    bool publishGray_;
    bool publishColor_;
    bool converted_;
    std::string cameraTopic, imageTopic;
};


int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ImageConvertServer>());
    rclcpp::shutdown();
    return 0;
}