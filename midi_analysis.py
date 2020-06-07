import re

fhandler = open('song.txt')

exp_pitch = 'pitch=(\d+) '
exp_vol = 'vol=(\d+)'
exp_time = 'Time=(\d+) '

note = []

div = 1440 # ticks for 3/8 bar

for i in fhandler:
    
    if 'Note on' in i:       
        if re.search(exp_pitch, i) and re.search(exp_vol, i) and re.search(exp_time, i): 
            n = int(re.findall(exp_pitch , i)[0])
            v = int(re.findall(exp_vol , i)[0])
            start = int(re.findall(exp_time , i)[0])
            note.append([n, v, -start, False, start, int(start/div), int(int((start % div) / 480))])
            
    if 'Note off' in i: 
        if re.search(exp_pitch, i) and re.search(exp_vol, i) and re.search(exp_time, i): 
            n = int(re.findall(exp_pitch , i)[0])
            v = int(re.findall(exp_vol , i)[0])
            end = int(re.findall(exp_time , i)[0])
            res = [item for item in note if item[0] == n and item[3] == False]
            if len(res) > 1:
                print('error')
                continue
            res[0][2] += end
            res[0][3] = True

fhandler.close()

fhandler_output = open('song_1.txt', 'w')

bar = 0
last_bar = 0

sub_bar = 0
last_sub_bar = 0

for n in note:
    bar = n[5]
    sub_bar = n[6]
    
    if last_bar != bar:
        fhandler_output.write('------------- {0} -------------\n'.format(bar))
        last_bar = bar
        
    
    if last_sub_bar != sub_bar:
        fhandler_output.write('--- {0} ---\n'.format(sub_bar))
        last_sub_bar = sub_bar
    
    fhandler_output.write('N={0} D={2} V={1}\n'.format(n[0], n[1], n[2]))
    
fhandler_output.close()

print(note)
