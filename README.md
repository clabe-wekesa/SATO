# SATO - Sequence Analysis Toolkit
This Python application, built with PyQt6 and integrated with the BioPython library, serves as a Sequence Analysis Toolkit (SATO). SATO offers a user-friendly graphical interface with multiple tabs for various sequence analysis tasks. Users can perform tasks such as generating consensus sequences from two input sequences, aligning sequences using Clustal Omega or MAFFT, and conducting phylogenetic analysis using MrBayes or FastTree. The application also provides features for visualizing alignment results and phylogenetic trees, making it a versatile tool for researchers and scientists working with biological sequences. 
### Purpose of the Package
The package provides a comprehensive and user-friendly solution for biologists and researchers working with biological sequence data. It aims to streamline and simplify various sequence analysis tasks, including generating consensus sequences, conducting sequence alignments, and performing phylogenetic analysis. By offering a graphical user interface (GUI) and integrating with external tools and libraries like BioPython, Clustal Omega, MAFFT, MrBayes, FastTree, Jalview, and FigTree, the package empowers users to efficiently analyze and visualize biological sequence data, making it a valuable resource for molecular biology and bioinformatics research. 
### Features
SATO is a powerful Sequence Analysis Toolkit that offers a range of features for working with biological sequences. Whether you need to generate consensus sequences, perform sequence alignment, or conduct phylogenetic analysis, SATO has you covered. Below are some of the key features of this application:
### Consensus Sequence Generation
   - Users can provide two sequences in FASTA format.
   - The app generates a consensus sequence by finding the best overlapping window that minimizes mismatches while maximizing sequence length.
### Sequence Alignment
   - Users can perform sequence alignment using either Clustal Omega or MAFFT.
   - Input sequences are validated for FASTA format.
   - Aligned sequences are displayed in a user-friendly format.
### Phylogenetic Analysis
   - Users can conduct phylogenetic analysis using either MrBayes (Bayesian Phylogeny) or FastTree (Maximum Likelihood).
   - Supports both DNA and Protein sequences.
   - The app handles input alignments in FASTA or Nexus format.
   - Generates a phylogenetic tree and visualizes it using FigTree.
### User-Friendly Interface
   - The app offers a tabbed interface for easy navigation between different analysis functions. 
### Installation Instructions
**1. Python Environment** - Make sure you have Python 3.x installed on your system. You can download Python from the official website: Python Downloads

**2. Python Packages** - Install the required Python packages using pip:
```bash
pip install PyQt6
pip install biopython
```
**3. Others include:**
- [Clustal Omega](http://www.clustal.org/omega/) and/or [MAFFT](https://mafft.cbrc.jp/alignment/software/) for sequence alignment
- [MrBayes](https://nbisweden.github.io/MrBayes/) and/or [FastTree](http://www.microbesonline.org/fasttree/) for phylogenetic analysis
- [Jalview](https://www.jalview.org/) and [FigTree](http://tree.bio.ed.ac.uk/software/figtree/) for visualization and analysis of multiple sequence alignment and phylogenetic trees respectively

### Usage
After installation, open the terminal.
Type sato and press Enter to launch the SATO application.
SATO is designed to be cross-platform and works on Windows, macOS, and Linux using the same installation and execution commands. Users on any of these operating systems can easily install and run SATO using the provided instructions.

### Acknowledgment
1. Huelsenbeck, J. P., & Ronquist, F. (2001). MRBAYES: Bayesian inference of phylogenetic trees. Bioinformatics, 17(8), 754-755.
2. Price, M. N., Dehal, P. S., & Arkin, A. P. (2009). FastTree: computing large minimum evolution trees with profiles instead of a distance matrix. Molecular biology and evolution, 26(7), 1641-1650.
3. Sievers, F., Wilm, A., Dineen, D., Gibson, T. J., Karplus, K., Li, W., Lopez, R., McWilliam, H., Remmert, M., Söding, J., Thompson, J. D., & Higgins, D. G. (2011). Fast, scalable generation of high-quality protein multiple sequence alignments using Clustal Omega. Molecular systems biology, 7, 539. https://doi.org/10.1038/msb.2011.75
4. Katoh, K., Misawa, K., Kuma, K., & Miyata, T. (2002). MAFFT: a novel method for rapid multiple sequence alignment based on fast Fourier transform. Nucleic acids research, 30(14), 3059–3066. https://doi.org/10.1093/nar/gkf436
5. Rambaut, A. (2009). FigTree. Tree figure drawing tool. http://tree. bio. ed. ac. uk/software/figtree/.
6. Waterhouse, A., Procter, J., Martin, D.A. and Barton, G.J., 2005. Jalview: visualization and analysis of molecular sequences, alignments, and structures. BMC Bioinformatics, 6(3), pp.1-1.
### Contribution
Should you notice a bug, please let us know through issues in the, [GitHub Issue Tracker](https://github.com/clabe-wekesa/SATO/issues)

### Author
[Dr. Clabe Wekesa](https://www.ice.mpg.de/246268/group-members)
 
