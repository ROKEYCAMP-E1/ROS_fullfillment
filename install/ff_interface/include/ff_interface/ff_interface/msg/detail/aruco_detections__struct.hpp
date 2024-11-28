// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from ff_interface:msg/ArucoDetections.idl
// generated code does not contain a copyright notice

#ifndef FF_INTERFACE__MSG__DETAIL__ARUCO_DETECTIONS__STRUCT_HPP_
#define FF_INTERFACE__MSG__DETAIL__ARUCO_DETECTIONS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'poses'
#include "geometry_msgs/msg/detail/pose_array__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__ff_interface__msg__ArucoDetections __attribute__((deprecated))
#else
# define DEPRECATED__ff_interface__msg__ArucoDetections __declspec(deprecated)
#endif

namespace ff_interface
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ArucoDetections_
{
  using Type = ArucoDetections_<ContainerAllocator>;

  explicit ArucoDetections_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : poses(_init)
  {
    (void)_init;
  }

  explicit ArucoDetections_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : poses(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _marker_ids_type =
    std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>>;
  _marker_ids_type marker_ids;
  using _poses_type =
    geometry_msgs::msg::PoseArray_<ContainerAllocator>;
  _poses_type poses;

  // setters for named parameter idiom
  Type & set__marker_ids(
    const std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>> & _arg)
  {
    this->marker_ids = _arg;
    return *this;
  }
  Type & set__poses(
    const geometry_msgs::msg::PoseArray_<ContainerAllocator> & _arg)
  {
    this->poses = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    ff_interface::msg::ArucoDetections_<ContainerAllocator> *;
  using ConstRawPtr =
    const ff_interface::msg::ArucoDetections_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<ff_interface::msg::ArucoDetections_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<ff_interface::msg::ArucoDetections_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      ff_interface::msg::ArucoDetections_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<ff_interface::msg::ArucoDetections_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      ff_interface::msg::ArucoDetections_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<ff_interface::msg::ArucoDetections_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<ff_interface::msg::ArucoDetections_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<ff_interface::msg::ArucoDetections_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__ff_interface__msg__ArucoDetections
    std::shared_ptr<ff_interface::msg::ArucoDetections_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__ff_interface__msg__ArucoDetections
    std::shared_ptr<ff_interface::msg::ArucoDetections_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ArucoDetections_ & other) const
  {
    if (this->marker_ids != other.marker_ids) {
      return false;
    }
    if (this->poses != other.poses) {
      return false;
    }
    return true;
  }
  bool operator!=(const ArucoDetections_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ArucoDetections_

// alias to use template instance with default allocator
using ArucoDetections =
  ff_interface::msg::ArucoDetections_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace ff_interface

#endif  // FF_INTERFACE__MSG__DETAIL__ARUCO_DETECTIONS__STRUCT_HPP_
