from converter import convert_midi_file_to_text
from midi_analysis import analysis_a

file = 'hannon.mid'
convert_midi_file_to_text(file)
analysis_a(file)