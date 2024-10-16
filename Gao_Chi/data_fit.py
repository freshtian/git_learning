import os
from fitparse import FitFile
from fitparse import FitParseError, FitFile


def remove_bin_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.bin'):
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)
            print(f"Removed: {file_path}")


def parse_fit_and_save_as_txt(fit_folder, txt_folder):
    for filename in os.listdir(fit_folder):
        if filename.endswith('.fit'):
            fit_file_path = os.path.join(fit_folder, filename)
            txt_file_path = os.path.join(txt_folder, filename.replace('.fit', '.txt'))

            try:

                fitfile = FitFile(fit_file_path)

                with open(txt_file_path, 'w') as txt_file:

                    for msg in fitfile.get_messages():

                        txt_file.write(f"Message Name: {msg.name}\n")

                        for field in msg.fields:
                            txt_file.write(f"  {field.name}: {field.value} (units: {field.units})\n")

                        txt_file.write("----------------------------\n")

                print(f"Data successfully saved to {txt_file_path}")

            except Exception as e:
                print(f"Error parsing FIT file {fit_file_path}: {e}")


def twt(fit_folder, txt_folder):
    for filename in os.listdir(fit_folder):
        if filename.endswith('.fit'):
            fit_file_path = os.path.join(fit_folder, filename)
            txt_file_path = os.path.join(txt_folder, filename.replace('.fit', '.txt'))

            try:
                fitfile = FitFile(fit_file_path)
                with open(txt_file_path, 'w') as txt_file:

                    for msg in fitfile.get_messages():
                        print(msg.fields)
                        txt_file.write(f"{msg.fields}")

                        # for field in msg.fields:
                        #     txt_file.write(f"  {field.name}: {field.value} (units: {field.units})\n")

                        txt_file.write("----------------------------\n")

                print(f"Data successfully saved to {txt_file_path}")
            except Exception as e:
                print(f"Error parsing FIT file {fit_file_path}: {e}")


if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))

    # 删除所有 .bin 文件
    remove_bin_files(directory)

    # 解析所有 .fit 文件，另存为 .txt 文件
    twt(directory, directory)
