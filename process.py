import numpy as np
import matplotlib.pyplot as plt
import csv
import spec
import os

'''

The attachments contain all the data you need. I tested a J-Series SiPM and a C-Series SiPM, hence the naming convention.
In all the raw spectra (.spe), the first letter denotes the SiPM series, the middle number denotes how much fluence had been deposited in that SiPM
(see the table in my memo where zero denotes zero fluence and increasing number refer to the increments in Table 1 of the memo),
while the last number or word denotes what iteration if a Cs-137 spectrum or whether it was a dark spectrum or background spectrum.
The Excel file contains the metadata from the spectra including full energy peak (FEP) centroid location, FEP FWHM, and their averages, standard deviations, etc.



'''

def main():

    cs_li = []
    dk_li = []
    bg_li = []

    directories = ['data/CSeriesRawData', 'data/JSeriesRawData']            #What directories to load from
    script_dir = os.path.dirname(__file__)

    for directory in directories:
        ndirectory = os.path.join(script_dir, directory)
        for filename in os.listdir(ndirectory):


            if filename[-3:] == 'Spe':                                      #Grab only spe files and form abs path

                nam = filename[:-4]
                rel_path =  directory + '/' + filename
                abs_path= os.path.join(script_dir, rel_path)

                nam_st = nam + ' = spec.spectrum(abs_path)'
                exec(nam_st)                                          #name_spectrum based on file name

                tp = None                           #Sort and store by spectrum type
                exec('tp = ' + nam + '.tp')

                if tp == None:
                    pass
                elif tp == 'bg':
                    exec('bg_li.append(' + nam + ')')
                elif tp == 'dk':
                    exec('dk_li.append(' + nam + ')')
                elif tp == 'cs':
                    exec('cs_li.append(' + nam + ')')


            else:
                pass


    for item in cs_li:
        print item.nam
    print len(dk_li)
    print len(bg_li)


def gen_plot():

    pass

def fig_1():
    pass

def fig_2():
    pass

def fig_3():
    pass

def fig_4():
    pass

def fig_5():
    pass

def fig_6():
    pass

def fig_7():
    pass

def fig_8():
    pass


if __name__ == '__main__':
    main()