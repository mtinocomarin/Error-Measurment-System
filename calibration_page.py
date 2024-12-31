############################################################################################
# Project Name: Motor Skill Acquisition Error Management System (San Francisco State University Project 2024) 
# 
# Filename: CalibrationPage.py
# 
# Authors: Milton Tinoco, Ethan Weldon, Joshua Samson, Michael Cabrera
#
# Last Update: 12/08/2024
#
# File Description:
# This file contains the code for the calibration page of the application. 
# The calibration page allows users to select a folder of images, choose a calibration image, horizontal and vertical axis,
# and set the distance between two points in the image to calculate a scaling factor for real-world measurements.
# It also reslect the points and axis if the user made a mistake.
# Then proceed to the image editing page to apply the scaling factor to other images.
#
############################################################################################

# Import necessary libraries

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
    QGraphicsPixmapItem, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLabel
)
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QPen
from PyQt5.QtCore import Qt, QLineF
from file_manger_class import FileManager
from calculation_class import CalculationsManager
from image_interface import ImageView
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer


# Class: CalibrationPage
# Description: 
# This class represents the calibration page of the application.
# It allows users to select a folder of images, choose a calibration image,
# and set the distance between two points in the image to calculate a scaling factor for real-world measurements.
# The user can then proceed to the image editing page to apply the scaling factor to other images.

class CalibrationPage(QWidget):
    # Constructor for the CalibrationPage class
    def __init__(self, parent):
        super().__init__()

        # Set the parent widget
        self.parent = parent

        # Initialize the file manager
        self.file_manager = FileManager()

        # Initialize the calculations manager
        self.calculations_manager = CalculationsManager()

        # Set vertical layout for buttons
        self.layout = QVBoxLayout()

        # Direction label 

        # Create text on the top of the page of directions for the user
        self.direction_label = QLabel("Please select a folder with image set, then select a calibration image.") 
        # Set the alignment of the text to center
        self.direction_label.setAlignment(Qt.AlignCenter)
        # Set the font size, weight, and margin for the text
        self.direction_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        # Add the text to the layout
        self.layout.addWidget(self.direction_label)

        # Button to select folder
        # Create a button to select a folder with images
        self.select_folder_button = QPushButton("Select Folder")
        # Connect the button to the select_folder method
        self.select_folder_button.clicked.connect(self.select_folder)
        # Add the button to the layout
        self.layout.addWidget(self.select_folder_button)

        # Label to display selected folder
        # create a text label to display the selected folder path
        self.folder_label = QLabel("No folder selected.")
        # Set the alignment of the text to center
        self.layout.addWidget(self.folder_label)

        # Button to select image
        # Create a button to select a calibration image
        self.select_image_button = QPushButton("Reselect Image")
        # Initially disable the button
        self.select_image_button.setEnabled(False)  # Initially disabled
        # Connect the button to the select_image method
        self.select_image_button.clicked.connect(self.select_image)
        # Add the button to the layout
        self.layout.addWidget(self.select_image_button)
        # Initially hide the button
        self.select_image_button.hide()

        # Button to reselect the points
        # Create a button to reselect the points
        self.reselect_points_button = QPushButton("Reselect Points")
        # Initially disable the button
        self.reselect_points_button.setEnabled(False)
        # Connect the button to the reselect_points method
        self.reselect_points_button.clicked.connect(self.reselect_points)
        # Add the button to the layout
        self.layout.addWidget(self.reselect_points_button)
        # Initially hide the button
        self.reselect_points_button.hide()

        #####################################################
        # Horizontal Axis Selection Section
        #####################################################

        # Create a vertical layout for the horizontal axis selection
        horizontal_axis_layout = QVBoxLayout()

        # Label for horizontal axis selection
        self.horizontal_axis_label = QLabel("Horizontal Axis Selection Left to Right") # Create a label for the horizontal axis selection
        self.horizontal_axis_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;") # Set the font size and weight for the label
        horizontal_axis_layout.addWidget(self.horizontal_axis_label) # Add the label to the layout
        # Hide the horizontal axis label
        self.horizontal_axis_label.hide()

        # Horizontal axis buttons layout
        horizontal_axis_button_layout = QHBoxLayout()

        # Create a button to select the x-axis from negative to positive left to right
        self.negative_to_positive_x_button = QPushButton("-x 0 +x") 
        self.negative_to_positive_x_button.setEnabled(False)
        self.negative_to_positive_x_button.clicked.connect(self.negative_to_positive_x)
        horizontal_axis_button_layout.addWidget(self.negative_to_positive_x_button)
        self.negative_to_positive_x_button.setVisible(False)

        # Create a button to select the x-axis from positive to negative right to left
        self.positive_to_negative_x_button = QPushButton("x+ 0 -x")
        self.positive_to_negative_x_button.setEnabled(False)
        self.positive_to_negative_x_button.clicked.connect(self.positive_to_negative_x)
        horizontal_axis_button_layout.addWidget(self.positive_to_negative_x_button)
        self.positive_to_negative_x_button.setVisible(False)

        # Create a button to select the y-axis from negative to positive top to bottom
        self.negative_to_positive_y_button = QPushButton("-y 0 +y")
        self.negative_to_positive_y_button.setEnabled(False)
        self.negative_to_positive_y_button.clicked.connect(self.negative_to_positive_y)
        horizontal_axis_button_layout.addWidget(self.negative_to_positive_y_button)
        self.negative_to_positive_y_button.setVisible(False)

        # Create a button to select the y-axis from positive to negative bottom to top
        self.positive_to_negative_y_button = QPushButton("y+ 0 -y")
        self.positive_to_negative_y_button.setEnabled(False)
        self.positive_to_negative_y_button.clicked.connect(self.positive_to_negative_y)
        horizontal_axis_button_layout.addWidget(self.positive_to_negative_y_button)
        self.positive_to_negative_y_button.setVisible(False)

        # Add horizontal axis buttons layout to the main horizontal axis layout
        horizontal_axis_layout.addLayout(horizontal_axis_button_layout)
        self.layout.addLayout(horizontal_axis_layout)

        #####################################################
        # Vertical Axis Selection Section
        #####################################################

        # Create a vertical layout for the vertical axis selection
        vertical_axis_layout = QVBoxLayout()

        # Label for vertical axis selection
        self.vertical_axis_label = QLabel("Vertical Axis Selection Right Top to Bottom") # Create a label for the vertical axis selection
        self.vertical_axis_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;") # Set the font size and weight for the label
        vertical_axis_layout.addWidget(self.vertical_axis_label) # Add the label to the layout
        self.vertical_axis_label.hide() # Hide the vertical axis label
        

        # Vertical axis buttons layout
        vertical_axis_button_layout = QHBoxLayout()

        # Create a button to select the x-axis from negative to positive left to right
        self.negative_to_positive_x_button_vertical = QPushButton("-x 0 +x")
        self.negative_to_positive_x_button_vertical.setEnabled(False)
        self.negative_to_positive_x_button_vertical.clicked.connect(self.negative_to_positive_x_vertical)
        vertical_axis_button_layout.addWidget(self.negative_to_positive_x_button_vertical)
        self.negative_to_positive_x_button_vertical.setVisible(False)

        # Create a button to select the x-axis from positive to negative right to left
        self.positive_to_negative_x_button_vertical = QPushButton("x+ 0 -x")
        self.positive_to_negative_x_button_vertical.setEnabled(False)
        self.positive_to_negative_x_button_vertical.clicked.connect(self.positive_to_negative_x_vertical)
        vertical_axis_button_layout.addWidget(self.positive_to_negative_x_button_vertical)
        self.positive_to_negative_x_button_vertical.setVisible(False)

        # Create a button to select the y-axis from negative to positive top to bottom
        self.negative_to_positive_y_button_vertical = QPushButton("-y 0 +y")
        self.negative_to_positive_y_button_vertical.setEnabled(False)
        self.negative_to_positive_y_button_vertical.clicked.connect(self.negative_to_positive_y_vertical)
        vertical_axis_button_layout.addWidget(self.negative_to_positive_y_button_vertical)
        self.negative_to_positive_y_button_vertical.setVisible(False)

        # Create a button to select the y-axis from positive to negative bottom to top
        self.positive_to_negative_y_button_vertical = QPushButton("y+ 0 -y")
        self.positive_to_negative_y_button_vertical.setEnabled(False)
        self.positive_to_negative_y_button_vertical.clicked.connect(self.positive_to_negative_y_vertical)
        vertical_axis_button_layout.addWidget(self.positive_to_negative_y_button_vertical)
        self.positive_to_negative_y_button_vertical.setVisible(False)

        # Add vertical axis buttons layout to the main vertical axis layout
        vertical_axis_layout.addLayout(vertical_axis_button_layout)
        self.layout.addLayout(vertical_axis_layout)

        # Label to display the selected vertical axis
        self.distance_input = QLineEdit() # Create a text input field for the distance
        # Set the placeholder text for the distance input field
        self.distance_input.setPlaceholderText("Enter distance between points in cm (e.g., 10)")
        # Set the font size for the distance input field
        self.distance_input.setStyleSheet("font-size: 20px")
        # Initially disable the distance input field
        self.distance_input.setEnabled(False)  # Enable after selecting two points
        self.distance_input.installEventFilter(self) # Enable Enter key press event (doesn't work)
        # Initially hide the distance input field
        self.layout.addWidget(self.distance_input)
        # Initially hide the distance input field
        self.distance_input.returnPressed.connect(self.handle_enter_pressed)
        # Initially hide the distance input field
        self.distance_input.hide()

        # Image viewer
        # Create an image viewer widget
        self.image_viewer = ImageView()
        # Set the image viewer to track two clicks
        self.image_viewer.track_clicks = 2
        # Add the image viewer to the layout
        self.layout.addWidget(self.image_viewer)

        # Assign the layout to the widget
        self.setLayout(self.layout)

        # Initialize variables

        # Folder and Image Paths
        self.folder_path = None  # Store the selected folder path
        self.image_path = None  # Store the selected image path
        self.axis = None  # Store the selected axis
        self.vertical_axis = None  # Store the selected vertical axis

        # Tracked Clicks
        self.clicked_points = []

        # Connect the point_clicked signal from the ImageView to the point_clicked method
        self.image_viewer.point_clicked.connect(self.handle_point_clicked)


    # Method (handle_enter_pressed)
    # Description:
    # This method handler after the user presses the Enter key in the distance input field.
    # It validates the entered distance, calculates the scaling factor based on the selected distance between points,
    # update the direction label with the distance entered, pixel distance, and scaling factor,
    # Input: self
    # Output: None'

    def handle_enter_pressed(self):
        """Handle pressing Enter in the distance input field."""
        try:
            # Get and validate the entered distance
            distance = float(self.distance_input.text())
            if distance <= 0:
                raise ValueError("Distance must be a positive number.")

            if self.axis is None or self.vertical_axis is None:
                raise ValueError(" missing axis selection")
            
            if (self.vertical_axis == 0 or self.vertical_axis == 1) and (self.axis == 0 or self.axis == 1):
                raise ValueError("Invalid axis selection")
            if (self.vertical_axis == 2 or self.vertical_axis == 3) and (self.axis == 2 or self.axis == 3):
                raise ValueError("Invalid axis selection")
            
            # Calculate pixel distance between the clicked points
            pixel_distance = self.calculations_manager.calculate_pixel_distance(
                self.clicked_points[0][0],
                self.clicked_points[0][1],
                self.clicked_points[1][0],
                self.clicked_points[1][1]
            )

            # Calculate the scaling factor
            scaling_factor = self.scaling_factor = self.calculations_manager.calculate_scaling_factor(
                distance, pixel_distance
            )

            # Update the direction label with the calculated values
            self.direction_label.setText(
                f"Distance entered: {distance} cm\n"
                f"Pixel Distance: {pixel_distance:.2f}\n"
                f"Scaling Factor: {scaling_factor:.6f}"
            )

            # Transition to the next page after a delay
            QTimer.singleShot(2000, lambda: self.next_page(scaling_factor))

        except ValueError as e:
            # Display an error message box with the specific issue
            QMessageBox.warning(self, "Invalid Input", str(e))


    # Method (next_page)
    # Description:
    # This method switches to the next page after a delay of 2 seconds.
    # Input: self
    # Output: None
    def next_page(self, scaling_factor):
        # Transition to the next page (image editing page)
        # pass, scaling_factor, folder_path, image_path, axis
        self.parent.edit_page.set_data(scaling_factor, self.folder_path, self.image_path,self.axis,self.vertical_axis)
        self.parent.stack.setCurrentWidget(self.parent.edit_page)

    #####################################################
    # Vertical Axis Selection Methods
    #####################################################

    # Method (negative_to_positive_x_vertical)
    # Description:
    # This method handles the selection of the x-axis from negative to positive left to right for vertical axis.
    # It updates the direction label with the selected vertical axis and prompts the user to enter the distance in cm.
    # Input: self
    # Output: None
    def negative_to_positive_x_vertical(self):
        self.vertical_axis = 0
        self.direction_label.setText("Selected vertical axis: -x 0 +x , please enter the distance in cm ")
        self.distance_input.setEnabled(True)
        self.distance_input.setVisible(True)
       
     

    # Method (positive_to_negative_x_vertical)
    # Description:
    # This method handles the selection of the x-axis from positive to negative right to left.
    # It updates the direction label with the selected vertical axis and prompts the user to enter the distance in cm.
    # Input: self
    # Output: None

    def positive_to_negative_x_vertical(self):
        self.vertical_axis = 1
        self.direction_label.setText("Selected vertical axis: x+ 0 -x , please enter the distance in cm ")
        self.distance_input.setEnabled(True)
        self.distance_input.setVisible(True)
     

    # Method (negative_to_positive_y_vertical)
    # Description:
    # This method handles the selection of the y-axis from negative to positive top to bottom.
    # It updates the direction label with the selected vertical axis and prompts the user to enter the distance in cm.
    # Input: self
    # Output: None

    def negative_to_positive_y_vertical(self):
        self.vertical_axis  = 2
        self.direction_label.setText("Selected vertical axis: -y 0 +y , please enter the distance in cm ")
        self.distance_input.setEnabled(True)
        self.distance_input.setVisible(True)
    

    # Method (positive_to_negative_y_vertical)
    # Description:
    # This method handles the selection of the y-axis from positive to negative bottom to top.
    # It updates the direction label with the selected vertical axis and prompts the user to enter the distance in cm.
    # Input: self
    # Output: None
        
    def positive_to_negative_y_vertical(self):
        self.vertical_axis = 3
        self.direction_label.setText("Selected vertical axis: y+ 0 -y , please enter the distance in cm ")
        self.distance_input.setEnabled(True)
        self.distance_input.setVisible(True)

    #####################################################
    # Horizontal Axis Selection Methods
    #####################################################
       

    # Method (negative_to_positive_x)
    # Description:
    # This method handles the selection of the x-axis from negative to positive left to right.
    # It updates the direction label with the selected horizontal axis and prompts the user to enter the distance in cm.
    # Input: self
    # Output: None
    def negative_to_positive_x(self):
        self.axis = 0
        self.direction_label.setText("Selected horizontal : -x 0 +x , please enter the distance in cm ")
        self.distance_input.setEnabled(True)
        self.distance_input.setVisible(True)

    # Method (positive_to_negative_x)
    # Description:
    # This method handles the selection of the x-axis from positive to negative right to left.
    # It updates the direction label with the selected vertical axis and prompts the user to enter the distance in cm.
    # Input: self
    # Output: None

    def positive_to_negative_x(self):
        self.axis = 1
        self.direction_label.setText("Selected horizontal  axis: x+ 0 -x , please enter the distance in cm ")
        self.distance_input.setEnabled(True)
        self.distance_input.setVisible(True)

    # Method (negative_to_positive_y)
    # Description:
    # This method handles the selection of the y-axis from negative to positive top to bottom.
    # It updates the direction label with the selected vertical axis and prompts the user to enter the distance in cm.
    # Input: self
    # Output: None

    def negative_to_positive_y(self):
        self.axis = 2
        self.direction_label.setText("Selected horizontal  axis: -y 0 +y , please enter the distance in cm ")
        self.distance_input.setEnabled(True)
        self.distance_input.setVisible(True)
        

    # Method (positive_to_negative_y)
    # Description:
    # This method handles the selection of the y-axis from positive to negative bottom to top.
    # It updates the direction label with the selected vertical axis and prompts the user to enter the distance in cm.
    # Input: self
    # Output: None
        
    def positive_to_negative_y(self):
        self.axis = 3
        self.direction_label.setText("Selected horizontal  axis: y+ 0 -y , please enter the distance in cm ")
        self.distance_input.setEnabled(True)
        self.distance_input.setVisible(True)
       
    # Method (reselect_points)
    # Description:
    # This method allows the user to reselect the two points in the image to set the distance.
    # It clears the clicked points list, resets the image viewer, and prompts the user to select new points.
    # Input: self
    # Output: None

    def reselect_points(self):
        self.clicked_points = [] # Clear the clicked points
        self.reselect_points_button.setEnabled(False) # Disable the button
        self.image_viewer.click_list = [] # Clear the clicked points
        self.direction_label.setText("Please select new two points to set the distance")
        self.image_viewer.load_image(self.image_path) # Reload the image
        self.hide_vertical_axis_buttons() # Hide the vertical axis buttons

    # Method (enable_vertical_axis_buttons)
    # Description:
    # This method enables and displays the vertical axis selection buttons on the page.
    # Input: self
    # Output: None

    def enable_vertical_axis_buttons(self):
        self.vertical_axis_label.setVisible(True)
        self.horizontal_axis_label.setVisible(True)
        self.negative_to_positive_x_button.setEnabled(True)
        self.positive_to_negative_x_button.setEnabled(True)
        self.negative_to_positive_y_button.setEnabled(True)
        self.positive_to_negative_y_button.setEnabled(True)
        self.negative_to_positive_x_button.setVisible(True)
        self.positive_to_negative_x_button.setVisible(True)
        self.negative_to_positive_y_button.setVisible(True)
        self.positive_to_negative_y_button.setVisible(True)
        
        self.negative_to_positive_x_button_vertical.setEnabled(True)
        self.positive_to_negative_x_button_vertical.setEnabled(True)
        self.negative_to_positive_y_button_vertical.setEnabled(True)
        self.positive_to_negative_y_button_vertical.setEnabled(True)
        self.negative_to_positive_x_button_vertical.setVisible(True)
        self.positive_to_negative_x_button_vertical.setVisible(True)
        self.negative_to_positive_y_button_vertical.setVisible(True)
        self.positive_to_negative_y_button_vertical.setVisible(True)

    # Method (hide_vertical_axis_buttons)
    # Description:
    # This method hides and disables the vertical axis selection buttons on the page.
    # The distance input field is also hidden and disabled.
    # Input: self
    # Output: None

    def hide_vertical_axis_buttons(self):
        self.distance_input.setEnabled(False)
        self.distance_input.setVisible(False)
        self.horizontal_axis_label.setVisible(False)
        self.vertical_axis_label.setVisible(False)
        self.negative_to_positive_x_button.setEnabled(False)
        self.positive_to_negative_x_button.setEnabled(False)
        self.negative_to_positive_y_button.setEnabled(False)
        self.positive_to_negative_y_button.setEnabled(False)
        self.negative_to_positive_x_button.setVisible(False)
        self.positive_to_negative_x_button.setVisible(False)
        self.negative_to_positive_y_button.setVisible(False)
        self.positive_to_negative_y_button.setVisible(False)
        self.negative_to_positive_x_button_vertical.setEnabled(False)
        self.positive_to_negative_x_button_vertical.setEnabled(False)
        self.negative_to_positive_y_button_vertical.setEnabled(False)
        self.positive_to_negative_y_button_vertical.setEnabled(False)
        self.negative_to_positive_x_button_vertical.setVisible(False)
        self.positive_to_negative_x_button_vertical.setVisible(False)
        self.negative_to_positive_y_button_vertical.setVisible(False)
        self.positive_to_negative_y_button_vertical.setVisible(False)

    # Method (handle_point_clicked)
    # Description:
    # This method handles the clicked points on the image viewer.
    # It checks if the clicked point is too close to an already clicked point and displays a warning message.
    # If two points are selected, it enables the next steps and prompts the user to select the vertical axis.
    # Input: self, x, y (coordinates of the clicked point)
    # Output: None

    def handle_point_clicked(self, x, y):
        # Check if the clicked point is too close to an already clicked point
        for point in self.clicked_points:
            # If the distance between the clicked point and an already clicked point is less than 10 pixels
            if abs(point[0] - x) < 1 and abs(point[1] - y) < 1: 
                QMessageBox.warning(self, "Invalid Selection", "You cannot select the same spot or too close to it.")
                self.reselect_points() # Reselect the points
                return
            
        # Append the clicked point to the clicked points list

        if (x, y) not in self.clicked_points:
            self.clicked_points.append((x, y))

        # If two points are selected, enable the next steps
        # and prompt the user to select the vertical axis
        if len(self.clicked_points) == 2: 
            self.reselect_points_button.setVisible(True) # Show the reselect points button
            self.reselect_points_button.setEnabled(True) # Enable the reselect points button
            self.direction_label.setText("Please select vertical axis!")
            self.enable_vertical_axis_buttons() # Enable the vertical axis buttons
            
    # Method (select_folder)
    # Description:
    # This method opens a dialog to select a folder containing images.
    # It updates the folder path label and enables the select image button.
    # Input: self
    # Output: None

    def select_folder(self):
        """Open a dialog to select a folder."""
        self.hide_vertical_axis_buttons() # Hide the vertical axis buttons

        # Open a dialog to select a folder
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.folder_path = folder_path # Store the selected folder path
            self.folder_label.setText(f"Selected Folder: {folder_path}")# Display the selected folder path
            self.select_image_button.setEnabled(True)# Enable the select image button
            self.select_image_button.setVisible(True)#  Show the select image button
            self.select_image() # Call the select_image method

    # Method (select_image)
    # Description:
    # This method opens a dialog to select an image from the selected folder.
    # It loads the selected image in the image viewer and prompts the user to select two points to set the distance.
    # Input: self
    # Output: None
    def select_image(self):
        
            self.hide_vertical_axis_buttons() # Hide the vertical axis buttons
            self.image_viewer.click_list = [] # Clear the clicked points
            self.clicked_points = [] # Clear the clicked points
            """Open a dialog to select an image from the selected folder."""
            if not self.folder_path:
                return
            # Open a dialog to select an image from the selected folder
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            image_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Image",
                self.folder_path,
                "Images (*.png *.jpg *.jpeg *.bmp)",
                options=options
            )
            # If an image is selected, load it in the image viewer
            if image_path:
                self.image_path = image_path # Store the selected image path
                self.image_viewer.load_image(image_path) # Load the selected image in the image viewer
                self.direction_label.setText("Please select two points to set the distance") # Prompt the user to select two points
                self.select_folder_button.setText("Reselect Folder")# Change the text of the select folder button




        


