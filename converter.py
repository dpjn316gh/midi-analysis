from os.path import realpath, dirname, join, splitext
from subprocess import Popen, PIPE

midi_files_folder_path = 'midi-files'
text_files_folder_path = 'text'


def execute_mftext_program(midi_file: str) -> str:
    process = Popen(['mftext', f'{midi_file}'], stdout=PIPE)
    return process.communicate()[0]


def get_absolute_path_for_file(file_name: str, folder: str, new_extension: str) -> str:
    absolute_current_directory = dirname(realpath(__file__))
    file_name_with_out_ext, extension = splitext(file_name)
    new_file_name = f"{file_name_with_out_ext}.{new_extension}"
    return join(absolute_current_directory, folder, new_file_name)


def write_file(file_name: str, content: bytes):
    binary_format = bytearray(content)
    with open(file_name, mode='w+b') as writer:
        writer.write(binary_format)


def convert_midi_file_to_text(midi_file: str):
    midi_file_absolute_path = get_absolute_path_for_file(midi_file, midi_files_folder_path, 'mid')
    content = execute_mftext_program(midi_file_absolute_path)
    text_file_absolute_path = get_absolute_path_for_file(midi_file, text_files_folder_path, 'txt')
    write_file(text_file_absolute_path, content)
