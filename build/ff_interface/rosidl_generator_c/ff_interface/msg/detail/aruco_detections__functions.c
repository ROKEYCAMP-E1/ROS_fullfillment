// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from ff_interface:msg/ArucoDetections.idl
// generated code does not contain a copyright notice
#include "ff_interface/msg/detail/aruco_detections__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `marker_ids`
#include "rosidl_runtime_c/primitives_sequence_functions.h"
// Member `poses`
#include "geometry_msgs/msg/detail/pose_array__functions.h"

bool
ff_interface__msg__ArucoDetections__init(ff_interface__msg__ArucoDetections * msg)
{
  if (!msg) {
    return false;
  }
  // marker_ids
  if (!rosidl_runtime_c__int32__Sequence__init(&msg->marker_ids, 0)) {
    ff_interface__msg__ArucoDetections__fini(msg);
    return false;
  }
  // poses
  if (!geometry_msgs__msg__PoseArray__init(&msg->poses)) {
    ff_interface__msg__ArucoDetections__fini(msg);
    return false;
  }
  return true;
}

void
ff_interface__msg__ArucoDetections__fini(ff_interface__msg__ArucoDetections * msg)
{
  if (!msg) {
    return;
  }
  // marker_ids
  rosidl_runtime_c__int32__Sequence__fini(&msg->marker_ids);
  // poses
  geometry_msgs__msg__PoseArray__fini(&msg->poses);
}

bool
ff_interface__msg__ArucoDetections__are_equal(const ff_interface__msg__ArucoDetections * lhs, const ff_interface__msg__ArucoDetections * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // marker_ids
  if (!rosidl_runtime_c__int32__Sequence__are_equal(
      &(lhs->marker_ids), &(rhs->marker_ids)))
  {
    return false;
  }
  // poses
  if (!geometry_msgs__msg__PoseArray__are_equal(
      &(lhs->poses), &(rhs->poses)))
  {
    return false;
  }
  return true;
}

bool
ff_interface__msg__ArucoDetections__copy(
  const ff_interface__msg__ArucoDetections * input,
  ff_interface__msg__ArucoDetections * output)
{
  if (!input || !output) {
    return false;
  }
  // marker_ids
  if (!rosidl_runtime_c__int32__Sequence__copy(
      &(input->marker_ids), &(output->marker_ids)))
  {
    return false;
  }
  // poses
  if (!geometry_msgs__msg__PoseArray__copy(
      &(input->poses), &(output->poses)))
  {
    return false;
  }
  return true;
}

ff_interface__msg__ArucoDetections *
ff_interface__msg__ArucoDetections__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ff_interface__msg__ArucoDetections * msg = (ff_interface__msg__ArucoDetections *)allocator.allocate(sizeof(ff_interface__msg__ArucoDetections), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(ff_interface__msg__ArucoDetections));
  bool success = ff_interface__msg__ArucoDetections__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
ff_interface__msg__ArucoDetections__destroy(ff_interface__msg__ArucoDetections * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    ff_interface__msg__ArucoDetections__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
ff_interface__msg__ArucoDetections__Sequence__init(ff_interface__msg__ArucoDetections__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ff_interface__msg__ArucoDetections * data = NULL;

  if (size) {
    data = (ff_interface__msg__ArucoDetections *)allocator.zero_allocate(size, sizeof(ff_interface__msg__ArucoDetections), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = ff_interface__msg__ArucoDetections__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        ff_interface__msg__ArucoDetections__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
ff_interface__msg__ArucoDetections__Sequence__fini(ff_interface__msg__ArucoDetections__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      ff_interface__msg__ArucoDetections__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

ff_interface__msg__ArucoDetections__Sequence *
ff_interface__msg__ArucoDetections__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ff_interface__msg__ArucoDetections__Sequence * array = (ff_interface__msg__ArucoDetections__Sequence *)allocator.allocate(sizeof(ff_interface__msg__ArucoDetections__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = ff_interface__msg__ArucoDetections__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
ff_interface__msg__ArucoDetections__Sequence__destroy(ff_interface__msg__ArucoDetections__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    ff_interface__msg__ArucoDetections__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
ff_interface__msg__ArucoDetections__Sequence__are_equal(const ff_interface__msg__ArucoDetections__Sequence * lhs, const ff_interface__msg__ArucoDetections__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!ff_interface__msg__ArucoDetections__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
ff_interface__msg__ArucoDetections__Sequence__copy(
  const ff_interface__msg__ArucoDetections__Sequence * input,
  ff_interface__msg__ArucoDetections__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(ff_interface__msg__ArucoDetections);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    ff_interface__msg__ArucoDetections * data =
      (ff_interface__msg__ArucoDetections *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!ff_interface__msg__ArucoDetections__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          ff_interface__msg__ArucoDetections__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!ff_interface__msg__ArucoDetections__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
