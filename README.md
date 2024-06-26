# Face Verification System for Teacher Attendance

## Introduction
This application, named "Facial Recognition Attendance System", automates student attendance management for teachers using cutting-edge facial recognition technology. The system identifies students from class photos and updates attendance records in an Excel file. This application offers a modern, efficient, and cost-effective solution for schools and teachers.

## Features
- **Automated Attendance Management**: Streamlines attendance recording by recognizing students' faces.
- **Triplet Loss Model**: Enhances the accuracy and reliability of face recognition.
- **Excel Integration**: Automatically updates attendance records in an Excel spreadsheet.
- **User-Friendly Interface**: Easy-to-use interface for daily operations.

## Technologies Used
- Python 3.11
- OpenCV for image processing
- tkinter for GUI

## Setup and Installation
1. Clone the repository:

2. Install the required libraries:

3. Adjust the configurations in `app_config.json` as per your system setup:
- Set the directory path to your class photos.
- Specify the path to the Excel file for attendance logging.

## Dataset
The project utilizes the Face Recognition Dataset available on Kaggle, which can be accessed at [this link](https://www.kaggle.com/datasets/stoicstatic/face-recognition-dataset). This dataset provides a diverse set of face images used to train the face verification model.

## Usage Instructions
1. On first launch, set up your class by entering a unique class identifier.
2. Upload a reference image of the class. This can be a new image or an existing one.
3. The application will recognize faces from the reference image and compare them against stored photos.
4. Attendance results will be displayed and updated in the designated Excel file.
5. Ensure all data is correct and there are no omissions in the attendance list.

## How It Works
1. **Capturing the Image**: The teacher uploads a class photo.
2. **Processing the Image**: The system uses a triplet loss model to process the image and identify faces.
3. **Comparing and Logging Attendance**: Faces are compared with stored images, and attendance is logged in an Excel file.

## Contributions
We welcome contributions from the community. If you have suggestions or improvements, please fork this repository and submit a pull request.

