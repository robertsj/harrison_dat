import matplotlib.pyplot as plt
import spec
import os
import operator
import numpy as np
from decimal import Decimal


from matplotlib import rc
rc('font',**{'family':'serif'})
from matplotlib import rcParams
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'
rcParams['xtick.labelsize'] = 14
rcParams['ytick.labelsize'] = 14
rcParams['lines.linewidth'] = 1.85
rcParams['axes.labelsize'] = 16
rcParams['legend.fontsize'] = 14
rcParams.update({'figure.autolayout': True})
rcParams['figure.figsize'] = 8, 8/1.6
rcParams['text.usetex'] = True

'''

The attachments contain all the data you need. I tested a J-Series SiPM and a C-Series SiPM, hence the naming convention.
In all the raw spectra (.spe), the first letter denotes the SiPM series, the middle number denotes how much fluence had been deposited in that SiPM
(see the table in my memo where zero denotes zero fluence and increasing number refer to the increments in Table 1 of the memo),
while the last number or word denotes what iteration if a Cs-137 spectrum or whether it was a dark spectrum or background spectrum.
The Excel file contains the metadata from the spectra including full energy peak (FEP) centroid location, FEP FWHM, and their averages, standard deviations, etc.
'''



plt_dict = {0:'b' , 1:'g', 2:'r', 3:'c', 4:'m', 5:'y', 6:'k', 7:'b--', 8:'g--'}


mean_j = {0: (458.4, 32.96, 7.19), 
          1: (459.6, 34.05, 7.41), 
          2: (452.2, 34.72, 7.68), 
          3: (450.8, 33.47, 7.43), 
          4: (443.3, 33.89, 7.65), 
          5: (435.4, 32.88, 7.55),
          6: (429.6, 34.36, 8.00), 
          7: (388.2, 34.70, 9.24),
          8: (325.4, 39.20,12.43)}
mean_c = {0: (374.8, 36.47, 9.74), 
          1: (368.6, 36.57, 9.93),
          2: (372.2, 37.17, 9.99),
          3: (360.9, 37.78, 10.49), 
          4: (361.4, 36.48, 10.1), 
          5: (352.4, 36.85, 10.46), 
                      6: (354.5, 37.22, 10.5), 
                         7: (317.6, 41.05, 13.37), 
                            8: (243.5, 45.48, 18.7)}
dev_j = {0: (7.6, 0.84, 0.11), 
         1: (4.4, 1.44, 0.36), 
            2: (6.4, 1.36, 0.39), 
               3: (7.3, 0.9, 0.16), 
                  4: (11.0, 0.54, 0.29), 
                     5: (6.6, 1.12, 0.27), 
                        6: (8.5, 0.9, 0.16), 
                           7: (35.2, 1.7, 0.07), 
                              8: (42.1, 4.22, 3.62)}
dev_c = {0: (9.3, 0.92, 0.36), 1: (9.4, 1.13, 0.4), 2: (6.4, 0.9, 0.27), 3: (16.1, 0.99, 0.63), 4: (8.1, 1.06, 0.37), 5: (8.3, 0.8, 0.43), 6: (7.4, 1.64, 0.53), 7: (4.1, 0.89, 1.15), 8: (7.1, 1.41, 0.94)}
max_j = {0: (473.76, 34.76, 7.34), 1: (464.45, 36.57, 8.01), 2: (461.33, 36.56, 8.15), 3: (463.76, 34.85, 7.62), 4: (451.84, 34.5, 8.16), 5: (445.72, 34.45, 8.0), 6: (441.77, 35.14, 8.26), 7: (363.51, 33.71, 9.28), 8: (347.26, 47.43, 19.79)}
max_c = {0: (386.75, 38.37, 10.45), 1: (383.7, 38.54, 10.54), 2: (381.05, 38.45, 10.42), 3: (380.56, 38.93, 11.5), 4: (370.77, 37.87, 10.53), 5: (361.8, 37.91, 11.01), 6: (361.99, 40.06, 11.18), 7: (321.25, 42.4, 15.58), 8: (256.44, 47.47, 19.8)}
min_j = {0: (451.64, 32.16, 6.97), 1: (452.91, 32.47, 7.07), 2: (445.28, 33.35, 7.32), 3: (443.36, 32.53, 7.23), 4: (422.25, 33.04, 7.36), 5: (429.05, 30.96, 7.22), 6: (418.97, 33.05, 7.77), 7: (360.58, 33.28, 8.53), 8: (239.63, 35.69, 10.42)}
min_c = {0: (362.32, 35.49, 9.39), 1: (358.88, 35.0, 9.52), 2: (365.47, 36.4, 9.61), 3: (338.47, 36.48, 9.92), 4: (353.55, 35.11, 9.47), 5: (338.75, 35.95, 9.99), 6: (340.55, 35.68, 9.98), 7: (313.08, 40.09, 12.48), 8: (236.0, 43.73, 17.5)}


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

                nam_st = nam + ' = spec.spectrum(abs_path, True)'
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


    return cs_li, dk_li, bg_li


cs_li, dk_li, bg_li = main()

cs_li.sort(key=operator.attrgetter('fluence'))
dk_li.sort(key=operator.attrgetter('fluence'))
bg_li.sort(key=operator.attrgetter('fluence'))

def gen_plot():

    pass




def fig_1():
    num = 0
    c_dk_li = []
    for spect in dk_li:
        if spect.series == 'c':
            c_dk_li.append(spect)

    #lgn_lab = ["${:.2}$".format(0.00)]
    lgn_lab = ["${:.2}$".format(0.00)]


   # plt.figure(1, figsize=(
    for index,spect in enumerate(c_dk_li):
        plt.semilogy([it + 1 for it in range(len(spect.spec))], np.array(spect.spec)/1800.,plt_dict[num] )      #form channel list and plot spectrum

        if index == 0:
            pass
        else:
            tmp = "{:.2E}".format(Decimal(str(spec.fluence_dict[num])))
            a,b=tmp.split('E+')
            ab = r'$%.2f \times 10^{%i}$' % (float(a), int(b))
            print('ab = ', ab)
            #lgn_lab.append("{:.2E}".format(Decimal(str(spec.fluence_dict[num]))))
            lgn_lab.append(ab)
        num +=1


    plt.xlim(0,120)
    plt.ylabel('Count Rate (cps)')
    plt.xlabel('Channel Number')
    #plt.title('C-Series Dark Spectra')
    plt.legend(lgn_lab, loc=1)
    plt.savefig('figs/fig_1.pdf')
    plt.clf()

def fig_2():
    num = 0
    j_dk_li = []
    for spect in dk_li:
        if spect.series == 'j':
            j_dk_li.append(spect)

    lgn_lab = ["${:.2}$".format(0.00)]

    for index,spect in enumerate(j_dk_li):
        plt.semilogy([it + 1 for it in range(len(spect.spec))], spect.spec,plt_dict[num] )      #form channel list and plot spectrum

        if index == 0:
            pass
        else:
            tmp = "{:.2E}".format(Decimal(str(spec.fluence_dict[num])))
            a,b=tmp.split('E+')
            ab = r'$%.2f \times 10^{%i}$' % (float(a), int(b))
            print('ab = ', ab)
            #lgn_lab.append("{:.2E}".format(Decimal(str(spec.fluence_dict[num]))))
            lgn_lab.append(ab)        
            #lgn_lab.append("{:.2E}".format(Decimal(str(spec.fluence_dict[num]))))
        num +=1


    plt.xlim(0,80)
    plt.ylabel('Count Rate (cps)')
    plt.xlabel('Channel Number')
    #plt.title('J-Series Dark Spectra')
    plt.legend(lgn_lab, loc=1)
    plt.savefig('figs/fig_2.pdf')
    plt.clf()

def fig_3():
    dat =[]
    dev = []
    fl_li =[]

    for num in range(9):
        dat.append(mean_c[num][0])
        dev.append(dev_c[num][0])
        fl_li.append(spec.fluence_dict[num])
        print(spec.fluence_dict[num])


    #plt.plot()
    plt.errorbar(fl_li, dat, dev, fmt='o', color='k')
    plt.plot(np.unique(fl_li), np.poly1d(np.polyfit(fl_li, dat, 1))(np.unique(fl_li)), linestyle = '--', color='k')
    plt.plot(np.unique(fl_li), np.poly1d(np.polyfit(fl_li, [dat[0] for it in dat], 1))(np.unique(fl_li)), linestyle = '-', color='r')
    plt.plot(np.unique(fl_li), np.poly1d(np.polyfit(fl_li, [(dat[0]+dev[0]) for it in dat], 1))(np.unique(fl_li)), linestyle = '--', color='r')
    plt.plot(np.unique(fl_li), np.poly1d(np.polyfit(fl_li, [(dat[0]-dev[0]) for it in dat], 1))(np.unique(fl_li)), linestyle = '--', color='r')
    plt.xscale('log', nonposy='clip')
    plt.ylim(200, 450)
    plt.xlim(1e7, 5e8)
    #plt.title('C-series Centroid Location vs Neutron Fluence')
    plt.xlabel('Fission Neutron Fluence (cm$^{-2}$)')
    plt.ylabel('$^{137}$Cs Peak FWHM (\%)')
    plt.savefig('figs/fig_3.pdf')
    plt.clf()


def fig_4():
    dat =[]
    dev = []
    fl_li =[]

    for num in range(9):
        dat.append(mean_j[num][0])
        dev.append(dev_j[num][0])
        fl_li.append(spec.fluence_dict[num])
        print(spec.fluence_dict[num])


    #plt.plot()
    plt.errorbar(fl_li, dat, dev, fmt='o', color='k')
    plt.plot(np.unique(fl_li), np.poly1d(np.polyfit(fl_li, dat, 1))(np.unique(fl_li)), linestyle = '--', color='k')
    plt.plot(np.unique(fl_li), np.poly1d(np.polyfit(fl_li, [dat[0] for it in dat], 1))(np.unique(fl_li)), linestyle = '-', color='r')
    plt.plot(np.unique(fl_li), np.poly1d(np.polyfit(fl_li, [(dat[0]+dev[0]) for it in dat], 1))(np.unique(fl_li)), linestyle = '--', color='r')
    plt.plot(np.unique(fl_li), np.poly1d(np.polyfit(fl_li, [(dat[0]-dev[0]) for it in dat], 1))(np.unique(fl_li)), linestyle = '--', color='r')


    plt.xscale('log', nonposy='clip')
    plt.ylim(300, 480)
    plt.xlim(1e7, 5e8)
    #plt.title('J-series Centroid Location vs Neutron Fluence')
    plt.xlabel('Fission Neutron Fluence (cm$^{-2}$)')
    plt.ylabel('$^{137}$Cs Peak FWHM (\%)')
    plt.savefig('figs/fig_4.pdf')
    plt.clf()


def fig_5():
    dat =[]
    dev = []
    fl_li =[]

    for num in range(9):
        dat.append(mean_c[num][2])
        dev.append(dev_c[num][2])
        fl_li.append(spec.fluence_dict[num])
        print(spec.fluence_dict[num])


    #plt.plot()
    plt.errorbar(fl_li, dat, dev, fmt='o', color='k')
    plt.plot(np.unique(fl_li), np.poly1d(np.polyfit(fl_li, dat, 1))(np.unique(fl_li)), linestyle = '--', color='k')
    plt.plot(np.unique(fl_li), np.poly1d(np.polyfit(fl_li, [dat[0] for it in dat], 1))(np.unique(fl_li)), linestyle = '-', color='r')
    plt.plot(np.unique(fl_li), np.poly1d(np.polyfit(fl_li, [(dat[0]+dev[0]) for it in dat], 1))(np.unique(fl_li)), linestyle = '--', color='r')
    plt.plot(np.unique(fl_li), np.poly1d(np.polyfit(fl_li, [(dat[0]-dev[0]) for it in dat], 1))(np.unique(fl_li)), linestyle = '--', color='r')


    plt.xscale('log', nonposy='clip')
    plt.ylim(5, 21)
    plt.xlim(1e7, 5e8)
    #plt.title('C-series Centroid Location vs Neutron Fluence')
    plt.xlabel('Fission Neutron Fluence (cm$^{-2}$)')
    plt.ylabel('$^{137}$Cs Peak FWHM (\%)')
    plt.savefig('figs/fig_5.pdf')
    plt.clf()


def fig_6():
    dat =[]
    dev = []
    fl_li =[]

    for num in range(9):
        dat.append(mean_j[num][2])
        dev.append(dev_j[num][2])
        fl_li.append(spec.fluence_dict[num])
        print(spec.fluence_dict[num])


    #plt.plot()
    plt.errorbar(fl_li, dat, dev, fmt='o', color='k')
    plt.plot(np.unique(fl_li), np.poly1d(np.polyfit(fl_li, dat, 1))(np.unique(fl_li)), linestyle = '--', color='k')
    plt.plot(np.unique(fl_li), np.poly1d(np.polyfit(fl_li, [dat[0] for it in dat], 1))(np.unique(fl_li)), linestyle = '-', color='r')
    plt.plot(np.unique(fl_li), np.poly1d(np.polyfit(fl_li, [(dat[0]+dev[0]) for it in dat], 1))(np.unique(fl_li)), linestyle = '--', color='r')
    plt.plot(np.unique(fl_li), np.poly1d(np.polyfit(fl_li, [(dat[0]-dev[0]) for it in dat], 1))(np.unique(fl_li)), linestyle = '--', color='r')


    plt.xscale('log', nonposy='clip')
    plt.ylim(5, 14)
    plt.xlim(1e7, 5e8)
    #plt.title('J-series Centroid Location vs Neutron Fluence')
    plt.xlabel('Fluence (cm$^{-2}$)')
    plt.ylabel('$^{137}$Cs Peak FWHM (%)')
    plt.savefig('figs/fig_6.pdf')
    plt.clf()

def fig_7():

    lgn_lab = ['LaBr$_3$:Ce, $^{137}$Cs exposed', 'ZnS:Ag Hornyak, AmBe exposed', 'Dark Spectra at $3.98\cdot 10^8$ cm$^{-2}$']
    script_dir = os.path.dirname(__file__)

    rel_420 = 'data/J_0_LaBr3_Cs137_420s.spe'
    abs_420 = os.path.join(script_dir, rel_420)
    spec_420 = spec.spectrum(abs_420)

    rel_1800 = 'data/J_0_Hornyak_AmBe_1800s_Ppos.spe'
    abs_1800 = os.path.join(script_dir, rel_1800)
    spec_1800 = spec.spectrum(abs_1800)

    plt.plot(range(len(spec_420.spec)), spec_420.spec, 'k')
    plt.plot(range(len(spec_1800.spec)), spec_1800.spec, 'b')
    plt.plot(range(len(dk_li[len(dk_li)-1].spec)), dk_li[len(dk_li)-1].spec, 'r')
    plt.yscale('log')
    plt.xlabel('Channel Number')
    plt.ylabel('Count Rate (cps)')
    plt.xlim(0, 600)
    plt.ylim(0, 1e7)
    
    
    plt.legend(lgn_lab, loc=1)
    plt.savefig('figs/fig_7.pdf')
    plt.clf()

def fig_8():
    pass


if __name__ == '__main__':
    main()
    for num in range(7):
        num += 1

        print(num)
        exec('fig_' + str(num) + '()')

