import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='scraper',
     version='0.1',
     author="John Oram",
     description="A basic web scraping library",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/joram/py-scraper",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
