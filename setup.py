import os
from glob import glob
from setuptools import setup
from setuptools import find_packages

package_name = 'bot_tutorial'

data_files=[
  ...
  (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
  (os.path.join('share', package_name), glob('urdf/*')),
],

setup(
    name=package_name,
    packages=[package_name],
    data_files=[
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name), glob('urdf/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'state_publisher = bot_tutorial.state_publisher:main'
        ],
    },
)