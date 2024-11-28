// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from ff_interface:msg/ArucoDetections.idl
// generated code does not contain a copyright notice

#ifndef FF_INTERFACE__MSG__DETAIL__ARUCO_DETECTIONS__STRUCT_H_
#define FF_INTERFACE__MSG__DETAIL__ARUCO_DETECTIONS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'marker_ids'
#include "rosidl_runtime_c/primitives_sequence.h"
// Member 'poses'
#include "geometry_msgs/msg/detail/pose_array__struct.h"

/// Struct defined in msg/ArucoDetections in the package ff_interface.
typedef struct ff_interface__msg__ArucoDetections
{
  /// 감지된 마커들의 ID 리스트
  rosidl_runtime_c__int32__Sequence marker_ids;
  /// 각 마커의 PoseArray (position + orientation)
  geometry_msgs__msg__PoseArray poses;
} ff_interface__msg__ArucoDetections;

// Struct for a sequence of ff_interface__msg__ArucoDetections.
typedef struct ff_interface__msg__ArucoDetections__Sequence
{
  ff_interface__msg__ArucoDetections * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} ff_interface__msg__ArucoDetections__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // FF_INTERFACE__MSG__DETAIL__ARUCO_DETECTIONS__STRUCT_H_
