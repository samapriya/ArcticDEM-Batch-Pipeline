from setuptools import setup
from setuptools import find_packages
def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='arcticdem',
    version='0.2.0',
    packages=find_packages(),
    package_data={'arcticdem':['*.*']},
    url='https://github.com/samapriya/ArcticDEM-Batch-Pipeline',
    license='Apache 2.0',
    install_requires=['requests>=2.21.1',
                      'progressbar2>=3.38.0',
                      'rtree>=0.9.4',
                      'beautifulsoup4',
                      'retrying>=1.3.3',
                      'pyproj>=1.9.5.1;platform_system!="Windows"',
                      'shapely>=1.6.4;platform_system!="Windows"',
                      'fiona>=1.8.6;platform_system!="Windows"',
                      'geopandas>=0.5.0;platform_system!="Windows"',
                      ],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: GIS',
    ),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.4',
    author='Samapriya Roy',
    author_email='samapriya.roy@gmail.com',
    description='ArcticDEM Batch Download & Processing Tools',
    entry_points={
        'console_scripts': [
            'arcticdem=arcticdem.arcticdem:main',
        ],
    },
)
