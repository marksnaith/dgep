import setuptools

long_description = "DGEP"

setuptools.setup(
     name='dgep',
     version='0.1',
     author="Mark Snaith",
     author_email="mark@arg.tech",
     description="Dialogue Game Execution Platform",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="http://arg.tech",
     packages=setuptools.find_packages(),
     install_requires = [
     'dgdl @ git+https://github.com/arg-tech/dgdl-parser.git#egg=dgdl&subdirectory=src'
     ],
     dependency_links=[

     ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
         "Operating System :: OS Independent",
     ],
 )
