from converter import convert_midi_file_to_text
from hanon_analysis import hanon_analysis

file = 'hannon.mid'
convert_midi_file_to_text(file)
hanon_analysis(file)