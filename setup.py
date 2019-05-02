import pip
import setuptools

with open('requirements.txt', 'r') as f:
    requirements = f.read()

with open('README.md', 'r') as f:
    long_description = f.read()

name = 'cp2webhook'

setuptools.setup(
    name=name,
    version='@@VERSION@@',
    author='HARDWARIO s.r.o.',
    author_email='ask@hardwario.com',
    description='COOPER to Webhook',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hardwario/cp2webhook',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'
    ],
    keywords='cooper influxdb iot',
    platforms='any',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            '%s=%s:main' % (name, name)
        ]
    }
)
