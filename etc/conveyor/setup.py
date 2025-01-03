from setuptools import find_packages, setup

package_name = 'conveyor'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(include=['conveyor', 'conveyor.*']),
    include_package_data=True,
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rokey',
    maintainer_email='kim3he@gamil.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'main = conveyor.main:main',
        ],
    },
)
