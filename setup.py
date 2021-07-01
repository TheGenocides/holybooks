from setuptools import setup, find_packages
 
with open('README.md', 'r', encoding = 'utf-8') as f:
    long_description = f.read()

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
	name='holybooks',
	version='0.1.2',
	url='https://github.com/TheGenocides/holybooks',
	description='An Api Wrapper for extracting info from: quran api and bible api.',
	long_description=long_description,
	long_description_content_type = 'text/markdown',  
	author='TheGenocide',
	author_email='luke.genesis.hyder@gmail.com',
	license='MIT', 
	classifiers=classifiers,
	keywords=['holybooks', 'holybook', 'scripture', 'kitab', 'quran', 'bible', 'torah'], 
	packages=find_packages(),
	install_requires=['requests', 'aiohttp'] 
)
