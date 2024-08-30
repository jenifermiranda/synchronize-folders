import os

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import shutil
import logging
import sys
import threading
import time


logging.basicConfig(
    filename="operations.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def read_files(folder):

    files_info = []

    for root, dir, files in os.walk(folder):
        for file in files:
            full_path_file = os.path.join(root, file)

            name_file = os.path.basename(file)

            size_file = os.path.getsize(full_path_file)

            modify_date_file = os.path.getmtime(full_path_file)

            info = {
                "name_file": name_file,
                "size": size_file,
                "modify_date": modify_date_file,
            }

            files_info.append(info)

    return files_info


def delete_files(file_path):
    os.remove(file_path)


def copy_files(file_path, destination_folder):
    shutil.copy2(file_path, destination_folder)


def compare_files(source, replica):
    source_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), source)
    replica_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), replica)

    source_files_info = read_files(source_folder)

    replica_files_info = read_files(replica_folder)

    delete_files_list = []
    copy_files_list = []
    create_files_list = []

    source_file_names = [s_file["name_file"] for s_file in source_files_info]

    for s_file in source_files_info:
        found = False
        for r_file in replica_files_info:
            if s_file["name_file"] == r_file["name_file"]:
                found = True
                if s_file["size"] != r_file["size"]:
                    delete_files_list.append(
                        os.path.join(replica_folder, r_file["name_file"])
                    )
                    copy_files_list.append(
                        os.path.join(source_folder, s_file["name_file"])
                    )

        if not found:
            create_files_list.append(os.path.join(source_folder, s_file["name_file"]))

    for r_file in replica_files_info:
        if r_file["name_file"] not in source_file_names:
            delete_files_list.append(os.path.join(replica_folder, r_file["name_file"]))

    log_to_console = print(
        f"Files created: {create_files_list}\nFiles updated: {copy_files_list}\nFiles removed: {delete_files_list}"
    )

    logging.info("Files created: %s", create_files_list)
    logging.info("Files updated: %s", copy_files_list)
    logging.info("Files removed: %s", delete_files_list)

    for file in delete_files_list:
        delete_files(file)

    for file in copy_files_list:
        copy_files(file, replica_folder)

    for file in create_files_list:
        copy_files(file, replica_folder)

    return log_to_console


def run_threaded(compare_files_func, source, replica):
    compare_files_thread = threading.Thread(
        target=compare_files_func, args=(source, replica)
    )
    compare_files_thread.start()


if __name__ == "__main__":
    source = sys.argv[2]
    replica = sys.argv[3]
    while True:
        run_threaded(compare_files, source, replica)
        time.sleep(60)
