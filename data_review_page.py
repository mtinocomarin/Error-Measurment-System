
#############################################################################################################
# Project Name: Motor Skill Acquisition Error Management System (San Francisco State University Project 2024) 
# 
# Filename: data_review_page.py
# 
# Authors: Milton Tinoco, Ethan Weldon, Joshua Samson, Michael Cabrera
#
# Last Update: 12/08/2024
#
# File Description:
# This file contains the code for the data review page, which loads data from a Results_File.txt file,
# displays it in a table, and provides options to export the data, show statistics, and generate graphs.
#
###########################################################################################################

# Import necessary libraries

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QFileDialog, QDialog
)
from PyQt5.QtCore import Qt
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMessageBox

# Class: DataReviewPage
# Description:
# This class represents the data review page of the application.
# It allows users to load data from a Results_File.txt file, display it in a table,
# export the data to Excel or CSV, show statistics, and generate graphs.

class DataReviewPage(QWidget):
    def __init__(self, parent=None):  # Add parent as an optional argument
        super().__init__(parent)  # Pass parent to the base class constructor
        self.parent = parent 
        self.setWindowTitle("Data Review Page")
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        # Data storage
        self.data = None
        self.file_path = None

        # Label for data review
        # This add text to the data review page
        self.data_label = QLabel("Data Review Page")
        self.data_label.setAlignment(Qt.AlignCenter)
        self.data_label.setStyleSheet("font-size: 20px")
        layout.addWidget(self.data_label)

        # Table to display data
        # This creates a table to display the data
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(4)
        self.data_table.setHorizontalHeaderLabels(["Image Trial", "Z-Axis", "Y-Axis", "X-Axis"])
        layout.addWidget(self.data_table)

        # Buttons
        button_layout = QHBoxLayout()

        # Button to load folder
        # This button allows the user to load a folder
        self.load_folder_button = QPushButton("Load Folder")
        self.load_folder_button.setStyleSheet("font-size: 16px")
        self.load_folder_button.clicked.connect(self.load_folder)
        button_layout.addWidget(self.load_folder_button)

        # Button to export data
        # This button allows the user to export the data
        self.export_button = QPushButton("Export Data")
        self.export_button.setStyleSheet("font-size: 16px")
        self.export_button.clicked.connect(self.export_data)
        button_layout.addWidget(self.export_button)

        # Button to display statistics
        # This button allows the user to display statistics
        self.stats_button = QPushButton("Show Statistics")
        self.stats_button.setStyleSheet("font-size: 16px")
        self.stats_button.clicked.connect(self.show_statistics)
        button_layout.addWidget(self.stats_button)

        # Button to display graphs
        # This button allows the user to display graphs
        self.graphs_button = QPushButton("Show Graphs")
        self.graphs_button.setStyleSheet("font-size: 16px")
        self.graphs_button.clicked.connect(self.show_graphs)
        button_layout.addWidget(self.graphs_button)

        # Button to go back to main menu
        # This button allows the user to go back to the main menu
        self.back_button = QPushButton("Back to Menu")
        self.back_button.setStyleSheet("font-size: 16px")
        self.back_button.clicked.connect(self.go_to_main_menu)
        button_layout.addWidget(self.back_button)

        # Add button layout to the main layout
        layout.addLayout(button_layout)
        self.setLayout(layout)

    # Method: load_folder
    # Description:
    # Load the folder and read data from Results_File.txt.
    # Input: None
    # Output: None
    def load_folder(self):
        # Select a folder
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Folder", os.path.expanduser("~")
        )
        if folder_path:
            # Construct the file path
            results_file = os.path.join(folder_path, "Results", "Results_File.txt") # Results_File.txt path
            if os.path.exists(results_file):
                self.file_path = results_file
                self.read_and_display_data(results_file)
            else:
                self.data_label.setText("Results_File.txt not found in the selected folder.")

    # Method: read_and_display_data
    # Description:
    # Read data from Results_File.txt and display it in the table.
    # Input: file_path - Path to the Results_File.txt
    # Output: None

    def read_and_display_data(self, file_path):
        """Read data from Results_File.txt and display it in the table."""
        try:
            data = []
            with open(file_path, "r") as file:
                for line in file:
                    line = line.strip()  # Remove leading/trailing whitespace
                    if not line or line.startswith("Image Index") or line.startswith("="):
                        # Skip empty lines, headers, and separator lines
                        continue

                    # Extract the data from a well-structured line
                    if line.startswith("Image Trial:"):
                        try:
                            trial = line.split("Image Trial:")[1].split()[0]
                            z_axis = line.split("Z-Axis:")[1].split()[0]
                            y_axis = line.split("Y-Axis:")[1].split()[0]
                            x_axis = line.split("X-Axis:")[1].split()[0]
                            data.append([int(trial), float(z_axis), float(y_axis), float(x_axis)])
                        except (IndexError, ValueError):
                            
                            continue

            # Save data for exporting
            self.data = pd.DataFrame(data, columns=["Image Trial", "Z-Axis", "Y-Axis", "X-Axis"])

            # Populate the table
            self.data_table.setRowCount(len(data))
            for row_idx, row_data in enumerate(data):
                for col_idx, value in enumerate(row_data):
                    self.data_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            self.data_label.setText(f"Loaded data from: {file_path}")

        except Exception as e:
            self.data_label.setText(f"Error reading file: {str(e)}")


    # Method: show_statistics
    # Description:
    # Display enhanced statistics such as mean, median, standard deviation, and variability metrics.
    # Input: None
    # Output: None
    def show_statistics(self):
        if self.data is not None:
            stats_summary = "Statistics:\n"

            for column in self.data.columns[1:]:
                column_data = self.data[column]
                
                # Basic numerical measures
                # Mean, median, and mode
                mean_value = column_data.mean()
                median_value = column_data.median()
                mode_value = column_data.mode().iloc[0] if not column_data.mode().empty else "No mode"
                
                # Spread and variability measures
                # Standard deviation, variance, range, and interquartile range
                std_dev = column_data.std()
                variance = column_data.var()
                data_range = column_data.max() - column_data.min()
                iqr = column_data.quantile(0.75) - column_data.quantile(0.25)
                
                # Additional measure: max difference percentage
                # Calculate the maximum difference percentage from the mean
                absolute_difference = (column_data - mean_value).abs()
                max_difference = absolute_difference.max()
                max_difference_percentage = (max_difference / mean_value) * 100 if mean_value != 0 else 0

                # Append statistics for this column to the summary
                # Format the statistics with two decimal places
                stats_summary += (
                    f"Column: {column}\n"
                    f"  Mean (Average): {mean_value:.2f}\n"
                    f"  Median (Midpoint): {median_value:.2f}\n"
                    f"  Mode (Most Frequent): {mode_value}\n"
                    f"  Standard Deviation (Spread): {std_dev:.2f}\n"
                    f"  Variance: {variance:.2f}\n"
                    f"  Range (Max - Min): {data_range:.2f}\n"
                    f"  Interquartile Range (IQR): {iqr:.2f}\n"
                    f"  Max Difference (%): {max_difference_percentage:.2f}%\n"
                    "\n"
                )

            # Display the statistics in a dialog
            # Create a message box to show the statistics summary
            stats_dialog = QMessageBox()
            stats_dialog.setWindowTitle("Statistics Summary")
            stats_dialog.setText(stats_summary)
            stats_dialog.exec_() # Execute the dialog
        else:
            self.data_label.setText("No data ")

    # Method: show_graphs
    # Description:
    # Generate and display graphs for the Z-Axis, Y-Axis, and X-Axis data.
    # Input: None
    # Output: None

    def show_graphs(self):
        if self.data is not None:
            # Plot Z-Axis
            plt.figure()
            plt.plot(self.data["Image Trial"], self.data["Z-Axis"], marker="o", label="Z-Axis")
            plt.xlabel("Image Trial")
            plt.ylabel("Z-Axis")
            plt.title("Z-Axis vs. Image Trial")
            plt.legend()
            plt.grid(True)

            # Plot Y-Axis
            plt.figure()
            plt.plot(self.data["Image Trial"], self.data["Y-Axis"], marker="o", label="Y-Axis", color="green")
            plt.xlabel("Image Trial")
            plt.ylabel("Y-Axis")
            plt.title("Y-Axis vs. Image Trial")
            plt.legend()
            plt.grid(True)

            # Plot X-Axis
            plt.figure()
            plt.plot(self.data["Image Trial"], self.data["X-Axis"], marker="o", label="X-Axis", color="red")
            plt.xlabel("Image Trial")
            plt.ylabel("X-Axis")
            plt.title("X-Axis vs. Image Trial")
            plt.legend()
            plt.grid(True)

            plt.show()
        else:
            self.data_label.setText("No data loaded to generate graphs.")

    # Method: export_data
    # Description:
    # Export the data to Excel or CSV.
    # Input: None
    # Output: None

    def export_data(self):
        """Export the data to Excel or CSV."""
        if self.data is not None:
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save File", os.path.expanduser("~"),
                "Excel Files (*.xlsx);;CSV Files (*.csv)"
            )
            if save_path:
                if save_path.endswith(".xlsx"):
                    self.data.to_excel(save_path, index=False)
                elif save_path.endswith(".csv"):
                    self.data.to_csv(save_path, index=False)
                else:
                    self.data_label.setText("Invalid file format selected.")
                self.data_label.setText(f"Data exported to: {save_path}")
        else:
            self.data_label.setText("No data to export.")

    def go_to_main_menu(self):
        """Go back to the main menu."""
        if self.parent and hasattr(self.parent, "stack"):
            self.parent.stack.setCurrentWidget(self.parent.main_menu)
