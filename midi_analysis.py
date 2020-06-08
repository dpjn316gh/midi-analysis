from re import search, findall

from converter import get_absolute_path_for_file, text_files_folder_path

standard_duration = 480
analysis_folder_path = 'analysis'

exp_pitch = 'pitch=(\d+) '
exp_vol = 'vol=(\d+)'
exp_time = 'Time=(\d+) '
exp_division = 'division=(\d+)'
exp_signature = 'signature=(\d+)\/(\d+)'


def get_notes(text_file_name: str) -> list:
    note = []
    with open(text_file_name, mode='r') as fhandler:

        # div = 1440  # ticks for 3/8 bar
        # div = 1920  # ticks for 4/4 bar

        for i in fhandler:

            if 'division' in i:
                if search(exp_division, i):
                    division = int(search(exp_division, i).groups()[0])
                    if standard_duration != division:
                        print(f"WARNING Division: {division}")

            if 'signature' in i:
                if search(exp_signature, i):
                    numerator, denominator = search(exp_signature, i).groups()
                    div = int(division) // int(standard_duration) * int(numerator) * standard_duration
                    print(div)

            if 'Note on' in i:
                if search(exp_pitch, i) and search(exp_vol, i) and search(exp_time, i):
                    n = int(findall(exp_pitch, i)[0])
                    v = int(findall(exp_vol, i)[0])
                    start = int(findall(exp_time, i)[0])
                    note.append(
                        [n, v, -start, False, start, int(start / div), int(int((start % div) / standard_duration))])

            if 'Note off' in i:
                if search(exp_pitch, i) and search(exp_vol, i) and search(exp_time, i):
                    n = int(findall(exp_pitch, i)[0])
                    v = int(findall(exp_vol, i)[0])
                    end = int(findall(exp_time, i)[0])
                    res = [item for item in note if item[0] == n and item[3] == False]
                    if len(res) > 1:
                        print('error')
                        continue
                    res[0][2] += end
                    res[0][3] = True
    return note


def generate_file_a(notes: list, analysis_a_file: str):
    with open(analysis_a_file, 'w') as fhandler_output:
        last_bar = 0

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
    print(notes)
    analysis_file_absolute_path = get_absolute_path_for_file(text_file, analysis_folder_path, 'txt')
    generate_file_a(notes, analysis_file_absolute_path)
