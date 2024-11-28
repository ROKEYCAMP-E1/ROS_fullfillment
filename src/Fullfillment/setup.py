from setuptools import find_packages, setup

package_name = 'Fullfillment'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(include=[package_name, f"{package_name}.*"]),  # 모든 하위 디렉토리 포함
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'rclpy', 'opencv-python'],  # 필요한 의존성 추가
    zip_safe=True,
    maintainer='rokey',
    maintainer_email='sy3180@gamil.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'UI_node = Fullfillment.UI.ui_node:main',
            'TopView_Camera_node = Fullfillment.TopView_Camera.TopView_Camera_node:main',
        ],
    },
)
