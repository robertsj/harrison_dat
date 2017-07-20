import csv

mean_j = {}
mean_c = {}
dev_j = {}
dev_c = {}
max_j = {}
max_c = {}
min_j = {}
min_c = {}

cnt = 0
with open('cent_dat.csv') as fle:
    reader = csv.reader(fle)
    for ind, row in enumerate(reader):
        if ind >= 119:
            line = [it.strip() for it in row]


            line = filter(None, line)

            if line[0].strip().lower() == 'mean':
                mean_c[cnt] = (float(line[1]), float(line[2]), float(line[3].replace("%","")))
                mean_j[cnt] = (float(line[5]), float(line[6]), float(line[7].replace("%","")))

            if line[0].strip().lower() == 'std dev':
                dev_c[cnt] = (float(line[1]), float(line[2]), float(line[3].replace("%","")))
                dev_j[cnt] = (float(line[5]), float(line[6]), float(line[7].replace("%","")))

            if line[0].strip().lower() == 'max':
                max_c[cnt] = (float(line[1]), float(line[2]), float(line[3].replace("%","")))
                max_j[cnt] = (float(line[5]), float(line[6]), float(line[7].replace("%","")))

                print line

            if line[0].strip().lower() == 'min':
                min_c[cnt] = (float(line[1]), float(line[2]), float(line[3].replace("%","")))
                min_j[cnt] = (float(line[5]), float(line[6]), float(line[7].replace("%","")))


                print line
                cnt += 1


tli = [mean_j, mean_c, dev_j, dev_c, max_j, max_c, min_j, min_c]

for it in tli:
    print it