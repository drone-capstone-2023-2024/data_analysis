import tkinter
from PIL import Image, ImageTk

from dataset_extractor import DroneDatasetExtractor


class DataClassifier:
    drones = []
    root = None

    def __init__(self, drones):
        self.drones = drones
        self.initGui()

    def initGui(self):
        self.root = tkinter.Tk()
        self.root.title('Drone Classifier')

        # Load and display an image
        image = tkinter.Image.open(self.drones[0]['picture'])
        photo = ImageTk.PhotoImage(image)

        image_label = tkinter.Label(self.root, image=photo)
        image_label.pack()

        # Create a text field
        text_label = tkinter.Label(self.root, text="Enter text:")
        text_label.pack()

        text_entry = tkinter.Entry(self.root)
        text_entry.pack()

        submit_button = tkinter.Button(self.root, text="Submit", command=self.classify)
        submit_button.pack()

        self.root.mainloop()

    def classify(self):
        for drone in self.drones:
            drone['type'] = 'test'


if __name__ == "__main__":
    datasetExtractor = DroneDatasetExtractor()

    classifier = DataClassifier(datasetExtractor.extract_details())
