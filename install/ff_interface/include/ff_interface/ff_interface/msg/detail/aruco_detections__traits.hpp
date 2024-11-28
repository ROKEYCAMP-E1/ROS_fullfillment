// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from ff_interface:msg/ArucoDetections.idl
// generated code does not contain a copyright notice

#ifndef FF_INTERFACE__MSG__DETAIL__ARUCO_DETECTIONS__TRAITS_HPP_
#define FF_INTERFACE__MSG__DETAIL__ARUCO_DETECTIONS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "ff_interface/msg/detail/aruco_detections__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'poses'
#include "geometry_msgs/msg/detail/pose_array__traits.hpp"

namespace ff_interface
{

namespace msg
{

inline void to_flow_style_yaml(
  const ArucoDetections & msg,
  std::ostream & out)
{
  out << "{";
  // member: marker_ids
  {
    if (msg.marker_ids.size() == 0) {
      out << "marker_ids: []";
    } else {
      out << "marker_ids: [";
      size_t pending_items = msg.marker_ids.size();
      for (auto item : msg.marker_ids) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: poses
  {
    out << "poses: ";
    to_flow_style_yaml(msg.poses, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ArucoDetections & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: marker_ids
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.marker_ids.size() == 0) {
      out << "marker_ids: []\n";
    } else {
      out << "marker_ids:\n";
      for (auto item : msg.marker_ids) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: poses
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "poses:\n";
    to_block_style_yaml(msg.poses, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ArucoDetections & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace ff_interface

namespace rosidl_generator_traits
{

[[deprecated("use ff_interface::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const ff_interface::msg::ArucoDetections & msg,
  std::ostream & out, size_t indentation = 0)
{
  ff_interface::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use ff_interface::msg::to_yaml() instead")]]
inline std::string to_yaml(const ff_interface::msg::ArucoDetections & msg)
{
  return ff_interface::msg::to_yaml(msg);
}

template<>
inline const char * data_type<ff_interface::msg::ArucoDetections>()
{
  return "ff_interface::msg::ArucoDetections";
}

template<>
inline const char * name<ff_interface::msg::ArucoDetections>()
{
  return "ff_interface/msg/ArucoDetections";
}

template<>
struct has_fixed_size<ff_interface::msg::ArucoDetections>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<ff_interface::msg::ArucoDetections>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<ff_interface::msg::ArucoDetections>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // FF_INTERFACE__MSG__DETAIL__ARUCO_DETECTIONS__TRAITS_HPP_
