from setuptools import setup


if __name__ == '__main__':
    setup(
        name='anno-dbnsfp',
        packages=['anno-dbnsfp'],
        version='0.1.0',
        scripts=['anno-dbnsfp/anno-dbnsfp.py'],
        description='Annotaion of genomic mutations.',
        long_description='Annotate a set of single nucleotide polymorphisms\
        with variables from dbNSFP',
        url='https://github.com/simonsfoundation/anno-dbnsfp',
        author='Andrei Salomatov',
        author_email='Andrei.Salomatov@gmail.com',
        license='MIT',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Operating System :: Linux',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License', 
            'Programming Language :: Python',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
            ],
        install_requires=[
            'pandas',
            'sqlite3',
            'argparse',
            'tempfile',
            'subprocess'
        ],
    )
