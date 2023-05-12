import os
from setuptools import setup, PEP420PackageFinder
from setuptools.dist import Distribution
from wheel.bdist_wheel import bdist_wheel

def get_torch_xla_version():
    return os.environ['TORCH_XLA_VERSION']

def get_torch_version():
    return os.environ['PYTORCH_VERSION'] + '.*'

class BinaryDistribution(Distribution):

    def has_ext_modules(self):
        return True


class bdist_wheel_plat_only(bdist_wheel):

    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False

    def get_tag(self):
        python, abi, plat = super().get_tag()
        python, abi = 'py3', 'none'
        return python, abi, plat

exec(open('src/neuronx_distributed/_version.py').read())
setup(
    name='neuronx-distributed',
    version=__version__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='aws neuron',
    packages=PEP420PackageFinder.find(where='src'),
    package_dir={'': 'src'},
    package_data={'': [
        'LICENSE.txt',
    ]},
    install_requires=[
        f'torch-neuronx=={get_torch_version()}',
        f'torch-xla=={get_torch_xla_version()}',
    ],
    distclass=BinaryDistribution,
    cmdclass={
        'bdist_wheel': bdist_wheel_plat_only,
    },
)
