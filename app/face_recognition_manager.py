import pandas as pd
import os
from datetime import date
import cv2
import face_recognition
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

class FaceRecognitionManager:
    def __init__(self, directory_path, anchor_image_path, file_path):
        # Initialize with the paths to the directory containing images, the anchor image, and the output file path.
        self.directory_path = directory_path
        self.anchor_image_path = anchor_image_path
        self.file_path = file_path

    def crop_faces(self):
        """Crops faces from the anchor image using face_recognition library."""
        anchor_image = face_recognition.load_image_file(self.anchor_image_path)  # Load the image file
        face_locations = face_recognition.face_locations(anchor_image)  # Find all face locations in the image
        # Return cropped images of each face found
        return [anchor_image[top:bottom, left:right] for top, right, bottom, left in face_locations]

    def load_known_faces(self):
        """Loads and encodes faces from images in the directory, caching the encodings to optimize performance."""
        known_faces = []
        for filename in os.listdir(self.directory_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(self.directory_path, filename)
                encoding = self.get_face_encoding(image_path)
                if encoding:
                    name = filename.replace("_", " ")[:filename.rindex(".")].strip()
                    known_faces.append((name, encoding))
        return known_faces

    @lru_cache(maxsize=None)
    def get_face_encoding(self, image_path):
        """Generates encoding for a single face in an image file, with results cached to avoid redundant processing."""
        image = cv2.imread(image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert the image from BGR to RGB
        try:
            encoding = face_recognition.face_encodings(rgb_image)[0]
            return encoding
        except IndexError:
            return None  # Return None if no faces are found

    def encode_and_compare(self, face):
        """Encodes a cropped face and compares it against all known faces to find a match."""
        rgb_face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)  # Convert to RGB
        face_encodings = face_recognition.face_encodings(rgb_face)
        if face_encodings:
            known_faces = self.load_known_faces()
            matches = face_recognition.compare_faces([encoding for _, encoding in known_faces], face_encodings[0])
            if True in matches:
                matched_index = matches.index(True)
                matched_name = known_faces[matched_index][0]
                return matched_name
        return None

    def compare_faces(self, cropped_faces):
        """Uses multiple threads to compare each cropped face with known faces, improving efficiency with parallel processing."""
        results = {name: '✗' for name, _ in self.load_known_faces()}  # Initialize results with '✗' for all known faces

        with ThreadPoolExecutor() as executor:
            matched_results = executor.map(self.encode_and_compare, cropped_faces)  # Process comparison in parallel

        for matched_name in matched_results:
            if matched_name:
                results[matched_name] = '✓'  # Mark as '✓' if a match was found

        return results

    def update_dataframe(self, results, df):
        """Updates the DataFrame with recognition results and saves it to Excel with formatting."""
        current_date = date.today().strftime(r"%Y-%m-%d")
        
        if current_date not in df.columns:
            df[current_date] = False  # Add new column for today if it doesn't exist

        for person in df.index:
            df.at[person, current_date] = results.get(person, '✗')  # Update results for each person
        
        # Save the updated DataFrame to an Excel file with formatting adjustments
        with pd.ExcelWriter(self.file_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1')

            # Adjust column widths based on content length
            for column in df:
                column_width = max(df[column].astype(str).map(len).max(), len(column))
                col_idx = df.columns.get_loc(column)
                writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_width + 1)  # Slightly wider for aesthetics

        return df
