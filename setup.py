from setuptools import setup
setup(
    name="Lookup",
    version='0.1.0',
    packages=['lookup'],
    description='Lookup AWS stuff',
    author='Chuck Muckamuck',
    author_email='Chuck.Muckamuck@gmail.com',
    install_requires=[
        "boto3>=1.9",
        "Click>=7"
    ],
    entry_points="""
        [console_scripts]
        lookup=lookup.command:cli
    """
)
