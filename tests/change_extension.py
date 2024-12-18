import os

def rename():
    print("Starting file operation...")
    folder_path = os.path.join(os.getcwd(), "examples")
    files = os.listdir(folder_path)
    try:
        for index, file in enumerate(files):
            # Construct the full path for each file
            old_file_path = os.path.join(folder_path, file)
            
            # Construct the new file name
            file_name = f"main_{index}.flint"
            new_file_path = os.path.join(folder_path, file_name)
            
            os.rename(old_file_path, new_file_path)
            print(f"{file} -> {file_name}")
        print("File operation successful :)")
    except Exception as error:
        print(error)
    
    
if __name__ == '__main__':
    rename()


