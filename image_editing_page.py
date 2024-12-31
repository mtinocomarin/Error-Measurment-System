
############################################################################################
# Project Name: Motor Skill Acquisition Error Management System (San Francisco State University Project 2024) 
# 
# Filename: image_editing_page.py
# 
# Authors: Milton Tinoco, Ethan Weldon, Joshua Samson, Michael Cabrera
#
# Last Update: 12/08/2024
#
# File Description:
# This file contains the code for the image editing page, where users can select points on images
# to calculate real-world measurements. The EditPage class allows users to select a center point
# and a puck point on the image to calculate the z-axis, y-axis, and x-axis values. The calculated
# values are displayed on the screen and saved to a text file. The page also provides navigation
# options to move between images and return to the main menu. At the end of the image list, users
# can choose to go to the data review page, return to the main menu, or exit the program.
#
############################################################################################

# Import necessary libraries

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QPoint, QTimer, pyqtSignal
from calculation_class import CalculationsManager
from file_manger_class import FileManager
from image_interface import ImageView
import os
import math
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QFileDialog


# Class: EditPage
# Description:
# This class represents the image editing page where users can select points on images to calculate
# real-world measurements. The EditPage class allows users to select a center point and a puck point
# on the image to calculate the z-axis, y-axis, and x-axis values. The calculated values are displayed
# on the screen and saved to a text file. The page also provides navigation options to move between images
# and return to the main menu. At the end of the image list, users can choose to go to the data review page,
# return to the main menu, or exit the program.
class EditPage(QWidget):
    def __init__(self, parent): 
        super().__init__()
        self.parent = parent # Save the reference to the parent

        # Initialize the file manager and calculations manager objects
        self.file_manager = FileManager()
        self.calculations_manager = CalculationsManager()

        # Initialize the class attributes

        self.folder_path = None  # Store the selected folder path
        self.image_path = None  # Store the selected image path
        self.axis = None  # Store the selected axis
        self.scaling_factor = None # Store the scaling factor
        self.image_list = []  # List to store the image paths in the selected folder
        self.image_index = 1 # Index of the current image being displayed
        self.center_point = None  # Store the center point of the image
        self.clicked_points = []  # List to store the clicked points on the image
        self.result_file_path = None # Store the path to the result file
        self.result_folder_path = None # Store the path to the result folder
        self.information_file_path = None # Store the path to the information file
        self.track_clicks = 1  # Number of clicks to track
        self.zaxis = None # Store the calculated z-axis value
        self.yaxis = None # Store the calculated y-axis value
        self.xaxis = None # Store the calculated x-axis value
        self.vertical_axis = None # Store the vertical axis

        self.layout = QVBoxLayout() # Create a vertical layout for the page

        # Direction label 

        # Create text on the top of the page of directions for the user
        self.direction_label = QLabel("Please click the center")
        # Set the alignment of the text to center
        self.direction_label.setAlignment(Qt.AlignCenter)
        # Set the font size, weight, and margin for the text
        self.direction_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        # Add the text to the layout
        self.layout.addWidget(self.direction_label)

        # create a horizontal layout for button

        axis_button_layout = QHBoxLayout()

        # Button to reselect the center point
        # Description: This button allows the user to reselect the center point on the image.
        self.center_button = QPushButton("Reselect Center")
        self.center_button.setEnabled(False)
        self.center_button.clicked.connect(self.reselect_center)
        axis_button_layout.addWidget(self.center_button)
        self.center_button.hide()

        # Button to go back to the previous image
        # Description: This button allows the user to go back to the previous image in the list.
        self.previous_button = QPushButton("Previous Image")
        self.previous_button.clicked.connect(self.previous_image)
        axis_button_layout.addWidget(self.previous_button)

        # Add the horizontal layout to the main vertical layout
        self.layout.addLayout(axis_button_layout)

        # Info Label

        # Create text on top of image to display the information
        self.info_label = QLabel(f"Image Number [{self.image_index}] | z axis: {self.zaxis} | y axis: {self.yaxis} | x axis: {self.xaxis}")
        # Set the alignment of the text to center
        self.info_label.setAlignment(Qt.AlignCenter)
        # Set the font size, weight, and margin for the text
        self.info_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        # Add the text to the layout
        self.layout.addWidget(self.info_label)

        # Image viewer
        # Create an image viewer widget
        self.image_viewer = ImageView()
        # Set the image viewer to track two clicks
        self.image_viewer.track_clicks = self.track_clicks
        # Add the image viewer to the layout
        self.layout.addWidget(self.image_viewer)
        self.setLayout(self.layout)

        # Connect the point_clicked signal from the ImageView to the point_clicked method
        self.image_viewer.point_clicked.connect(self.handle_point_clicked)

    # Method: handle_point_clicked
    # Description:
    # Handle the event when a point is clicked on the image.
    # Append the clicked point to the list of clicked points.
    # Calculate the z-axis, y-axis, and x-axis values based on the selected points.
    # Append the calculated data to the results file.
    # Update the info label with the calculated data.
    # Display the next image after a delay.
    # Input: x - x-coordinate of the clicked point
    #        y - y-coordinate of the clicked point
    # Output: None

    def handle_point_clicked(self, x, y):

        # check if the track_clicks is 1 which means that center point is selected
        if self.track_clicks == 1:
            # Append the center point if not already in the list
            if self.center_point and self.center_point not in self.clicked_points:
                self.clicked_points.append(self.center_point)
                self.image_viewer.draw_point_circle(self.center_point[0], self.center_point[1])
            
            # Append the clicked point to the list of clicked points
            self.clicked_points.append((x, y)) 
            # Check if the number of clicked points is 2 to calculate the values
            if len(self.clicked_points) == 2:
                # update the direction label
                self.direction_label.setText("Next image will be displayed in 2 seconds.")
                self.image_viewer.track_clicks = self.track_clicks
                self.calulate_and_display() # Calculate the z-axis, y-axis, and x-axis values

        # check if the track_clicks is 2 which means that not selected or reselecting the center point
        else:  
            self.clicked_points.append((x, y)) # Append the clicked point to the list of clicked points

            # Update the direction label for user next step
            if len(self.clicked_points) == 1: 
                self.direction_label.setText("Please click on the puck.")

            # Check if the number of clicked points is 2 to go to the next step to calculate the values
            if len(self.clicked_points) == 2:
                # give update to the user
                self.direction_label.setText("Next image will be displayed in 2 seconds.")
                # Set the center point to the first clicked point
                self.center_point = self.clicked_points[0]
                # Set the track_clicks to 1 to and update the next time to only need to click on the puck
                self.track_clicks = 1
                # update the image viewer to track the clicks
                self.image_viewer.track_clicks = self.track_clicks 
                self.calulate_and_display() # Calculate the z-axis, y-axis, and x-axis values
                self.center_button.show() # Show the reselect center button
                self.center_button.setEnabled(True) # Enable the reselect center button

    # Method: calulate_and_display
    # Description:
    # Adjust the coordinates based on the user selected axes and center point.
    # Calculate the z-axis, y-axis, and x-axis values based on the selected points.
    # Append the calculated data to the results file.
    # Update the info label with the calculated data.
    # 
    # Input: None
    # Output: None

    def calulate_and_display(self):
        # Calculate the offset to make clicked_points[0] the origin
        # Relative x and y values based on the origin point
        origin_x, origin_y = self.clicked_points[0]
        relative_x = self.clicked_points[1][0] - origin_x
        relative_y = self.clicked_points[1][1] - origin_y

        # Determine vertical and horizontal values based on the selected axes
        if  self.axis == 0 and self.vertical_axis == 3:
            # Vertical: +y to -y (top to bottom)
            # Horizontal: -x to +x (right to left)
            vertical_value = relative_x
            horizontal_value = -relative_y

        elif self.axis == 1 and self.vertical_axis == 3:
            # Vertical: +y to -y (bottom to top)
            # Horizontal: +x to -x (right to left)
            vertical_value = -relative_x
            horizontal_value = -relative_y

        elif self.axis == 2 and self.vertical_axis == 1:
            # Vertical +x to -x (top to bottom)
            # Horizontal: -y to +y (left to right)
            vertical_value = -relative_y
            horizontal_value = relative_x
      
        elif self.axis == 3 and self.vertical_axis == 1:
            # Vertical +x to -x (top to bottom)
            # Horizontal: +y to  (left to right)
            vertical_value = -relative_y
            horizontal_value = -relative_x
     
        else:
            # Handle invalid combinations
            raise ValueError(
                f"Invalid axis combination: horizontal_axis={self.axis}, vertical_axis={self.vertical_axis}"
            )


        # Calculate the z-axis error using the adjusted vertical and horizontal values
        self.zaxis = self.calculations_manager.calculate_error(
            0, 0, vertical_value, horizontal_value, self.scaling_factor
        )

        # If z-axis error is zero, set x and y to zero
        if self.zaxis == 0:
            self.xaxis = 0
            self.yaxis = 0
        else:
            # Calculate real-world coordinates using the adjusted vertical and horizontal values
            self.xaxis, self.yaxis = self.calculations_manager.calculate_real_world_coordinates(
                0, 0, vertical_value, horizontal_value, self.scaling_factor
            )

        # Append the calculated data to the results file
        self.file_manager.append_axis_data(
            self.result_file_path, self.image_index, self.zaxis, self.yaxis, self.xaxis
        )

        # Update the info label with the calculated data
        self.info_label.setText(
            f"Image Number [{self.image_index}] | z axis: {self.zaxis} | y axis: {self.yaxis} | x axis: {self.xaxis}"
        )

        # Display the next image after a delay
        QTimer.singleShot(2000, lambda: self.next_image("Please click on the puck"))

    # Method: reselect_center
    # Description:
    # Allow the user to reselect the center point on the image.
    # Reset the track_clicks to 2 and update the image viewer.
    # Load the current image with a message to click on the center again.
    # Input: None
    # Output: None
    def reselect_center(self):
        self.track_clicks = 2
        self.image_viewer.track_clicks = self.track_clicks
        self.load_image(self.image_index, "Please click on the center again to reselect")
    
    # Method: load_image
    # Description:
    # Load the image at the specified index from the image list.
    # Update the direction label with the specified text.
    # Clear the clicked points and load the image in the image viewer.
    # Input: index - index of the image to load
    #        text - text to display in the direction label
    # Output: None
    def load_image(self,index,text):
   
        # Validate index
        if index < 0 or index >= len(self.image_list):
            raise IndexError("Index out of range for image list.")
        # Get image path from the list
        image_path = self.image_list[index]
        # Validate image file existence
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        # Clear clicked points
        self.image_viewer.click_list = []  # Clear internal clicked points
        self.clicked_points = []  # Clear external clicked points
        # Load the image
        self.image_path = image_path  # Update the current image path
        self.direction_label.setText(text)
        # Load the image in the image viewer
        self.image_viewer.load_image(image_path)  
        # Draw the center point if center point is selected
        if self.track_clicks == 1:
            self.image_viewer.draw_point_circle(self.center_point[0], self.center_point[1])

    # Method: next_image
    # Description:
    # Load the next image in the image list.
    # Increment the image index and update the information label.
    # Draw the center point on the image viewer.
    # Load the next image with a message to click on the center.
    # Input: text - text to display in the direction label
    # Output: None

    def next_image(self, text):
        # Check if the image index is less than the total number of images otherwise the user has reached the end of the images
        if self.image_index < len(self.image_list) - 1: 
            # Increment the image index and update information
            self.image_index += 1 
            self.info_label.setText(f" Total Images [{len(self.image_list) - 1}] Image Trial [{self.image_index}] | z axis: None | y axis: None | x axis: None")
            self.image_viewer.draw_point_circle(self.center_point[0], self.center_point[1]) 
            self.load_image(self.image_index, text)

        else:
            # If at the end of the image list, remove image viewer and add options
            QMessageBox.information(self, "End of Images", "All images have been processed.")

            # Add a label to indicate completion
            completion_label = QLabel("Processing complete! What would you like to do next?")
            completion_label.setAlignment(Qt.AlignCenter)
            completion_label.setStyleSheet("font-size: 18px; font-weight: bold;")
            self.layout.addWidget(completion_label)

            # Add a button to navigate to the Data Review Page
            data_review_button = QPushButton("Go to Data Review")
            data_review_button.setStyleSheet("font-size: 16px; padding: 10px;")
            data_review_button.clicked.connect(self.go_to_data_review)
            self.layout.addWidget(data_review_button)

            # Add a button to return to the main menu
            main_menu_button = QPushButton("Back to Main Menu")
            main_menu_button.setStyleSheet("font-size: 16px; padding: 10px;")
            main_menu_button.clicked.connect(self.go_to_main_menu)
            self.layout.addWidget(main_menu_button)

            # Add a button to exit the program
            exit_button = QPushButton("Exit Program")
            exit_button.setStyleSheet("font-size: 16px; padding: 10px;")
            exit_button.clicked.connect(self.exit_program)
            self.layout.addWidget(exit_button)

    # Method: go_to_data_review
    # Description:
    # Navigate to the DataReviewPage and load the result file.
    # Input: None
    # Output: None
    def go_to_data_review(self):
        """Navigate to the DataReviewPage and load the result file."""
        if self.result_file_path:
            self.parent.data_review_page.read_and_display_data(self.result_file_path)
            self.parent.stack.setCurrentWidget(self.parent.data_review_page)
        else:
            QMessageBox.warning(self, "File Missing", "Result file path is not available.")

    # Method: go_to_main_menu
    # Description:
    # Navigate back to the main menu.
    # Input: None
    # Output: None
    def go_to_main_menu(self):
        """Navigate back to the main menu."""
        self.parent.stack.setCurrentWidget(self.parent.main_menu)

    # Method: exit_program
    # Description:
    # Exit the program.
    # Input: None
    # Output: None
    def exit_program(self):
        """Exit the program."""
        QApplication.quit()

        
    # Method: previous_image
    # Description:
    # Load the previous image in the image list.
    # Decrement the image index and update the information label.
    # Remove the last line from the results file.
    # Load the previous image with a message to click on the puck.
    # Input: text - text to display in the direction label
    # Output: None
    def previous_image(self,text):
        if self.image_index > 1:
            self.image_index -= 1
            text = "Loaded previous image please click on the puck"
            self.info_label.setText(f"Previous:  Total Images [{len(self.image_list) - 1}] Image Trial [{self.image_index}] | z axis: None | y axis: None | x axis: None")
            self.file_manager.remove_last_line(self.result_file_path)
            self.zaxis = None
            self.xaxis = None
            self.yaxis = None
            self.load_image( self.image_index, text)
        else:
            QMessageBox.warning(self, "Start of Images", "This is the first image.")


    # Method: create_files_list
    # Description:
    # Create the list of image files in the selected folder.
    # Create the Results folder and Results file.
    # Input: folder_path - path to the folder containing images
    #        image_path - path to the selected image
    # Output: None

    def create_files_list(self, folder_path, image_path):

        # Constants for results folder and file
        RESULTS_FOLDER_NAME = "Results"
        RESULTS_FILE_NAME = "Results_File.txt"


        # Ensure image_path is the first in the image list
        self.image_list = [
            os.path.normpath(os.path.join(folder_path, f))
            for f in os.listdir(folder_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))
        ]

        # Normalize image_path for comparison
        normalized_image_path = os.path.normpath(image_path)

        # Remove image_path if it exists and insert it at the beginning

        if normalized_image_path in self.image_list:
            self.image_list.remove(normalized_image_path)
        self.image_list.insert(0, normalized_image_path)

        # Create Results folder
        results_folder_path = os.path.join(folder_path, RESULTS_FOLDER_NAME)
        if not os.path.exists(results_folder_path):
            self.result_folder_path = self.file_manager.create_folder(folder_path, folder_name=RESULTS_FOLDER_NAME)
        else:
            self.result_folder_path = results_folder_path

        # Create Results file
        results_file_path = os.path.join(self.result_folder_path, RESULTS_FILE_NAME)
        if not os.path.exists(results_file_path):
            self.result_file_path = self.file_manager.create_text_file(self.result_folder_path, file_name=RESULTS_FILE_NAME)
        else:
            self.result_file_path = results_file_path


    # Method: set_data
    # Description:
    # Set the data required for image editing.
    # Input: scaling_factor - scaling factor for the image
    #        folder_path - path to the folder containing images
    #        image_path - path to the selected image
    #        result_file_path - path to the result file
    # Output: None

    # def load_image(self, image_path,index,text):

    def set_data(self, scaling_factor, folder_path, image_path, axis, vertical_axis):
     
        self.scaling_factor = scaling_factor
        self.folder_path = folder_path
        self.axis = axis
        self.create_files_list(folder_path, image_path)
        self.track_clicks = 2
        self.vertical_axis = vertical_axis
        self.image_viewer.track_clicks = self.track_clicks
        self.load_image(self.image_index, "Please click on the center")