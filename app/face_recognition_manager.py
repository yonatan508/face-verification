import pandas as pd
import os
from datetime import date
import cv2
import face_recognition
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

class FaceRecognitionManager:
    def __init__(self, directory_path, anchor_image_path, file_path):
        self.directory_path = directory_path
        self.anchor_image_path = anchor_image_path
        self.file_path = file_path

    def crop_faces(self):
        """Crops faces from the anchor image."""
        anchor_image = face_recognition.load_image_file(self.anchor_image_path)
        face_locations = face_recognition.face_locations(anchor_image)
        return [anchor_image[top:bottom, left:right] for top, right, bottom, left in face_locations]

    def load_known_faces(self):
        """Loads and encodes known faces from a directory, caching the encodings."""
        known_faces = []
        for filename in os.listdir(self.directory_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(self.directory_path, filename)
                encoding = self.get_face_encoding(image_path)
                if encoding is not None:
                    name = filename.replace("_", " ")[:filename.rindex(".")].strip()
                    known_faces.append((name, encoding))
        return known_faces

    @lru_cache(maxsize=None)
    def get_face_encoding(self, image_path):
        """Encodes a face from an image path, with caching to improve performance."""
        image = cv2.imread(image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        try:
            encoding = face_recognition.face_encodings(rgb_image)[0]
            return encoding
        except IndexError:
            return None

    def encode_and_compare(self, face):
        """Helper method to encode a face and compare it against known faces."""
        rgb_face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_face)
        if face_encodings:
            matches = face_recognition.compare_faces([encoding for _, encoding in self.load_known_faces()], face_encodings[0])
            if True in matches:
                matched_index = matches.index(True)
                matched_name = self.load_known_faces()[matched_index][0]
                return matched_name
        return None

    def compare_faces(self, cropped_faces):
        """Compares cropped faces to known faces in the directory using parallel processing."""
        results = {name: '✗' for name, _ in self.load_known_faces()}

        # Use ThreadPoolExecutor to encode and compare faces in parallel
        with ThreadPoolExecutor() as executor:
            matched_results = executor.map(self.encode_and_compare, cropped_faces)

        for matched_name in matched_results:
            if matched_name:
                results[matched_name] = '✓'

        return results

    def update_dataframe(self, results, df):
        """Updates the DataFrame with the recognition results and formats the Excel output."""
        current_date = date.today().strftime(r"%Y-%m-%d")
        
        
        df.columns = pd.to_datetime(df.columns).strftime(r"%Y-%m-%d")
        
        if current_date not in df.columns:
            df[current_date] = False

        for person in df.index:
            df.at[person, current_date] = results.get(person, False)
        

        # Save DataFrame to Excel with formatting
        with pd.ExcelWriter(self.file_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1')

            # Auto-adjust columns' width
            for column in df:
                column_width = max(df[column].astype(str).map(len).max(), len(column))
                col_idx = df.columns.get_loc(column)
                writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_width + 1)  # add a little extra width

        return df
