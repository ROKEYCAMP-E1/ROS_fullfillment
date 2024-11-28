// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from ff_interface:msg/ArucoDetections.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "ff_interface/msg/detail/aruco_detections__rosidl_typesupport_introspection_c.h"
#include "ff_interface/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "ff_interface/msg/detail/aruco_detections__functions.h"
#include "ff_interface/msg/detail/aruco_detections__struct.h"


// Include directives for member types
// Member `marker_ids`
#include "rosidl_runtime_c/primitives_sequence_functions.h"
// Member `poses`
#include "geometry_msgs/msg/pose_array.h"
// Member `poses`
#include "geometry_msgs/msg/detail/pose_array__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__ArucoDetections_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  ff_interface__msg__ArucoDetections__init(message_memory);
}

void ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__ArucoDetections_fini_function(void * message_memory)
{
  ff_interface__msg__ArucoDetections__fini(message_memory);
}

size_t ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__size_function__ArucoDetections__marker_ids(
  const void * untyped_member)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return member->size;
}

const void * ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__get_const_function__ArucoDetections__marker_ids(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void * ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__get_function__ArucoDetections__marker_ids(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__fetch_function__ArucoDetections__marker_ids(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const int32_t * item =
    ((const int32_t *)
    ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__get_const_function__ArucoDetections__marker_ids(untyped_member, index));
  int32_t * value =
    (int32_t *)(untyped_value);
  *value = *item;
}

void ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__assign_function__ArucoDetections__marker_ids(
  void * untyped_member, size_t index, const void * untyped_value)
{
  int32_t * item =
    ((int32_t *)
    ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__get_function__ArucoDetections__marker_ids(untyped_member, index));
  const int32_t * value =
    (const int32_t *)(untyped_value);
  *item = *value;
}

bool ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__resize_function__ArucoDetections__marker_ids(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  rosidl_runtime_c__int32__Sequence__fini(member);
  return rosidl_runtime_c__int32__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__ArucoDetections_message_member_array[2] = {
  {
    "marker_ids",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ff_interface__msg__ArucoDetections, marker_ids),  // bytes offset in struct
    NULL,  // default value
    ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__size_function__ArucoDetections__marker_ids,  // size() function pointer
    ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__get_const_function__ArucoDetections__marker_ids,  // get_const(index) function pointer
    ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__get_function__ArucoDetections__marker_ids,  // get(index) function pointer
    ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__fetch_function__ArucoDetections__marker_ids,  // fetch(index, &value) function pointer
    ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__assign_function__ArucoDetections__marker_ids,  // assign(index, value) function pointer
    ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__resize_function__ArucoDetections__marker_ids  // resize(index) function pointer
  },
  {
    "poses",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ff_interface__msg__ArucoDetections, poses),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__ArucoDetections_message_members = {
  "ff_interface__msg",  // message namespace
  "ArucoDetections",  // message name
  2,  // number of fields
  sizeof(ff_interface__msg__ArucoDetections),
  ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__ArucoDetections_message_member_array,  // message members
  ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__ArucoDetections_init_function,  // function to initialize message memory (memory has to be allocated)
  ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__ArucoDetections_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__ArucoDetections_message_type_support_handle = {
  0,
  &ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__ArucoDetections_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_ff_interface
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ff_interface, msg, ArucoDetections)() {
  ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__ArucoDetections_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, PoseArray)();
  if (!ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__ArucoDetections_message_type_support_handle.typesupport_identifier) {
    ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__ArucoDetections_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &ff_interface__msg__ArucoDetections__rosidl_typesupport_introspection_c__ArucoDetections_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
