import numpy as np
from itertools import islice
import re

class FLACS_geom:
    def __init__(self, file):
        self.file = file

    def search(self, word):                                         ## searches for word and then yields info from 1, 2 or 3 lines after
        self.file.seek(0)                                           ## seek to start of file
        for line in self.file:
            if re.search(word, line):
                yield next(self.file)
                yield next(self.file)
                yield next(self.file)

################### islice(iterater, yield choice, stop, number of yields) #### i think.... #########

    def sort_info1(self):
        """This gets box coordinates"""
        return list(islice(self.search('BOX'), 0, None, 3))
    def sort_info2(self):                                           
        """This gets box dimensions"""
        return list(islice(self.search('BOX'), 1, None, 3))
    def sort_info3(self):                                           
        """This gets cylinder coordinates"""
        return list(islice(self.search('CYLINDER'), 0, None, 3))
    def sort_info4(self):                                           
        """This gets cylinder dimensions"""
        return list(islice(self.search('CYLINDER'), 1, None, 3))        
    def sort_info5(self):                                           
        """This gets cylinder direction"""
        return list(islice(self.search('CYLINDER'), 2, None, 3))        

    def unit_conversion1(self):
        return np.around((np.array(np.loadtxt(self.sort_info1())) / 1000),decimals = 1).tolist() 
    def unit_conversion2(self):
        return np.around((np.array(np.loadtxt(self.sort_info2())) / 1000),decimals = 3).tolist()         
    def unit_conversion3(self):
        return np.around((np.array(np.loadtxt(self.sort_info3())) / 1000),decimals = 1).tolist() 
    def unit_conversion4(self):
        return np.around((np.array(np.loadtxt(self.sort_info4())) / 1000),decimals = 3).tolist()

######################################################################################################        
        
        
    def sort_to1(self, range):
        return list(a for a in self.sort_info1() if float(float(a.split()[2])) < range) 
        ## , list(a for a in self.sort_info3() if float(float(a.split()[2])) < range)

        
    def sort_to2(self, ratio):
        """This method sorts decks"""    
        return list([a,b] for a,b in zip(self.unit_conversion1(), self.unit_conversion2()) if 
        (
        ((b[2] != 0 and b[0] != 0 and b[1] != 0) and (b[0] > 0.5 and b[1] > 0.5)) and 
        (((b[2] / b[0]) < ratio and  (b[2] / b[1]) < ratio) or 
        (b[0] > 0.5 and b[1] > 0.5 and b[2] == 0)))
        )
        
    def sort_to3(self, ratio0, ratio1):
        """This method sorts pipe diameters"""    
        return list([a,b,c] for a,b,c in zip(self.unit_conversion3(), self.unit_conversion4(), self.sort_info5()) if 
        (
        (b[0] < ratio1*0.0254) and (b[0] >= ratio0*0.0254))
        )

    def sort_to4(self, ratio):
        """This method sorts walls"""    
        return list([a,b] for a,b in zip(self.unit_conversion1(), self.unit_conversion2()) if 
        (
        ((b[2] != 0 and b[0] != 0 and b[1] != 0) and 
        ((b[2] > 1.5 and b[1] > 1.5) or (b[2] > 1.5 and b[0] > 1.5))) and
        (((b[0] / b[2]) < ratio and (b[0] / b[1]) < ratio) or 
        ((b[1] / b[2]) < ratio and (b[1] / b[0]) < ratio)))
        )

    def sort_to5(self, ratio):
        """This method sorts structure, beams and columns"""    
        return list([a,b] for a,b in zip(self.unit_conversion1(), self.unit_conversion2()) if 
        (
        (b[2] != 0 and b[0] != 0 and b[1] != 0) and 
        (((b[0] / b[2]) < ratio and (b[1] / b[2]) < ratio) or 
        ((b[0] / b[1]) < ratio and (b[2] / b[1]) < ratio) or 
        ((b[2] / b[0]) < ratio and (b[1] / b[0]) < ratio))) 
        )

    def sort_to6(self):
        """This method filters large boxes"""    
        return list([a,b] for a,b in zip(self.unit_conversion1(), self.unit_conversion2()) if 
        (
        (b[0] > 10 and b[1] > 10 and b[2] > 0.5) or 
        (b[0] > 10 and b[1] > 0.5 and b[2] > 10) or 
        (b[0] > 0.5 and b[1] > 10 and b[2] > 10))   
        )

######################################################################################################

        
#    def filter_duplicates(self):
#        """This method filters duplicate boxes"""    
#        seen = set()
#        seen_add = seen.add
#        return list([a,b] for a,b in zip(self.sort_info3(), self.sort_info4()) if not b in seen or seen_add(b))
        
######################################################################################################

# a = FLACS_geom(open("combined.mcr")).sort_to4(0.2)
# b = FLACS_geom(open("combined.mcr")).sort_to2(0.2)
# c = FLACS_geom(open("combined.mcr")).sort_to3(2,4)
# d = FLACS_geom(open("combined.mcr")).sort_to3(0,2)
# e = FLACS_geom(open("combined.mcr")).sort_to6()
f = FLACS_geom(open("combined.mcr")).filter_duplicates()
g = FLACS_geom(open("combined.mcr")).sort_info1()
h = FLACS_geom(open("combined.mcr")).sort_info3()
print(len(g),len(h)) 




