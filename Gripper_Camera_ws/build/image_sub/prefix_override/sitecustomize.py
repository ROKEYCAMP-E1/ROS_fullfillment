import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/kimdahun/fullfillment_ws/Gripper_Camera_ws/install/image_sub'
