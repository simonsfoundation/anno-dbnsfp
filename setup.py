from setuptools import setup


if __name__ == '__main__':
    setup(
        name='anno-dbnsfp',
        packages=['anno-dbnsfp'],
        version='0.1.0',
        package_data={'anno-dbnsfp': ['denovo_classifier_model_SNP/*',
                                   'denovo_classifier_model_INDEL/*',
                                   'denovo_classifier_config/*', '*.sh']},
        include_package_data=True,
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
            'Operating System :: OS Independent',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License', 
            'Programming Language :: Python',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
            ],
        install_requires=[
            'pandas>=0.17.1'
        ],
    )
