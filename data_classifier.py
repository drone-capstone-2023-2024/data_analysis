# TODO: make plane name hyperlinks to google, use keyboard for selecting classification and allow going forwards and backwards, max screen

import tkinter
from PIL import Image, ImageTk

from dataset_extractor import DroneDatasetExtractor


class DataClassifier:
    current_drone_index = 0
    drones = []
    root = None

    photo = None  # photo must be defined here to prevent gc from destroying it in func
    image_label = None
    text_label = None
    type_sel_label = None
    submit_button = None


    def __init__(self, drones):
        self.drones = drones
        self.initGui()

    def initGui(self):
        self.root = tkinter.Tk()
        self.root.title('Drone Classifier')

        # Load and display an image
        image = Image.open(self.drones[self.current_drone_index]['picture'])
        self.photo = ImageTk.PhotoImage(image)

        self.image_label = tkinter.Label(self.root, image=self.photo)
        self.image_label.pack()

        # Create a text field
        self.text_label = tkinter.Label(self.root, text=self.create_label_text())
        self.text_label.pack()

        self.type_sel_label = tkinter.Entry(self.root)
        self.type_sel_label.pack()

        self.submit_button = tkinter.Button(self.root, text='Submit', command=self.classify)
        self.submit_button.pack()

        self.root.mainloop()

    def classify(self):
        self.drones[self.current_drone_index]['type'] = self.type_sel_label.get()
        self.current_drone_index += 1

        self.update_ui()

    def update_ui(self):
        if self.current_drone_index >= len(self.drones):
            self.root.quit()
        else:
            image = Image.open(self.drones[self.current_drone_index]['picture'])
            self.photo = ImageTk.PhotoImage(image)
            self.image_label['image'] = self.photo

            self.text_label['text'] = self.create_label_text()

    def create_label_text(self):
        return 'Enter type for ' + self.drones[self.current_drone_index]['Platform'] + ':'


if __name__ == "__main__":
    datasetExtractor = DroneDatasetExtractor()

    classifier = DataClassifier(datasetExtractor.extract_details())

    print(classifier.drones)
