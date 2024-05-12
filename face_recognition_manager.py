import pandas as pd
import os
from datetime import date
import cv2
import face_recognition


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

    def compare_faces(self, cropped_faces):
        """Compares cropped faces to known faces in the directory."""
        known_faces = []
        for filename in os.listdir(self.directory_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(self.directory_path, filename)
                image = cv2.imread(image_path)
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                try:
                    encoding = face_recognition.face_encodings(rgb_image)[0]
                    name = filename.replace("_", " ")[:filename.rindex(".")].strip()
                    known_faces.append((name, encoding))
                except IndexError:
                    continue

        results = {name: False for name, _ in known_faces}
        for face in cropped_faces:
            rgb_face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            try:
                face_encoding = face_recognition.face_encodings(rgb_face)[0]
                matches = face_recognition.compare_faces([encoding for _, encoding in known_faces], face_encoding)
                if True in matches:
                    match_index = matches.index(True)
                    matched_name = known_faces[match_index][0]
                    results[matched_name] = True
            except IndexError:
                continue
        return results

    def update_dataframe(self, results, df):
        """Updates the DataFrame with the recognition results and formats the Excel output."""
        current_date = date.today().strftime(r"%Y-%m-%d")
        
        
        df.columns = pd.to_datetime(df.columns).strftime(r"%Y-%m-%d")
        
        if current_date not in df.columns:
            df[current_date] = False

        for person in df.index:
            df.at[person, current_date] = results.get(person, False)
        
        # המרה של ערכים בוליאניים ל'✓' ו'✗'
        df = df.applymap(lambda x: '✓' if x else '✗')

        # Save DataFrame to Excel with formatting
        with pd.ExcelWriter(self.file_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1')

            # Auto-adjust columns' width
            for column in df:
                column_width = max(df[column].astype(str).map(len).max(), len(column))
                col_idx = df.columns.get_loc(column)
                writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_width + 1)  # add a little extra width

        return df