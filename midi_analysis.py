import re

from converter import get_absolute_path_for_file, text_files_folder_path

exp_pitch = 'pitch=(\d+) '
exp_vol = 'vol=(\d+)'
exp_time = 'Time=(\d+) '
standard_duration = 480
analysis_folder_path = 'analysis'


def get_notes(text_file_name: str) -> list:
    note = []
    with open(text_file_name, mode='r') as fhandler:

        # div = 1440  # ticks for 3/8 bar
        div = 1920  # ticks for 4/4 bar

        for i in fhandler:
            if 'Note on' in i:
                if re.search(exp_pitch, i) and re.search(exp_vol, i) and re.search(exp_time, i):
                    n = int(re.findall(exp_pitch, i)[0])
                    v = int(re.findall(exp_vol, i)[0])
                    start = int(re.findall(exp_time, i)[0])
                    note.append(
                        [n, v, -start, False, start, int(start / div), int(int((start % div) / standard_duration))])

            if 'Note off' in i:
                if re.search(exp_pitch, i) and re.search(exp_vol, i) and re.search(exp_time, i):
                    n = int(re.findall(exp_pitch, i)[0])
                    v = int(re.findall(exp_vol, i)[0])
                    end = int(re.findall(exp_time, i)[0])
                    res = [item for item in note if item[0] == n and item[3] == False]
                    if len(res) > 1:
                        print('error')
                        continue
                    res[0][2] += end
                    res[0][3] = True
    return note


def generate_file_a(notes: list, analysis_a_file: str):
    with open(analysis_a_file, 'w') as fhandler_output:
        bar = 0
        last_bar = 0

        sub_bar = 0
        last_sub_bar = 0

        for n in notes:
            bar = n[5]
            sub_bar = n[6]

            if last_bar != bar:
                fhandler_output.write('------------- {0} -------------\n'.format(bar))
                last_bar = bar

            if last_sub_bar != sub_bar:
                fhandler_output.write('--- {0} ---\n'.format(sub_bar))
                last_sub_bar = sub_bar

            fhandler_output.write('N={0} D={2} V={1}\n'.format(n[0], n[1], n[2]))


def analysis_a(text_file: str):
    text_file_absolute_path = get_absolute_path_for_file(text_file, text_files_folder_path, 'txt')
    notes = get_notes(text_file_absolute_path)
    analysis_file_absolute_path = get_absolute_path_for_file(text_file, analysis_folder_path, 'txt')
    generate_file_a(notes, analysis_file_absolute_path)


file = 'hannon.txt'
analysis_a(file)
