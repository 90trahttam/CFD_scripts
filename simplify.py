#!/usr/bin/env python 
# written by MRHA 
# version 1.1 06/04/2016; edited 10/2016 for wall filter logic, also refined deck filter and structure filter and long objects, added a volume grab function also
# version 1.2 28/11/2016; debugged

import time
start_time = time.time()
#print(start_time)
import os
import glob
import re
import sys 
import pandas as pd
import numpy as np

######## INPUT #################################################################################################################################################################

# myfile=sys.argv[1]     ####### FLACS MACRO FILE TO EDIT 
myfile='L3mezz.mcr'     ####### FLACS MACRO FILE TO EDIT 


#res = open('test.mcr','w'); res.write('DATABASE NEW OBJECT "test_fix"\nADD\n')
#resb = open('testb.mcr','w') #; res.write('DATABASE NEW OBJECT "test_fix"\nADD\n')
#resc = open('testc.mcr','w')
test_list = []
i = 0   
with open(myfile) as f:
    for line in f:
        if re.search('BOX',line):
            line=next(f); cx,cy,cz=round(float(line.split()[-3]),1)/1,round(float(line.split()[-2]),1)/1,round(float(line.split()[-1]),1)/1
            line=next(f); dx,dy,dz=round(float(line.split()[-3]),3)/1,round(float(line.split()[-2]),3)/1,round(float(line.split()[-1]),3)/1
            test_input = (i, cx , cy, cz, dx, dy, dz)
            test_list.append(test_input)
            i+=1
        else:
            continue
sys.stdout.write('x'); sys.stdout.flush();

#cols=['cx','cy','cz','dx','dy','dz']  
#test_frame=pd.DataFrame(test_list,columns=cols).sort_values(['cx','cy']).drop_duplicates().reset_index(drop=True)


groups = []   
group = [] 
   

#a = list(i for i in range(len(test_frame)))
#print(a)
max_dist = 1

#for i in range(len(a) -1) :
#    if len(a) > 0:
#        group.append(a[0])
#        for ii in range(a[0],len(test_frame)-1):
#            if (((0 <= abs(test_frame.loc[a[0],'cx'] - test_frame.loc[ii,'cx']) < max_dist) and (0 <= abs(test_frame.loc[a[0],'cy'] - test_frame.loc[ii,'cy']) < max_dist) and (0 <= abs(test_frame.loc[a[0],'cz'] - test_frame.loc[ii,'cz']) < max_dist)) and ((0<= abs((test_frame.loc[a[0],'cx'] + test_frame.loc[a[0],'dx']) - (test_frame.loc[ii,'cx'] + test_frame.loc[ii,'dx'])) < max_dist) and (0<= abs((test_frame.loc[a[0],'cy'] + test_frame.loc[a[0],'dy']) - (test_frame.loc[ii,'cy'] + test_frame.loc[ii,'dy'])) < max_dist) and (0<= abs((test_frame.loc[a[0],'cz'] + test_frame.loc[a[0],'dz']) - (test_frame.loc[ii,'cz'] + test_frame.loc[ii,'dz'])) < max_dist))):
#                group.append(ii)
#            else:
#                continue
#
#        groups.append(set(group))
#        for iii in group:
#
#            if iii in a:
#                a.remove(iii)
#            else:
#                continue
#        group = []
#    else:
#        break
#    sys.stdout.write('.'); sys.stdout.flush();

#df2 = [(i,x) for i,x in enumerate(test_list)]
df2 = sorted(test_list,key=lambda x: x[1])
df3 = sorted(test_list,key=lambda x: x[2])
df4 = sorted(test_list,key=lambda x: x[3])

cols=['i','cx','cy','cz','dx','dy','dz']  
test_frame=pd.DataFrame(df3,columns=cols).set_index('i')

#df4 = sorted(test_list,key=lambda x: x[0])
#for i in df2:
#    if (df2[i][2] == 390.000 and df2[i][3] == 38.000 and df2[i][4] == 49.200) or  (df2[i][3] == 38.100 and df2[i][2] == 390.100 and df2[i][4] == 49.400):
#        resc.write('{}\n'.format(i))
#    else:
#        continue

resultx = []
while df2:
    if len(df2) > 1:
        a = df2.pop(0)
        alist=[a[0]]
#        while ((abs(a[1] - df2[0][1]) < max_dist)) :#and (abs(a[2] - df3[0][2]) <= max_dist) and (abs(a[3] - df3[0][3]) <= max_dist)):
        while ((((a[1] + max_dist) >=  df2[0][1]))):#  and (abs(a[2] - df3[0][2]) < max_dist)):# and (abs(a[3] - df3[0][3]) < max_dist)) and ((abs((a[1] + a[4]) - (df3[0][1] + df3[0][4])) < max_dist) and (abs((a[2] + a[5]) - (df3[0][2] + df3[0][5])) < max_dist) and (abs((a[3] + a[6]) - (df3[0][3] + df3[0][6])) < max_dist))):
            alist.append(df2.pop(0)[0])
            if df2:

                continue
            else:

                break
        resultx.append(alist)
#        resb.write('{}\n'.format(alist))
    else:
        resultx.append(a[0])
#        resb.write('{}\n'.format(a[0]))
        break

resulty = []
while df3:
    if len(df3) > 1:
        a = df3.pop(0)
        alist=[a[0]]
#        while ((abs(a[1] - df3[0][1]) < max_dist)): # and (abs(a[2] - df3[0][2]) <= max_dist) and (abs(a[3] - df3[0][3]) <= max_dist)):
        while (((a[2] + max_dist) >= df3[0][2])):#  and (abs(a[2] - df3[0][2]) < max_dist)):# and (abs(a[3] - df3[0][3]) < max_dist)) and ((abs((a[1] + a[4]) - (df3[0][1] + df3[0][4])) < max_dist) and (abs((a[2] + a[5]) - (df3[0][2] + df3[0][5])) < max_dist) and (abs((a[3] + a[6]) - (df3[0][3] + df3[0][6])) < max_dist))):
            alist.append(df3.pop(0)[0])
            if df3:

                continue
            else:

                break
        resulty.append(alist)
#        resb.write('{}\n'.format(alist))
    else:
        resulty.append(a[0])
#        resb.write('{}\n'.format(a[0]))
        break

resultz = []
while df4:
    if len(df4) > 1:
        a = df4.pop(0)
        alist=[a[0]]
#        while ((abs(a[1] - df4[0][1]) < max_dist)):# and (abs(a[2] - df3[0][2]) <= max_dist) and (abs(a[3] - df3[0][3]) <= max_dist)):
        while ((((a[3] + max_dist) >=  df4[0][3]))):#  and (abs(a[2] - df3[0][2]) < max_dist)):# and (abs(a[3] - df3[0][3]) < max_dist)) and ((abs((a[1] + a[4]) - (df3[0][1] + df3[0][4])) < max_dist) and (abs((a[2] + a[5]) - (df3[0][2] + df3[0][5])) < max_dist) and (abs((a[3] + a[6]) - (df3[0][3] + df3[0][6])) < max_dist))):
            alist.append(df4.pop(0)[0])
            if df4:

                continue
            else:

                break
        resultz.append(alist)
#        resb.write('{}\n'.format(alist))
    else:
        resultz.append(a[0])
#        resb.write('{}\n'.format(a[0]))
        break

#
#for i in range(len(result)-1):    
#
#    a = test_frame.loc[result[i]]
#    a['mx'] = a['cx'] + a['dx']
#    a['my'] = a['cy'] + a['dy']
#    a['mz'] = a['cz'] + a['dz']
#    
#    b = pd.DataFrame()
#    c = pd.DataFrame()
#    
#    b['max_xyz'] = a[['mx','my','mz']].max()
#    c['min_xyz'] = a[['cx','cy','cz']].min()
#
#    res.write('BOX\n{0:.3f} {1:.3f} {2:.3f}\n{3:.3f} {4:.3f} {5:.3f}\n0 0 0\n0\n0\n'.format(c.loc['cx'].item(),c.loc['cy'].item(),c.loc['cz'].item(), b.loc['mx'].item() - c.loc['cx'].item(),  b.loc['my'].item() - c.loc['cy'].item(),  b.loc['mz'].item() - c.loc['cz'].item()))
#sys.stdout.write('o'); sys.stdout.flush();
#
# 
#
#res.write('FILE EXIT YES YES\n'); res.close()  
#resb.close()                   
#resc.close() 
            
            
           
# main()
print("--- %s seconds ---" % (time.time() - start_time))
