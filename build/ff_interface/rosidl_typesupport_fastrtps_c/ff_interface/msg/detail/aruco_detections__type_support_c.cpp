// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from ff_interface:msg/ArucoDetections.idl
// generated code does not contain a copyright notice
#include "ff_interface/msg/detail/aruco_detections__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "ff_interface/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "ff_interface/msg/detail/aruco_detections__struct.h"
#include "ff_interface/msg/detail/aruco_detections__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "geometry_msgs/msg/detail/pose_array__functions.h"  // poses
#include "rosidl_runtime_c/primitives_sequence.h"  // marker_ids
#include "rosidl_runtime_c/primitives_sequence_functions.h"  // marker_ids

// forward declare type support functions
ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_ff_interface
size_t get_serialized_size_geometry_msgs__msg__PoseArray(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_ff_interface
size_t max_serialized_size_geometry_msgs__msg__PoseArray(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_ff_interface
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, geometry_msgs, msg, PoseArray)();


using _ArucoDetections__ros_msg_type = ff_interface__msg__ArucoDetections;

static bool _ArucoDetections__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _ArucoDetections__ros_msg_type * ros_message = static_cast<const _ArucoDetections__ros_msg_type *>(untyped_ros_message);
  // Field name: marker_ids
  {
    size_t size = ros_message->marker_ids.size;
    auto array_ptr = ros_message->marker_ids.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: poses
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, geometry_msgs, msg, PoseArray
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->poses, cdr))
    {
      return false;
    }
  }

  return true;
}

static bool _ArucoDetections__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _ArucoDetections__ros_msg_type * ros_message = static_cast<_ArucoDetections__ros_msg_type *>(untyped_ros_message);
  // Field name: marker_ids
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->marker_ids.data) {
      rosidl_runtime_c__int32__Sequence__fini(&ros_message->marker_ids);
    }
    if (!rosidl_runtime_c__int32__Sequence__init(&ros_message->marker_ids, size)) {
      fprintf(stderr, "failed to create array for field 'marker_ids'");
      return false;
    }
    auto array_ptr = ros_message->marker_ids.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: poses
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, geometry_msgs, msg, PoseArray
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->poses))
    {
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ff_interface
size_t get_serialized_size_ff_interface__msg__ArucoDetections(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ArucoDetections__ros_msg_type * ros_message = static_cast<const _ArucoDetections__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name marker_ids
  {
    size_t array_size = ros_message->marker_ids.size;
    auto array_ptr = ros_message->marker_ids.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name poses

  current_alignment += get_serialized_size_geometry_msgs__msg__PoseArray(
    &(ros_message->poses), current_alignment);

  return current_alignment - initial_alignment;
}

static uint32_t _ArucoDetections__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_ff_interface__msg__ArucoDetections(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ff_interface
size_t max_serialized_size_ff_interface__msg__ArucoDetections(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: marker_ids
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: poses
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_geometry_msgs__msg__PoseArray(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = ff_interface__msg__ArucoDetections;
    is_plain =
      (
      offsetof(DataType, poses) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _ArucoDetections__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_ff_interface__msg__ArucoDetections(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_ArucoDetections = {
  "ff_interface::msg",
  "ArucoDetections",
  _ArucoDetections__cdr_serialize,
  _ArucoDetections__cdr_deserialize,
  _ArucoDetections__get_serialized_size,
  _ArucoDetections__max_serialized_size
};

static rosidl_message_type_support_t _ArucoDetections__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_ArucoDetections,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, ff_interface, msg, ArucoDetections)() {
  return &_ArucoDetections__type_support;
}

#if defined(__cplusplus)
}
#endif
