import matplotlib.pyplot as plt
#import spec
import numpy as np
from decimal import Decimal


from matplotlib import rc
rc('font',**{'family':'serif'})
from matplotlib import rcParams
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'
rcParams['xtick.labelsize'] = 16
rcParams['ytick.labelsize'] = 16
rcParams['xtick.top'] = True
rcParams['ytick.right'] = True
rcParams['lines.linewidth'] = 1.85
rcParams['axes.labelsize'] = 18
rcParams['legend.fontsize'] = 16
rcParams['legend.frameon'] = False
rcParams.update({'figure.autolayout': True})
w = 8
rcParams['figure.figsize'] = w, w/1.6
rcParams['text.usetex'] = True
        
# Centroid data (mean, stdev, max, and min) for 7 separate counts at 8 fluences
mean_j = {0: (458.4, 32.96, 7.19), 1: (459.6, 34.05, 7.41), 2: (452.2, 34.72, 7.68), 3: (450.8, 33.47, 7.43), 4: (443.3, 33.89, 7.65), 5: (435.4, 32.88, 7.55), 6: (429.6, 34.36, 8.0), 7: (388.2, 34.7, 9.24), 8: (325.4, 39.2, 12.43)}
mean_c = {0: (374.8, 36.47, 9.74), 1: (368.6, 36.57, 9.93), 2: (372.2, 37.17, 9.99), 3: (360.9, 37.78, 10.49), 4: (361.4, 36.48, 10.1), 5: (352.4, 36.85, 10.46), 6: (354.5, 37.22, 10.5), 7: (317.6, 41.05, 13.37), 8: (243.5, 45.48, 18.7)}
dev_j = {0: (7.6, 0.84, 0.11), 1: (4.4, 1.44, 0.36), 2: (6.4, 1.36, 0.39), 3: (7.3, 0.9, 0.16), 4: (11.0, 0.54, 0.29), 5: (6.6, 1.12, 0.27), 6: (8.5, 0.9, 0.16), 7: (35.2, 4.1, 3.06), 8: (42.1, 4.22, 3.62)}
dev_c = {0: (9.3, 0.92, 0.36), 1: (9.4, 1.13, 0.4), 2: (6.4, 0.9, 0.27), 3: (16.1, 0.99, 0.63), 4: (8.1, 1.06, 0.37), 5: (8.3, 0.8, 0.43), 6: (7.4, 1.64, 0.53), 7: (4.1, 0.89, 1.15), 8: (7.1, 1.41, 0.94)}
max_j = {0: (473.76, 34.76, 7.34), 1: (464.45, 36.57, 8.01), 2: (461.33, 36.56, 8.15), 3: (463.76, 34.85, 7.62), 4: (451.84, 34.5, 8.16), 5: (445.72, 34.45, 8.0), 6: (441.77, 35.14, 8.26), 7: (363.51, 33.71, 9.28), 8: (347.26, 47.43, 19.79)}
max_c = {0: (386.75, 38.37, 10.45), 1: (383.7, 38.54, 10.54), 2: (381.05, 38.45, 10.42), 3: (380.56, 38.93, 11.5), 4: (370.77, 37.87, 10.53), 5: (361.8, 37.91, 11.01), 6: (361.99, 40.06, 11.18), 7: (321.25, 42.4, 15.58), 8: (256.44, 47.47, 19.8)}
min_j = {0: (451.64, 32.16, 6.97), 1: (452.91, 32.47, 7.07), 2: (445.28, 33.35, 7.32), 3: (443.36, 32.53, 7.23), 4: (422.25, 33.04, 7.36), 5: (429.05, 30.96, 7.22), 6: (418.97, 33.05, 7.77), 7: (360.58, 33.28, 8.53), 8: (239.63, 35.69, 10.42)}
min_c = {0: (362.32, 35.49, 9.39), 1: (358.88, 35.0, 9.52), 2: (365.47, 36.4, 9.61), 3: (338.47, 36.48, 9.92), 4: (353.55, 35.11, 9.47), 5: (338.75, 35.95, 9.99), 6: (340.55, 35.68, 9.98), 7: (313.08, 40.09, 12.48), 8: (236.0, 43.73, 17.5)}
  

marks = ['o', 'x', '^', '>', 'v', '<', '*', 'h', 's']
        
def make_dark_spectra():
    # C series
    plt.figure(1)
    fluence = [r'$0.00\times 10^0$', r'$1.00\times 10^7$', r'$1.58\times 10^7$', 
               r'$2.51\times 10^7$', r'$3.98\times 10^7$', r'$6.31\times 10^7$',
               r'$1.00\times 10^8$', r'$1.58\times 10^8$', r'$3.98\times 10^8$']
    for i in range(0, len(fluence)):
        fn = 'data/CSeriesRawData/C_%i_Dark.Spe' % i
        lines = open(fn, 'r').readlines()
        time = float(lines[9].split()[0])
        spect = np.array(list(map(float, lines[12:1036]))) / time
        channel = np.arange(1, len(spect)+1)
        plt.semilogy(channel, spect, label=fluence[i])
    plt.xlim((1, 130))
    plt.ylim((1e-3, 1e5))
    plt.xlabel('Channel')
    plt.ylabel('Count Rate (cps)')
    plt.legend()
    plt.savefig('c_series_dark_spectra.pdf')
    
    # J series
    plt.figure(2)
    fluence = [r'$0.00\times 10^0$', r'$1.00\times 10^7$', r'$1.58\times 10^7$', 
               r'$2.51\times 10^7$',  '',                  r'$6.31\times 10^7$',
               r'$1.00\times 10^8$', r'$1.58\times 10^8$', r'$3.98\times 10^8$']
    for i in range(0, len(fluence)):
        if i == 4:
            # this measurement was missing
            continue
        fn = 'data/JSeriesRawData/J_%i_Dark.Spe' % i
        lines = open(fn, 'r').readlines()
        time = float(lines[9].split()[0])
        spect = np.array(list(map(float, lines[12:1036]))) / time
        channel = np.arange(1, len(spect)+1)
        plt.semilogy(channel, spect, label=fluence[i])
    plt.xlim((1, 80))
    plt.xlabel('Channel')
    plt.ylabel('Count Rate (cps)')
    plt.legend()
    plt.savefig('j_series_dark_spectra.pdf')
    

def make_centroid_vs_fluence():
    fluence = np.array([0,1e7, 1.57e7, 2.51e7, 3.98e7, 6.31e7, 1e8, 1.58e8, 3.98e8])
    
    for i in [3, 4]:
        plt.figure(i)
        if i == 3 :
            means, devs = mean_c, dev_c
        else :
            means, devs = mean_j, dev_j       
        dat =[]
        dev = []
        for num in range(9):
            dat.append(means[num][0])
            dev.append(devs[num][0])
        plt.errorbar(fluence, dat, dev, fmt='o', color='k', label='centroid')
        flu = np.linspace(1e7, 4e8, 100)
        plt.plot(flu, np.poly1d(np.polyfit(fluence, dat, 1, w = 1/np.array(dev)**2))(flu), linestyle = '--', color='k', label='linear fit')
        plt.plot(flu, np.ones(len(flu))*(dat[0]       ),linestyle = '-', color='r', label='centroid (unirradiated)')
        plt.plot(flu, np.ones(len(flu))*(dat[0]+dev[0]), linestyle = ':', color='r', label='centroid (unirradiated) $\pm$ error')
        plt.plot(flu, np.ones(len(flu))*(dat[0]-dev[0]), linestyle = ':', color='r')
        plt.ticklabel_format(style='plain', axis='y')
        plt.xscale('log', nonposy='clip')
        plt.ylim(200, 450)
        plt.xlim(0.95e7, 4.1e8)
        #plt.title('C-series Centroid Location vs Neutron Fluence')
        plt.xlabel('Fission Neutron Fluence (cm$^{-2}$)')
        plt.ylabel('$^{137}$Cs Peak Centroid (channel)')      
        
        
        h, l = plt.gca().get_legend_handles_labels()
        plt.legend([h[3],h[0],h[1],h[2]], [l[3], l[0], l[1], l[2]])
        
        #plt.ticklabel_format(useOffset=False)

        if i == 3:
            plt.ylim(200, 450)
            plt.savefig('c_series_centroid_fluence.pdf')
        else:
            plt.ylim(250, 480)
            plt.savefig('j_series_centroid_fluence.pdf')     
  
    
def make_fwhm_vs_fluence():
    fluence = np.array([0,1e7, 1.57e7, 2.51e7, 3.98e7, 6.31e7, 1e8, 1.58e8, 3.98e8])
    
    for i in [5, 6]:
        plt.figure(i)
        if i == 5 :
            means, devs = mean_c, dev_c
        else :
            means, devs = mean_j, dev_j       
        dat =[]
        dev = []
        for num in range(9):
            dat.append(means[num][2])
            dev.append(devs[num][2])
        plt.errorbar(fluence, dat, dev, fmt='o', color='k', label='FWHM')
        flu = np.linspace(1e7, 4e8, 100)
        plt.plot(flu, np.poly1d(np.polyfit(fluence, dat, 1, w = 1/np.array(dev)**2))(flu), linestyle = '--', color='k', label='linear fit')        
        #plt.plot(flu, np.poly1d(np.polyfit(fluence, dat, 2))(flu), linestyle = '--', color='k', label='linear fit')        
        
        plt.plot(flu, np.ones(len(flu))*(dat[0]       ),linestyle = '-', color='r', label='FWHM (unirradiated)')
        plt.plot(flu, np.ones(len(flu))*(dat[0]+dev[0]), linestyle = ':', color='r', label='FWHM (unirradiated) $\pm$ error')
        plt.plot(flu, np.ones(len(flu))*(dat[0]-dev[0]), linestyle = ':', color='r')
        plt.xscale('log', nonposy='clip')
        plt.xlim(0.95e7, 4.1e8)
        
        plt.xlabel('Fission Neutron Fluence (cm$^{-2}$)')
        plt.ylabel('$^{137}$Cs Peak FWHM (\%)')      

        h, l = plt.gca().get_legend_handles_labels()
        plt.legend([h[3],h[0],h[1],h[2]], [l[3], l[0], l[1], l[2]])

        if i == 5:
            plt.ylim(8, 20)
            plt.savefig('c_series_fwhm_fluence.pdf')
        else:
            plt.ylim(6, 18)
            plt.savefig('j_series_fwhm_fluence.pdf')     
    
def make_phs():
    lgn_lab = ['LaBr$_3$:Ce, $^{137}$Cs exposed', 
               'ZnS:Ag Hornyak, AmBe exposed', 
               r'Dark Spectra at $3.98\times 10^8$ cm$^{-2}$']

    lines = open('data/J_0_LaBr3_Cs137_420s.spe', 'r').readlines()
    time = float(lines[9].split()[0])
    spect_labr3 = np.array(list(map(float, lines[12:1036]))) / time
        
    lines = open('data/J_0_Hornyak_AmBe_1800s_Ppos.spe', 'r').readlines()
    time = float(lines[9].split()[0])
    spect_ambe = np.array(list(map(float, lines[12:1036]))) / time
 
    lines = open('data/JSeriesRawData/J_8_Dark.Spe', 'r').readlines()
    time = float(lines[9].split()[0])
    spect_j_dark = np.array(list(map(float, lines[12:1036]))) / time
    
    channel = np.arange(len(spect_labr3))
    plt.figure(7)
    plt.plot(channel, spect_labr3, 'k')
    plt.plot(channel, spect_ambe, 'b')
    plt.plot(channel, spect_j_dark, 'r')
    plt.yscale('log')
    plt.xlabel('Channel Number')
    plt.ylabel('Count Rate (cps)')
    plt.xlim(0, 600)
    plt.ylim(0, 1e4)
    
    
    plt.legend(lgn_lab, loc=1)
    plt.savefig('phs.pdf')
    plt.clf()    

if __name__ == '__main__':
    
    make_dark_spectra()
    make_centroid_vs_fluence()
    make_fwhm_vs_fluence()
    make_phs()