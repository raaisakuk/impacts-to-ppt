from setuptools import setup, find_packages
import subprocess
with open('requirements.txt') as req:
    requirements = req.read()

setup(name='pedsim',
      version="0.1",
      description='Package to automate the Pedsim Report generation',
      packages = find_packages(),
      author='Raaisa Mahajan, Raghu Ram',
      author_email='raaisa.iitd@gmail.com, raghuram1869@gmail.com',
      classifiers=[
          'Development Status :: 1- Beta',
          'Programming Language :: Python :: 2.7',
          'Topic :: Automation :: Report Generation',
      ],
      install_requires=[
          requirements,
      ],
      tests_require=['pytest'],
      include_package_data=True,
      )
