3. Adjust the configurations in `app_config.json` as per your system setup:
- Set the directory path to your class photos.
- Specify the path to the Excel file for attendance logging.

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

## Jupyter Notebook
- **`face_verification.ipynb`**: This notebook contains the code for the face verification model using triplet loss. To run the notebook:
1. Open the notebook in Jupyter or another compatible environment.
2. Follow the instructions within the notebook to train or test the model.

## Contributions
We welcome contributions from the community. If you have suggestions or improvements, please fork this repository and submit a pull request.

