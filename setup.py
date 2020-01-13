import sys
from setuptools import setup, find_packages
from kbsbot.nlpengine import __version__

with open('requirements.txt') as f:
    deps = [dep for dep in f.read().split('\n') if dep.strip() != ''
            and not dep.startswith('-e')]
    install_requires = deps

setup(name='nlp_engine',
      description="This microservice is  intended to extract structured information from raw text, to identify intents and entities for KBS bot.",
      long_description=open('README.rst').read(),
      version=__version__,
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      dependency_links=["https://github.com/Runnerly/flakon.git#egg=flakon","git+https://github.com/facebookresearch/fastText#egg=fasttext"],
      install_requires=["flask", "Flask-SQLAlchemy"],
      author="André Herrera",
      author_ewmail="andreherrera97@hotmail.com",
      license="MIT",
      keywords=["chatbots", "microservices", "linked data", "nlp"],
      entry_points={
          'console_scripts': [
              'nlp_engine = kbsbot.nlp_engine.run:app',
          ],
      }
      )
