
import face_recognition
import os
import shutil
import logging

input_folder = "./input"
output_folder = "./output"

# Load the jpg file into numpy arrays
my_image = face_recognition.load_image_file("my.jpg")


logging.basicConfig(format='%(levelname)s: [%(asctime)s] %(message)s', datefmt='%Y/%m/%d %H:%M:%S', filename='recognition.log', level=logging.INFO)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



for root, dirs, files in os.walk(input_folder):
    files_number = len(files)
    for count, name in enumerate(files, start=1):
        print(f'{round(100*count/files_number,0)}% {count} of {files_number} file: {name} ... ', end="")


        unknown_image = face_recognition.load_image_file(os.path.join(root, name))

        # Get the face encodings for each face in each image file
        # Since there could be more than one face in each image, it returns a list of encodings.
        # But since I know my image only has one face, I only care about the first encoding in each image, so I grab index 0.
        try:
            my_face_encoding = face_recognition.face_encodings(my_image)[0]
            unknown_face_encodings = face_recognition.face_encodings(unknown_image)
            print(f'{len(unknown_face_encodings)} faces ... ', end="")
            if len(unknown_face_encodings) < 1:
                logging.info(f";{name}; No faces in file ")
                print(f"{bcolors.WARNING}No faces in file{bcolors.ENDC}")
                continue
        except:
            logging.info(f";{name}; Unknown Error")
            print(f"{bcolors.WARNING}Unknown error{bcolors.ENDC}")
            

        # results is an array of True/False telling if any of the unknown faces matched my face
        results = face_recognition.compare_faces(my_face_encoding, unknown_face_encodings)
        if True in results:
            shutil.copy2(os.path.join(root, name),os.path.join(output_folder, name))
            logging.info(f";{name}; Your face found")
            print(f'{bcolors.OKGREEN}Your face found !!!{bcolors.ENDC}')
        else:
            logging.info(f";{name}; Not found")
            print("Not found")




