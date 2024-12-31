############################################################################################
# Project Name: Motor Skill Acquisition Error Management System (San Francisco State University Project 2024) 
# 
# Filename: Image_interface.py
# 
# Authors: Milton Tinoco, Ethan Weldon, Joshua Samson, Michael Cabrera
#
# Last Update: 12/08/2024
#
# File Description:
# This file contains the code for the image interface, which displays images and allows users to select points on them.
# The ImageView class is a custom QGraphicsView that displays images and emits signals when points are clicked on the image.
# 
############################################################################################

# Import necessary libraries

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QPen
from PyQt5.QtCore import Qt, QLineF, pyqtSignal

# Class: ImageView
# Description:
# This class is a custom QGraphicsView that displays images and emits signals when points are clicked on the image.
# The ImageView class inherits from QGraphicsView and displays images in a QGraphicsScene.
# It allows users to click on the image to select points and emits signals with the coordinates of the clicked points.

class ImageView(QGraphicsView):
    point_clicked = pyqtSignal(float, float) # Signal emitted when a point is clicked on the image

    # Constructor
    # Initializes the QGraphicsScene and sets the pen for drawing points on the image.
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self) # Create a QGraphicsScene
        self.setScene(self.scene) # Set the scene for the view

        self.pen = QPen(Qt.red) # Set the pen color to red
        self.pen.setWidth(2) # Set the pen width to 2

        self.scale_factor = 1.1 # Set the scale factor for zooming
        self.image_selected = False # Flag to check if an image is loaded
        self.track_clicks = None # Number of clicks to track
        self.click_list = [] # List to store clicked points

    # Method: draw_point_circle
    # Description:
    # Draw a circle centered at the specified point on the image.
    # Input: x - x-coordinate of the point
    #        y - y-coordinate of the point
    # Output: None
    def draw_point_circle(self, x, y):
        circle_radius = 6  # Set radius of the circle
        # Add an ellipse item to the scene to represent the circle
        ellipse_item =self.scene.addEllipse(
            x - circle_radius, y - circle_radius, 2 * circle_radius, 2 * circle_radius, self.pen
        )
        ellipse_item.setBrush(Qt.green)  # Set the brush color to yellow


    # Method: load_image
    # Description:
    # Load and display the selected image by creating a QGraphicsPixmapItem with the image and adding it to the scene.
    # Input: image_path - path to the image file
    # Output: None

    def load_image(self, image_path):
        """Load and display the selected image."""
        pixmap = QPixmap(image_path).scaled(1600, 1200, Qt.KeepAspectRatio) # Load the image and scale it
        self.scene.clear() # Clear the scene
        self.image_item = QGraphicsPixmapItem(pixmap) # Create a QGraphicsPixmapItem with the image
        self.scene.addItem(self.image_item) # Add the image item to the scene
        self.image_selected = True # Set the flag to indicate that an image is loaded
        self.fitInView(self.image_item, Qt.KeepAspectRatio) # Fit the image to the view

    # Method: mousePressEvent
    # Description:
    # Handle mouse press events on the image view.
    # When the left mouse button is clicked, emit a signal with the coordinates of the clicked point.
    # Draw a cross centered at the clicked position on the image.
    # Limit the number of set by the track_clicks attribute.
    # Input: event - mouse press event
    # Output: None

    def mousePressEvent(self, event):
        # Check if an image is loaded and return if not
        if not self.image_selected:
            return

        # Check if the number of clicks is limited and if the limit is reached then return

        if len(self.click_list) >= self.track_clicks:  # Limit clicks to two points
            return

        # Check if the left mouse button is clicked
        if event.button() == Qt.LeftButton:
            scene_pos = self.mapToScene(event.pos()) # Get the position of the click in the scene
            self.point_clicked.emit(scene_pos.x(), scene_pos.y())  # Emit the clicked point
            self.click_list.append((scene_pos.x(), scene_pos.y()))  # Append the point as a tuple
         

            # Draw a cross centered at the clicked position
            cross_size = 10 # Size of the cross
            # Draw horizontal and vertical lines for the cross
            self.scene.addLine(
                QLineF(scene_pos.x() - cross_size, scene_pos.y(),
                       scene_pos.x() + cross_size, scene_pos.y()),
                self.pen
            )
            # Draw vertical line
            self.scene.addLine(
                QLineF(scene_pos.x(), scene_pos.y() - cross_size,
                       scene_pos.x(), scene_pos.y() + cross_size),
                self.pen
            )

    # Method: wheelEvent
    # Description:
    # Handle wheel events for zooming in and out of the image.
    # Zoom in when the wheel is scrolled up and zoom out when the wheel is scrolled down.
    # Input: event - wheel event
    # Output: None

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale(self.scale_factor, self.scale_factor)
        else:
            self.scale(1 / self.scale_factor, 1 / self.scale_factor)
