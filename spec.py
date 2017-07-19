
import numpy
import os




class  spectrum():
    def __init__(self, fname):
        t_irr_dict = {0:0 , 1:59.6 , 2: 34.9, 3:55.3, 4:87.6, 5:138.9, 6:220.1, 7:348.8, 8:1429.1}
        fluence_dict = {0:0, 1:1e7 , 2:1.58e7, 3:2.51e7, 4:3.98e7, 5:6.31e7 , 6:10e8, 7:1.58e8, 8:3.98e8 }
        done = False
        self.spec = []

        i_name = fname.rfind('/') + 1  # Plus one to remove the slash itself

        self.name = fname[i_name:-4]

        if self.name[4:] == 'Bkgd':    # Store type of spectrum
            self.tp = 'bg'
            self.iteration = None

        elif self.name[4:] == 'Dark':
            self.tp = 'dk'
            self.iteration = None

        else:
            self.iteration = int(self.name[4:])
            self.tp = 'cs'


        self.series = self.name[0].lower()

        self.fluence = fluence_dict[int(self.name[2])]  #Fluence in n/ cm^2
        self.t_irr = t_irr_dict[int(self.name[2])]      #irradiation time in mins



        with open(fname, 'rb') as spec_f:
            for ind, line in enumerate(spec_f):
                if done:
                    pass

                elif ind == 7:
                    self.date = line[:10]                   #Extract date XX/XX/XXXX
                    self.time = line[11:]                   #Extract time XX:XX:XX

                elif ind == 9:
                    self.ti_el = line[:3]                    #Extract time elapsed (Seconds)

                elif ind == 11:
                    self.n_ent = line [2:]                   #Exract number of entries

                elif line.strip() == '$ROI:':
                    done = True                              #Trigger at the end of spectrum data

                elif ind > 11:
                    self.spec.append(int(line.strip()))      #Add data





def test_spec():
    script_dir = os.path.dirname(__file__)
    rel_path = 'CSeriesRawData/C_0_1.Spe'
    abs_file_path = os.path.join(script_dir, rel_path)
    spec = spectrum(fname = abs_file_path)



if __name__ =='__main__':
    test_spec()

