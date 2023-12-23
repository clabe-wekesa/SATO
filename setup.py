import setuptools

# Read README for long description
with open('README.md', 'r', encoding='utf-8') as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setuptools.setup(
    name="SATO",
    version="0.0.3",
    description='Python package that generates consensus sequence from the forward and reverse sequences, performs multiple sequence alignment of the fasta sequences, and generates phylogenetic trees using Bayesian and Maximum Likelihood Methods',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
    author='Clabe Wekesa',
    author_email='simiyu86wekesa@gmail.com',
    url="https://github.com/clabe-wekesa/SATO",
    keywords=['consensus', 'alignment', 'phylogenetics', 'bioinformatics'],
    install_requires=[
        'PyQt6',
        'Biopython'
    ],
    python_requires='>=3.6',
    packages=['SATO'],
    package_dir={'SATO': 'SATO'},
    package_data={
        'SATO': ['about_intro.txt', 'help.txt', 'stylesheet.css', 'icons/*.png', 'programs/*'],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'sato = SATO.SATO:main',
        ],
    },
    scripts=['run.py'],
)

