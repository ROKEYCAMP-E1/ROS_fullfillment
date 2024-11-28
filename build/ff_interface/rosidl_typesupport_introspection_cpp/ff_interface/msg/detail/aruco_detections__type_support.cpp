// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from ff_interface:msg/ArucoDetections.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "ff_interface/msg/detail/aruco_detections__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace ff_interface
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void ArucoDetections_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) ff_interface::msg::ArucoDetections(_init);
}

void ArucoDetections_fini_function(void * message_memory)
{
  auto typed_message = static_cast<ff_interface::msg::ArucoDetections *>(message_memory);
  typed_message->~ArucoDetections();
}

size_t size_function__ArucoDetections__marker_ids(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<int32_t> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ArucoDetections__marker_ids(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<int32_t> *>(untyped_member);
  return &member[index];
}

void * get_function__ArucoDetections__marker_ids(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<int32_t> *>(untyped_member);
  return &member[index];
}

void fetch_function__ArucoDetections__marker_ids(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const int32_t *>(
    get_const_function__ArucoDetections__marker_ids(untyped_member, index));
  auto & value = *reinterpret_cast<int32_t *>(untyped_value);
  value = item;
}

void assign_function__ArucoDetections__marker_ids(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<int32_t *>(
    get_function__ArucoDetections__marker_ids(untyped_member, index));
  const auto & value = *reinterpret_cast<const int32_t *>(untyped_value);
  item = value;
}

void resize_function__ArucoDetections__marker_ids(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<int32_t> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ArucoDetections_message_member_array[2] = {
  {
    "marker_ids",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ff_interface::msg::ArucoDetections, marker_ids),  // bytes offset in struct
    nullptr,  // default value
    size_function__ArucoDetections__marker_ids,  // size() function pointer
    get_const_function__ArucoDetections__marker_ids,  // get_const(index) function pointer
    get_function__ArucoDetections__marker_ids,  // get(index) function pointer
    fetch_function__ArucoDetections__marker_ids,  // fetch(index, &value) function pointer
    assign_function__ArucoDetections__marker_ids,  // assign(index, value) function pointer
    resize_function__ArucoDetections__marker_ids  // resize(index) function pointer
  },
  {
    "poses",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::PoseArray>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ff_interface::msg::ArucoDetections, poses),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ArucoDetections_message_members = {
  "ff_interface::msg",  // message namespace
  "ArucoDetections",  // message name
  2,  // number of fields
  sizeof(ff_interface::msg::ArucoDetections),
  ArucoDetections_message_member_array,  // message members
  ArucoDetections_init_function,  // function to initialize message memory (memory has to be allocated)
  ArucoDetections_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ArucoDetections_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ArucoDetections_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace ff_interface


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<ff_interface::msg::ArucoDetections>()
{
  return &::ff_interface::msg::rosidl_typesupport_introspection_cpp::ArucoDetections_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, ff_interface, msg, ArucoDetections)() {
  return &::ff_interface::msg::rosidl_typesupport_introspection_cpp::ArucoDetections_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
