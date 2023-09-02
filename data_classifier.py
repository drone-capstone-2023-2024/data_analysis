# TODO: make plane name hyperlinks to google, use keyboard for selecting classification and allow going forwards and backwards, max screen

import tkinter
from PIL import Image, ImageTk
import webbrowser

from dataset_extractor import DroneDatasetExtractor

classification_map = ['quadcopter',
                      'plane',
                      'hybrid (tilt rotor)',
                      'hybrid (winged copter)']


class DataClassifier:
    current_drone_index = 0
    drones = []
    root = None

    photo = None  # photo must be defined here to prevent gc from destroying it in func
    image_label = None
    text_label = None
    control_label = None

    input_map = {}

    def __init__(self, drones):
        self.drones = drones
        self.init_gui()

    def init_gui(self):
        self.def_input_map();

        self.root = tkinter.Tk()
        self.root.title('Drone Classifier')
        self.root.geometry('1920x1080')
        self.root.bind('<KeyPress>', self.key_input_callback)

        # Load and display an image
        image = Image.open(self.drones[self.current_drone_index]['picture'])
        image = image.resize((800, 500), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)

        self.image_label = tkinter.Label(self.root, image=self.photo, width=800, height=500)
        self.image_label.pack()

        # Create drone name label
        self.text_label = tkinter.Label(self.root, font=('Helveticabold', 15), fg='blue', cursor='hand2')
        self.text_label.pack()
        self.setup_platform_name_label()

        # Create control instruct label
        self.control_label = tkinter.Label(self.root, font=('Helveticabold', 15))
        self.control_label.pack()
        self.setup_control_instruct_label()

        self.root.mainloop()

    def classify(self, class_id):
        if class_id >= len(classification_map):
            print('invalid class id passed to classify!!!')
            return
        self.drones[self.current_drone_index]['type'] = classification_map[class_id]
        self.current_drone_index += 1

        self.update_ui()

    def update_ui(self):
        if self.current_drone_index >= len(self.drones):
            self.root.quit()
        else:
            image = Image.open(self.drones[self.current_drone_index]['picture'])
            image = image.resize((800, 500), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            self.image_label['image'] = self.photo

            self.setup_platform_name_label()

    def setup_platform_name_label(self):
        drone_name = self.drones[self.current_drone_index]['Platform']

        self.text_label['text'] = drone_name

        # set hyperlink callback to open search for device on Google
        self.text_label.bind("<Button-1>", lambda e: webbrowser.open_new_tab('https://www.google.com/search?q=' +
                                                                             drone_name.replace(' ', '+')))

    def setup_control_instruct_label(self):
        self.control_label['text'] = ''

        for i in range(len(classification_map)):
            self.control_label['text'] += str(i + 1) + ': ' + classification_map[i] + ', '

        self.control_label['text'] = self.control_label['text'].rstrip(', ')

    def def_input_map(self):
        self.input_map = {'1': lambda: self.classify(0),  # cannot use loop here as refs to them will be the same
                          '2': lambda: self.classify(1),
                          '3': lambda: self.classify(2),
                          '4': lambda: self.classify(3)}

    def key_input_callback(self, event):
        key = event.char
        if key in self.input_map:
            self.input_map[key]()


if __name__ == '__main__':
    datasetExtractor = DroneDatasetExtractor()

    classifier = DataClassifier(datasetExtractor.extract_details())

    print(classifier.drones)

    print('\n\nClassified types:')
    for drone in classifier.drones:
        if 'type' in drone:
            print(drone['Platform'] + ': ' + drone['type'])
