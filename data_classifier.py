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
    specs_label = None
    progress_label = None

    input_map = {}

    def __init__(self, drones):
        self.drones = drones
        self.init_gui()

    def init_gui(self):
        self.def_input_map()

        self.root = tkinter.Tk()
        self.root.title('Drone Classifier')
        self.root.geometry('1920x1080')
        self.root.bind('<KeyPress>', self.key_input_callback)

        # Load and display an image
        self.image_label = tkinter.Label(self.root, width=800, height=500)
        self.image_label.pack()

        # Create drone name label
        self.text_label = tkinter.Label(self.root, font=('Helveticabold', 15), fg='blue', cursor='hand2')
        self.text_label.pack()

        # Create control instruct label
        self.control_label = tkinter.Label(self.root, font=('Helveticabold', 15))
        self.control_label.pack()
        self.setup_control_instruct_label()

        # Create specs label
        self.specs_label = tkinter.Label(self.root, font=('Helveticabold', 15))
        self.specs_label.pack()

        # Create control instruct label
        self.progress_label = tkinter.Label(self.root, font=('Helveticabold', 15))
        self.progress_label.pack()

        self.update_ui()

        self.root.mainloop()

    def classify(self, class_id):
        if class_id >= len(classification_map):
            print('invalid class id passed to classify!!!')
            return
        self.drones[self.current_drone_index]['type'] = classification_map[class_id]
        self.current_drone_index += 1

        self.update_ui()

    def jump_to_drone(self, index):
        self.current_drone_index = index

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
            self.update_progress_label()
            self.update_specs_label()

    def setup_platform_name_label(self):
        drone_name = ''

        if 'type' in self.drones[self.current_drone_index]:
            drone_name += 'Current Type: ' + self.drones[self.current_drone_index]['type'] + '\n'

        drone_name += self.drones[self.current_drone_index]['Platform']

        self.text_label['text'] = drone_name

        # set hyperlink callback to open search for device on Google
        self.text_label.bind("<Button-1>", lambda e: webbrowser.open_new_tab('https://www.google.com/search?q=' +
                                                                             drone_name.replace(' ', '+')))

    def setup_control_instruct_label(self):
        self.control_label['text'] = ''

        for i in range(len(classification_map)):
            self.control_label['text'] += str(i + 1) + ': ' + classification_map[i] + ', '

        self.control_label['text'] = self.control_label['text'].rstrip(', ')

    def update_progress_label(self):
        self.progress_label['text'] = str(self.current_drone_index + 1) + ' / ' + str(len(self.drones))

    def update_specs_label(self):
        self.specs_label['text'] = '\n'

        current_drone = self.drones[self.current_drone_index]

        count = 1
        for spec in current_drone:
            self.specs_label['text'] += spec + ': ' + current_drone[spec]
            if count % 2 == 1:
                self.specs_label['text'] += ', '
            else:
                self.specs_label['text'] += '\n'

            count += 1

    def def_input_map(self):
        for i in range(len(classification_map)):
            self.input_map[str(i+1)] = lambda x=i: self.classify(x)

        self.input_map['n'] = lambda: self.jump_to_drone(self.current_drone_index - 1)
        self.input_map['m'] = lambda: self.jump_to_drone(self.current_drone_index + 1)

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
