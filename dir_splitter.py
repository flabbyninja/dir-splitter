from pathlib import Path
from os.path import join
from os import mkdir, stat, path
from shutil import move

# TODO: make optional whether we put archive in subdirs, or archive at top level directory

DATA_DIRECTORY = r'test\resources'

PROCESSED_COMPRESSED_EXT = '.jpg'
RAW_EXT = '.dng'
ARCHIVE_SUBDIR = 'archive'
SKIP_ARCHIVE_DIR = True


def get_filtered_dict(full_file_dict, extension):
    filtered_values = {
        join(full_file_dict[file].parent, full_file_dict[file].stem):
            full_file_dict[file] for file in list(full_file_dict.keys())
        if (file.endswith(extension))
    }
    return filtered_values

# Return total file size in bytes from a list
def calc_size(file_list):
    total_size = 0

    for f in file_list:
        total_size += f.stat().st_size

    return total_size

def delete_or_archive(file_list, delete_flag=0):
    for f in file_list:
        if delete_flag:
            # May implement in future - better to archive for now till sure
            print('Delete planned for', f)
        else:
            archive_directory = join(f.parent, ARCHIVE_SUBDIR)
            print('Move planned for', f, 'to', join(archive_directory, f.name))
            print('Checking archive directory exists')
            try:
                stat(archive_directory)
                print('Directory exists, so will use')
            except FileNotFoundError:
                print('Directory does not exist so will create')
                # mkdir(archive_directory)

                # move(join(f.parent, f.name), archive_directory)

def create_files_list(root_path, skip_archive):
    root_path_with_subdirs = root_path.glob('**/*')
    files_list = root_path_with_subdirs

    if skip_archive == True:
        files_list = [file for file in root_path_with_subdirs
                      if not file.parent.name == ARCHIVE_SUBDIR]

    return files_list


def main():
    root_path = Path(DATA_DIRECTORY)
    print('Root path set to: ', root_path)

    # Get all underlying files in root directory, excluding archive subdirs
    files_to_process = create_files_list(root_path, SKIP_ARCHIVE_DIR)

    # Create dictionary of full file paths against file objects (excluding dirs)
    full_file_dict = {join(file.parent.name, file.name): file for file in files_to_process if file.is_file()}
    print(len(full_file_dict.keys()), 'total files found: ', [p.name for p in full_file_dict.values()])

    # Filter to create dicts mapping full file path (excluding extension) to Path object, using extension
    jpeg_dict = get_filtered_dict(full_file_dict, PROCESSED_COMPRESSED_EXT)
    print(len(jpeg_dict.keys()), PROCESSED_COMPRESSED_EXT, 'files found: ')  # , [p.name for p in jpeg_dict.values()])
    dng_dict = get_filtered_dict(full_file_dict, RAW_EXT)
    print(len(dng_dict.keys()), RAW_EXT, 'files found: ')  # , [p.name for p in dng_dict.values()])

    # files to process are those dng's with the same stem in both jpeg and dng lists from full file list, construct new list of the files to be processed
    files_to_process = [dng_dict[file] for file in list(jpeg_dict.keys()) if file in dng_dict]
    print(len(files_to_process), 'files to process: ')  # , [p.name for p in files_to_process])

    # calculate size of files to be processed
    print("Total size to be archived: {:,d} MB".format(int(calc_size(files_to_process) / 1024 / 1024)))

    # delete_or_archive(files_to_process)


if __name__ == '__main__':
    main()
