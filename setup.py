from setuptools import setup
from setuptools import find_packages


setup(name='DSPP-Keras',
      version='0.0.1',
      description='Integration of DSPP database with Keral Machine Learning Library',
      author='Jan Domanski',
      author_email='jan@peptone.io',
      url='https://github.com/PeptoneInc/dspp-keras',
      download_url='https://github.com/PeptoneInc/dspp-keras/tarball/0.0.1',
      license='MIT',
      install_requires=['keras', 'numpy'],
      packages=find_packages())
