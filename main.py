import create_image as ci
import extract_data as ed
import os.path as op

if __name__ == "__main__":
    print("[1]: Hide data in image")
    print("[2]: Extract data from image")
    input_choice = input("$ ")
    while (input_choice not in ["1", "2"]):
        print("\nInvalid input.")
        print("[1]: Hide data in image")
        print("[2]: Extract data from image")
        input_choice = input("$ ")
    if input_choice == "1":
        image_input_path = input("\nEnter path to image: ")
        while (op.splitext(image_input_path)[1]!= ".png" or not op.exists(image_input_path)):
            print("\nPlease enter a path for existing PNG file.")
            image_input_path = input("Enter path to image: ")
        data_input_path = input("\nEnter path to data file: ")
        while (op.splitext(data_input_path)[1]!= ".txt" or not op.exists(data_input_path)):
            print("\nPlease enter a path for existing TXT file.")
            data_input_path = input("Enter path to data file: ")
        output_path = input("\nEnter path to output image: ")
        while (op.splitext(output_path)[1]!= ".png"):
            print("\nInvalid file type. Please enter a path for output PNG file.")
            output_path = input("Enter path to output image: ")
        ci.main(image_input_path, data_input_path, output_path)
        print("\nOutput image created at: " + output_path)
    elif input_choice == "2":
        image_input_path = input("\nEnter path to image: ")
        while (op.splitext(image_input_path)[1]!= ".png" or not op.exists(image_input_path)):
            print("\nPlease enter a path for existing PNG file.")
            image_input_path = input("Enter path to image: ")
        output_path = input("\nEnter path to output data file: ")
        while (op.splitext(output_path)[1]!= ".txt"):
            print("\nInvalid file type. Please enter a path for output TXT file.")
            output_path = input("Enter path to output data file: ")
        ed.main(image_input_path, output_path)
        print("\nOutput data file created at: " + output_path)
    