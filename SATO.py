import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QTextEdit, QFileDialog, QRadioButton, QTabWidget,
    QPushButton, QComboBox, QGridLayout
)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QFile, QTextStream, QIODevice
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Align.Applications import ClustalOmegaCommandline
from Bio.Align.Applications import MafftCommandline
from Bio import AlignIO
from io import StringIO
import subprocess
import shutil
from .validation import (
    is_protein_alignment, text_formatting,
    is_fasta_aligned, is_nexus_aligned, is_valid_fasta
)

# Define a custom exception for your application
class CustomError(Exception):
    def __init__(self, message):
        super().__init__(message)
class SATOApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.molecule_type = "DNA"  # Initialize molecule_type attribute
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SATO - Sequence Analysis Toolkit')
        # Get the directory of the current script
        script_directory = os.path.dirname(os.path.abspath(__file__))
        # Construct the absolute path to the icon file
        icon_path = os.path.join(script_directory, 'icons/sato.png')
        # Set the window icon
        self.setWindowIcon(QIcon(icon_path))
        self.setGeometry(100, 100, 750, 500)
        self.setContentsMargins(30, 30, 30, 30)

        # Get the absolute path of the directory containing this script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to stylesheet.css
        stylesheet_path = os.path.join(script_dir, "stylesheet.css")

        # Read the stylesheet from the external file
        with open(stylesheet_path, "r") as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)
        
        # Create the central widget
        central_widget = QTabWidget(self)
        self.setCentralWidget(central_widget)

        # Create tabs for Consensus Sequence, Sequence Alignment and Phylogenetic Analysis
        image_page = QWidget()
        about_tab = QWidget()
        help_tab = QWidget()
        consensus_tab = QWidget()
        alignment_tab = QWidget()
        phylogenetic_tab = QWidget()

        central_widget.addTab(image_page, 'SATO')
        central_widget.addTab(about_tab, 'About')
        central_widget.addTab(help_tab, 'Help')  # Set 'Help' as the first tab
        central_widget.addTab(consensus_tab, 'Consensus Sequence')
        central_widget.addTab(alignment_tab, 'Sequence Alignment')
        central_widget.addTab(phylogenetic_tab, 'Phylogenetic Analysis')


        # Initialize tabs
        self.initSATOTab(image_page)
        self.initAboutTab(about_tab)
        self.initHelpTab(help_tab)
        self.initConsensusTab(consensus_tab)
        self.initAlignmentTab(alignment_tab)
        self.initPhylogeneticTab(phylogenetic_tab)

    def delete_files_in_output_folder(self):
        output_folder = "output"
        for file_name in os.listdir(output_folder):
            file_path = os.path.join(output_folder, file_name)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error deleting file or directory {file_path}: {str(e)}")

    def initSATOTab(self, tab):
        # Create a QGridLayout to hold the image and text
        grid_layout = QGridLayout()

        # Create a QLabel for displaying the image
        image_label = QLabel()
        # Determine the full path to the icons directory within the package
        package_directory = os.path.dirname(__file__)
        icons_directory = os.path.join(package_directory, 'icons')

        # Use the full path to load the image
        image_path = os.path.join(icons_directory, 'logo-no-background.png')
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setScaledContents(False)
        image_label.setStyleSheet("margin-bottom: 100px;")

        # Create a QLabel for the text
        text_label = QLabel("Written by Dr. Clabe Wekesa")  # Replace with your desired text

        # Create a QFont instance and set the font size
        font = QFont()
        font.setPointSize(28)

        # Set the new font for the QLabel
        text_label.setFont(font)

        # Set the text alignment
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # You can change the alignment as needed

        # Add the image and text labels to the grid layout
        grid_layout.addWidget(image_label, 0, 0, 1, 1)  # Image at row 0, column 0
        grid_layout.addWidget(text_label, 1, 0, 1, 1)  # Text at row 1, column 0

        tab.setLayout(grid_layout)  # Set the layout for the tab, not the main window

    def initHelpTab(self, tab):
        layout = QVBoxLayout()
        # Create a QLabel for displaying the help content
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        # Get the formatted text using the text_formatting function
        formatted_text = text_formatting('help.txt')
        # Set the formatted text as HTML content
        help_text.setHtml(formatted_text)
        layout.addWidget(help_text)
        tab.setLayout(layout)

    def initConsensusTab(self, tab):
        layout = QVBoxLayout()

        # Create horizontal layout for file selection
        input_layout = QVBoxLayout()

        # Create labels to display file paths
        self.file1_path_label = QLabel()
        self.file2_path_label = QLabel()

        # File 1
        self.file1_label = QLabel('Forward Sequence (FASTA format)')
        # Determine the full path to the icons directory within the package
        package_directory = os.path.dirname(__file__)
        icons_directory = os.path.join(package_directory, 'icons')

        # Use the full path to load the icon
        icon_path = os.path.join(icons_directory, 'fasta.png')

        # Create the QPushButton with the QIcon
        self.file1_button = QPushButton(QIcon(icon_path), 'Browse')
        self.file1_button.clicked.connect(self.get_file1)
        self.file1_path = ""  # Store the selected file path
        input_layout.addWidget(self.file1_label)
        input_layout.addWidget(self.file1_button)
        input_layout.addWidget(self.file1_path_label)  # Add the path label

        # File 2
        self.file2_label = QLabel('Reverse Sequence (FASTA format)')
        # Use the same icon path as for self.file1_button
        self.file2_button = QPushButton(QIcon(icon_path), 'Browse')
        self.file2_button.clicked.connect(self.get_file2)
        self.file2_path = ""  # Store the selected file path
        input_layout.addWidget(self.file2_label)
        input_layout.addWidget(self.file2_button)
        input_layout.addWidget(self.file2_path_label)  # Add the path label

        layout.addLayout(input_layout)

        # Submit button
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.generate_consensus)
        layout.addWidget(self.submit_button)

        # Consensus sequence display
        self.result_label = QLabel('Consensus Sequence:')
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_text)

        tab.setLayout(layout)

    def get_file1(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select FASTA File 1", "",
                                                   "FASTA Files (*.fasta *.fa);;All Files (*)")
        if file_name:
            self.file1_path = file_name
            self.file1_path_label.setText(os.path.basename(file_name))  # Display only the filename

    def get_file2(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select FASTA File 2", "",
                                                   "FASTA Files (*.fasta *.fa);;All Files (*)")
        if file_name:
            self.file2_path = file_name
            self.file2_path_label.setText(os.path.basename(file_name))  # Display only the filename

    def generate_consensus(self):
        fasta_file1 = self.file1_path
        fasta_file2 = self.file2_path

        try:
            consensus_seq = self.consensus_sequence(fasta_file1, fasta_file2)
            self.result_text.setPlainText(consensus_seq)
        except CustomError as e:
            self.result_text.setPlainText(f" {str(e)}")

    def initAlignmentTab(self, tab):
        layout = QVBoxLayout()

        # Create a vertical layout for alignment options
        alignment_layout = QVBoxLayout()

        # Create labels and input fields for alignment options
        self.alignment_label = QLabel('Alignment Options:')
        self.alignment_label.setFont(QFont())
        self.alignment_input_label = QLabel('Select FASTA File for Alignment:')
        self.alignment_input_label.setFont(QFont())

        # Determine the full path to the icons directory within the package
        package_directory = os.path.dirname(__file__)
        icons_directory = os.path.join(package_directory, 'icons')

        # Use the full path to load the icon
        icon_path = os.path.join(icons_directory, 'fasta.png')
        self.alignment_input_file_button = QPushButton(QIcon(icon_path), 'Browse')

        self.alignment_input_file_button.clicked.connect(self.get_alignment_file)

        # Add labels for displaying the selected file paths
        self.alignment_input_path_label = QLabel()

        self.alignment_tool_label = QLabel('Alignment Tool')
        self.clustal_radio = QRadioButton('Clustal Omega')
        self.mafft_radio = QRadioButton('MAFFT')
        self.clustal_radio.setChecked(True)  # Default to Clustal Omega

        alignment_layout.addWidget(self.alignment_label)
        alignment_layout.addWidget(self.alignment_input_label)
        alignment_layout.addWidget(self.alignment_input_file_button)
        alignment_layout.addWidget(self.alignment_input_path_label)  # Add the path label
        alignment_layout.addWidget(self.alignment_tool_label)
        alignment_layout.addWidget(self.clustal_radio)
        alignment_layout.addWidget(self.mafft_radio)

        layout.addLayout(alignment_layout)

        # Submit button
        self.alignment_submit_button = QPushButton('Submit')
        self.alignment_submit_button.clicked.connect(self.perform_msa)
        layout.addWidget(self.alignment_submit_button)

        # Text box for displaying the alignment result
        self.alignment_result_label = QLabel('Alignment Result:')
        self.alignment_result_text = QTextEdit()
        self.alignment_result_text.setReadOnly(True)
        layout.addWidget(self.alignment_result_label)
        layout.addWidget(self.alignment_result_text)

        tab.setLayout(layout)

    def get_alignment_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select FASTA File for Alignment", "",
                                                   "FASTA Files (*.fasta *.fa);;All Files (*)")
        if file_name:
            self.upload_path = file_name
            self.alignment_input_path_label.setText(os.path.basename(file_name))  # Display only the filename

    def initAboutTab(self, tab):
        layout = QVBoxLayout()

        # Create a QTextEdit widget for displaying the introductory text
        about_text = QTextEdit()
        about_text.setReadOnly(True)

        # Get the formatted text using the text_formatting function
        formatted_text = text_formatting('about_intro.txt')

        # Set the formatted text as HTML content
        about_text.setHtml(formatted_text)

        #layout.addWidget(image_label)
        layout.addWidget(about_text)

        tab.setLayout(layout)

    def initPhylogeneticTab(self, tab):
        layout = QVBoxLayout()

        # Create vertical layout for phylogenetic analysis options
        phylogen_layout = QVBoxLayout()

        # File selection
        self.phylogen_file_label = QLabel('Select Alignment File for Phylogenetic Analysis:')

        # Get the directory of the current script
        script_directory = os.path.dirname(os.path.abspath(__file__))
        # Construct the absolute path to the icon file
        icon_path = os.path.join(script_directory, 'icons/file.png')
        # Create the QPushButton with the absolute icon path
        self.phylogen_file_button = QPushButton(QIcon(icon_path), 'Browse')

        self.phylogen_file_button.clicked.connect(self.get_phylogen_file)
        self.phylogen_file_path_label = QLabel()  # Add this line to create the label
        self.phylogen_file_path = ""  # Store the selected file path
        phylogen_layout.addWidget(self.phylogen_file_label)
        phylogen_layout.addWidget(self.phylogen_file_button)
        phylogen_layout.addWidget(self.phylogen_file_path_label)  # Add the path label

        # Radio buttons for selecting the tool
        self.tool_label = QLabel('Select Phylogenetic Method')
        self.mrBayes_radio = QRadioButton('Bayesian Phylogeny')
        self.fastTree_radio = QRadioButton('Maximum Likelihood')
        self.mrBayes_radio.setChecked(True)  # Default to MrBayes
        phylogen_layout.addWidget(self.tool_label)
        phylogen_layout.addWidget(self.mrBayes_radio)
        phylogen_layout.addWidget(self.fastTree_radio)

        self.molecule_type_label = QLabel('Molecule Type')
        self.molecule_type_combo = QComboBox()
        self.molecule_type_combo.addItem('DNA')
        self.molecule_type_combo.addItem('Protein')
        self.molecule_type_combo.setCurrentIndex(0)  # Default to DNA
        self.molecule_type_combo.currentIndexChanged.connect(self.update_molecule_type)
        phylogen_layout.addWidget(self.molecule_type_label)
        phylogen_layout.addWidget(self.molecule_type_combo)

        layout.addLayout(phylogen_layout)

        # Submit button
        self.phylogen_submit_button = QPushButton('Submit')
        self.phylogen_submit_button.clicked.connect(self.perform_phylogeny)
        layout.addWidget(self.phylogen_submit_button)

        # Text box for displaying the result
        self.output_text_label = QLabel('Analysis Result:')
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text_label)
        layout.addWidget(self.output_text)

        tab.setLayout(layout)

    def setMoleculeTypeDNA(self):
        self.protein_radio.setChecked(True)

    def setMoleculeTypeProtein(self):
        if self.dna_radio.isChecked():
            self.dna_radio.setChecked(False)

    def get_phylogen_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Alignment File for Phylogenetic Analysis", "",
                                                   "Alignment Files (*.fasta *.fa *.nex);;All Files (*)")
        if file_name:
            self.phylogen_file_path = file_name  # Store the selected file path
            self.phylogen_file_path_label.setText(os.path.basename(file_name))  # Display only the filename

    def perform_phylogeny(self):
        try:
            selected_tool = "Bayesian Phylogeny" if self.mrBayes_radio.isChecked() else "Maximum Likelihood"

            input_file = self.phylogen_file_path  # Use the selected file path

            # Call the phylogeny method
            self.phylogeny(input_file, selected_tool)

        except Exception as e:
            self.output_text.setPlainText(f"Error performing phylogenetic analysis: {str(e)}")

    def update_molecule_type(self, index):
        selected_type = self.molecule_type_combo.currentText()
        if selected_type == 'DNA':
            self.molecule_type = 'DNA'
        elif selected_type == 'Protein':
            self.molecule_type = 'Protein'

    def consensus_sequence(self, fasta_file1, fasta_file2, seq_name="Consensus_sequence"):
        """
        Generate a consensus sequence from two sequences with the overlapping
        window that minimizes mismatches while maximizing sequence length.
        """
        try:
            if not fasta_file1 or not fasta_file2:
                return "Please select both sequences for consensus sequence generation."

            def is_valid_fasta(content):
                """
                Check if the given content is in FASTA format.
                """
                lines = content.strip().split('\n')
                if len(lines) < 2 or not lines[0].startswith('>'):
                    return False
                return True

            # Read sequences from files or directly provided sequences
            if os.path.isfile(fasta_file1):
                with open(fasta_file1, 'r') as file1:
                    content1 = file1.read()
            else:
                content1 = fasta_file1

            if os.path.isfile(fasta_file2):
                with open(fasta_file2, 'r') as file2:
                    content2 = file2.read()
            else:
                content2 = fasta_file2

            # Check if the content is in FASTA format
            if not (is_valid_fasta(content1) and is_valid_fasta(content2)):
                return ("Files provided are not in FASTA format. Please provide FASTA files.")

            # Read sequences from FASTA files
            record1 = SeqIO.read(fasta_file1, "fasta")
            record2 = SeqIO.read(fasta_file2, "fasta")

            # Get sequences as strings
            seq1 = str(record1.seq)
            seq2 = str(record2.seq)

            # Remove non-nucleotide characters
            seq1 = ''.join([base for base in seq1 if base in 'ACGTacgt'])
            seq2 = ''.join([base for base in seq2 if base in 'ACGTacgt'])

            # Reverse complement of seq2
            seq2 = str(Seq(seq2).reverse_complement())

            # Find the best overlapping window
            min_overlap = 0
            max_overlap = min(len(seq1), len(seq2))

            best_overlap = None
            best_mismatches = float('inf')

            for i in range(max_overlap, min_overlap - 1, -1):
                overlap_seq1 = seq1[-i:]
                overlap_seq2 = seq2[:i]

                # Count mismatches
                count_mismatches = sum(1 for a, b in zip(overlap_seq1, overlap_seq2) if a != b)

                if count_mismatches < best_mismatches or (
                        count_mismatches == best_mismatches and i > len(best_overlap[0])):
                    best_overlap = (overlap_seq1, overlap_seq2)
                    best_mismatches = count_mismatches

            if best_overlap is not None:
                consensus_seq = f">{seq_name}\n{seq1 + best_overlap[1]}"
                return consensus_seq

            # If no consensus with acceptable mismatches found, concatenate the sequences
            consensus_seq = f">{seq_name}\n{seq1 + seq2}"
            return consensus_seq

        except FileNotFoundError as e:
            raise CustomError(f"File not found: {str(e)}")

        except Exception as e:
            raise CustomError(f"Files provided are not in FASTA format. Please provide FASTA files. {str(e)}")

    def perform_msa(self):
        try:
            selected_tool = "clustalo" if self.clustal_radio.isChecked() else "mafft"

            # Check if no file is provided
            if not hasattr(self, 'upload_path') or not self.upload_path:
                self.alignment_result_text.setPlainText("Please select a FASTA file for alignment.")
                return False

            input_filename = self.upload_path  # Use the selected file path

            # Check if the file is a valid FASTA file
            if not is_valid_fasta(input_filename):
                self.alignment_result_text.setPlainText(
                    "The selected file is not a valid FASTA file. Please provide a FASTA file.")
                return False

            # Initialize stdout and stderr
            stdout = ""
            stderr = ""

            # Perform the sequence alignment using the selected tool
            if selected_tool == "mafft":
                mafft_cline = MafftCommandline(input=input_filename)
                stdout, stderr = mafft_cline()
            elif selected_tool == "clustalo":
                clustalo_cline = ClustalOmegaCommandline(infile=input_filename, outfmt="fasta")
                stdout, stderr = clustalo_cline()

            # Check if alignment was successful
            if "error" in stderr.lower():
                self.alignment_result_text.setPlainText("Alignment failed. Check input and tool.")
                return False

            # Parse the alignment from stdout
            alignment = AlignIO.read(StringIO(stdout), "fasta")

            # Update the alignment result text box with the alignment content
            self.alignment_result_text.setPlainText(str(alignment))

            # Generate the output filename based on the input filename
            output_file = self.generate_output_filename(input_filename)

            # Save the alignment to the output file
            with open(output_file, "w") as output_handle:
                AlignIO.write(alignment, output_handle, "fasta")

            # Launch Jalview with the alignment file
            jalview_command = ["jalview", "-open", output_file]
            subprocess.Popen(jalview_command)
            return True

        except Exception as e:
            self.alignment_result_text.setPlainText(f"Error: {str(e)}")

    def generate_output_filename(self, input_filename):
        try:
            # Get the base name of the input filename (without the extension)
            base_name = os.path.splitext(os.path.basename(input_filename))[0]

            # Construct the output filename by adding "_alignment.fasta" to the base name
            output_filename = f"{base_name}_alignment.fasta"
            return output_filename
        except Exception as e:
            self.alignment_result_text.setPlainText(f"Error generating output filename: {str(e)}")
            return "alignment.fasta"  # Default to a hardcoded filename if an error occurs

    def phylogeny(self, input_file, tool="Bayesian Phylogeny"):
        try:
            # Use the selected file path
            input_file = self.phylogen_file_path if not input_file else input_file

            # Check if no input file is provided
            if not input_file:
                self.output_text.setPlainText("Please select an alignment file.")
                return

            # Check the alignment format and selected molecular type
            if is_protein_alignment(input_file) and self.molecule_type != "Protein":
                self.output_text.setPlainText(
                    "Error: The selected molecular type must be 'Protein' for protein alignments.")
                return

            # Check if the provided file is aligned
            if not is_fasta_aligned(input_file):
                self.output_text.setPlainText(
                    "Error: The provided alignment file is not aligned. Please provide an aligned FASTA or Nexus file.")
                return

            # Create the output folder if it doesn't exist
            output_folder = "output"
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Use the self.molecule_type variable for molecule type selection
            molecule_type = self.molecule_type

            if tool == "Maximum Likelihood":
                # Run FastTree directly on the input FASTA file to generate a tree file
                base_name = os.path.splitext(os.path.basename(input_file))[0]
                tree_path = os.path.join(output_folder, f"{base_name}.tree")

                # Define the command as a list of strings
                command = ["fasttree", "-out", tree_path, input_file]

                subprocess.run(command, check=True, text=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

            elif tool == "Bayesian Phylogeny":
                if input_file.endswith(".fasta"):
                    # Load FASTA alignment
                    alignment = AlignIO.read(input_file, "fasta")

                    # Define the output Nexus file path in the output folder
                    base_name = os.path.splitext(os.path.basename(input_file))[0]
                    nexus_file_path = os.path.join(output_folder, f"{base_name}.nex")

                    # Write the alignment to a Nexus file with the desired format in the output folder
                    with open(nexus_file_path, "w") as nexus_file:
                        nexus_file.write("#NEXUS\n")
                        nexus_file.write("BEGIN DATA;\n")
                        nexus_file.write(
                            f"    DIMENSIONS NTAX={len(alignment)} NCHAR={alignment.get_alignment_length()};\n")
                        nexus_file.write(f"    FORMAT DATATYPE={molecule_type} MISSING=? GAP=-;\n")
                        nexus_file.write("    MATRIX\n")

                        for record in alignment:
                            nexus_file.write(f"{record.id}\n{record.seq}\n")

                        nexus_file.write("    ;\n")
                        nexus_file.write("END;\n")

                    # Assuming the Nexus file is generated in the 'output' folder
                    nexus_file_path = os.path.join(output_folder, f"{base_name}.nex")

                    # Add MrBayes block to the Nexus file with output file paths in the output folder
                    with open(nexus_file_path, "a") as nexus_file:
                        nexus_file.write("\nBEGIN mrbayes;\n")
                        nexus_file.write(f"    set autoclose=yes nowarn=yes;\n")
                        nexus_file.write("    lset nst=6 rates=invgamma;\n")
                        nexus_file.write("    prset statefreqpr=fixed(equal);\n")
                        nexus_file.write(f"    mcmc ngen=10000;\n")
                        nexus_file.write(f"    sumt burnin=250;\n")
                        nexus_file.write("END;\n")

                    # Run MrBayes with the Nexus file in the output folder as input
                    subprocess.run(["mb", nexus_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    tree_path = os.path.join(output_folder, f"{base_name}.nex.con.tre")

                elif input_file.endswith(".nex"):
                    # Use the provided Nexus file directly
                    base_name = os.path.splitext(os.path.basename(input_file))[0]
                    nexus_file_path = os.path.join(output_folder, f"{base_name}.nex")
                    subprocess.run(["cp", input_file, nexus_file_path], check=True)
                    subprocess.run(["mb", nexus_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    tree_path = os.path.join(output_folder, f"{base_name}.nex.con.tre")

                else:
                    raise Exception("Unsupported file format. Please provide a .fasta or .nex file.")
            else:
                raise Exception("Invalid phylogeny tool selected.")

            # Visualize the tree with FigTree (assuming a tree file is generated)
            subprocess.run(["figtree", tree_path])

            # Delete input files in the output folder
            self.delete_files_in_output_folder()

            result_message = "Phylogenetic analysis completed. Tree visualization opened in FigTree."

            if not input_file:
                result_message += "\nProvide the alignment in fasta format or mrBayes configuration file (only for mrBayes)"

        except Exception as e:
            self.output_text.setPlainText(f"Error performing phylogenetic analysis: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = SATOApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
