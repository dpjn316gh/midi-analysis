from statistics import mean, mode, median_high, median_low, median, pstdev, pvariance

from converter import get_absolute_path_for_file, text_files_folder_path
from midi_analysis import get_notes, analysis_folder_path

human_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']


def return_note_octave(note_number: int):
    return f"{human_notes[note_number % 12]}_{note_number // 12}"


def return_note(note_number: int):
    return f"{human_notes[note_number % 12]}"


def prepare_data(notes: list)-> list:
    data = []
    for i, n in enumerate(notes):
        data.append((return_note(n[0]), return_note_octave(n[0]),
                     n[0], n[1], n[2], n[4]))
    return data


def analysis(data:list)->list:
    result=[]

    tmp_dic = {}
    for i, n in enumerate(data):

        if n[0] not in tmp_dic.keys():
            tmp_dic[n[0]] = list(n[2:])
        else:
            if n[2] < tmp_dic[n[0]][0]: # saber la nota mas alta (para saber si es la mano derecha o izauierda)
                tmp_dic[n[0]] = tmp_dic[n[0]] - list(n[2:])
            else:
                tmp_dic[n[0]] = list(n[2:]) -  tmp_dic[n[0]]


        if i % 16 == 0 and i > 0:
        #     tmp_dic.clear()
        #     result.append()


def generate_file_for_hanon(notes: list, analysis_a_file: str):
    with open(analysis_a_file, 'w') as fhandler_output:
        data = prepare_data(notes)

        analysis(data)

        for i, n in enumerate(data):
            if i % 16 == 0:
                fhandler_output.write("\n")
            fhandler_output.write('HN={0}, HNO={1} N={2} V={3} D={4} P={5}\n'.format
                                  (n[0], n[1], n[2], n[3], n[4], n[5]))


def statistics(notes: list):
    durations = [e[2] for e in notes]
    velocities = [e[1] for e in notes]
    print("Duration Mean", mean(durations))
    print("Duration Median", median(durations))
    print("Duration Max", median_high(durations))
    print("Duration Min", median_low(durations))
    print("Duration SD", pstdev(durations))
    print("Duration Variance", pvariance(durations))

    print("Velocity Mean", mean(velocities))
    print("Velocity Median", median(velocities))
    print("Velocity Max", max(velocities))
    print("Velocity Min", min(velocities))
    print("Velocity SD", pstdev(velocities))
    print("Velocity Variance", pvariance(velocities))


def hanon_analysis(text_file: str):
    text_file_absolute_path = get_absolute_path_for_file(text_file, text_files_folder_path, 'txt')
    notes = get_notes(text_file_absolute_path)
    print(notes)
    statistics(notes)
    analysis_file_absolute_path = get_absolute_path_for_file(f'hanon_data_{text_file}', analysis_folder_path, 'txt')
    generate_file_for_hanon(notes, analysis_file_absolute_path)
