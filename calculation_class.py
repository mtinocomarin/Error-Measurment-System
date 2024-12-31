############################################################################################
# Project Name: Motor Skill Acquisition Error Management System (San Francisco State University Project 2024) 
# 
# Filename: calculation_class.py
# 
# Authors: Milton Tinoco, Ethan Weldon, Joshua Samson, Michael Cabrera
#
# Last Update: 12/08/2024
#
# File Description:
# This file contains the code for the calculations manager, which performs calculations related to pixel distances, scaling factors, errors, and real-world coordinates.
# 
############################################################################################

# Import necessary libraries

import numpy as np

# Class: CalculationsManager
# Description:
# This class provides methods to perform calculations related to pixel distances, scaling factors, errors, and real-world coordinates.

class CalculationsManager:
    def __init__(self):
        pass

    def calculate_pixel_distance(self, x1, y1, x2, y2):
        """
        Calculate the pixel distance between two points.
        
        Args:
            x1, y1: Coordinates of the first point.
            x2, y2: Coordinates of the second point.
        
        Returns:
            float: The pixel distance between the two points.
        """
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def calculate_scaling_factor(self, real_world_distance, pixel_distance):
        """
        Calculate the scaling factor given a real-world distance and a pixel distance.
        
        Args:
            real_world_distance (float): The real-world distance.
            pixel_distance (float): The pixel distance.
        
        Returns:
            float: The scaling factor.
        
        Raises:
            ValueError: If pixel_distance is zero to prevent division by zero.
        """
        if pixel_distance == 0:
            raise ValueError("Pixel distance cannot be zero.")
        return real_world_distance / pixel_distance

    def calculate_error(self, x1, y1, x2, y2, scaling_factor):
        """
        Calculate the real-world error measurement between two points.
        
        Args:
            x1, y1: Coordinates of the first point.
            x2, y2: Coordinates of the second point.
            scaling_factor (float): The scaling factor.
        
        Returns:
            float: The real-world error measurement.
        """
        pixel_distance = self.calculate_pixel_distance(x1, y1, x2, y2)
        return pixel_distance * scaling_factor

    def calculate_real_world_coordinates(self, x1, y1, x2, y2, scaling_factor):
        """
        Calculate the real-world x and y values between two points.
        
        Args:
            x1, y1: Coordinates of the first point.
            x2, y2: Coordinates of the second point.
            scaling_factor (float): The scaling factor.
        
        Returns:
            tuple (float, float): The real-world x and y values.
        """
        delta_x = (x2 - x1) * scaling_factor
        delta_y = (y2 - y1) * scaling_factor
        return delta_x, delta_y
