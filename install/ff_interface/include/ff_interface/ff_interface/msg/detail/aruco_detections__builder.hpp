// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from ff_interface:msg/ArucoDetections.idl
// generated code does not contain a copyright notice

#ifndef FF_INTERFACE__MSG__DETAIL__ARUCO_DETECTIONS__BUILDER_HPP_
#define FF_INTERFACE__MSG__DETAIL__ARUCO_DETECTIONS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "ff_interface/msg/detail/aruco_detections__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace ff_interface
{

namespace msg
{

namespace builder
{

class Init_ArucoDetections_poses
{
public:
  explicit Init_ArucoDetections_poses(::ff_interface::msg::ArucoDetections & msg)
  : msg_(msg)
  {}
  ::ff_interface::msg::ArucoDetections poses(::ff_interface::msg::ArucoDetections::_poses_type arg)
  {
    msg_.poses = std::move(arg);
    return std::move(msg_);
  }

private:
  ::ff_interface::msg::ArucoDetections msg_;
};

class Init_ArucoDetections_marker_ids
{
public:
  Init_ArucoDetections_marker_ids()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ArucoDetections_poses marker_ids(::ff_interface::msg::ArucoDetections::_marker_ids_type arg)
  {
    msg_.marker_ids = std::move(arg);
    return Init_ArucoDetections_poses(msg_);
  }

private:
  ::ff_interface::msg::ArucoDetections msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::ff_interface::msg::ArucoDetections>()
{
  return ff_interface::msg::builder::Init_ArucoDetections_marker_ids();
}

}  // namespace ff_interface

#endif  // FF_INTERFACE__MSG__DETAIL__ARUCO_DETECTIONS__BUILDER_HPP_
