import csv
import urllib.request
import io

def print_stat (libelle, row_i):
    if row_i > 0:
        for i in range (1, 14):
            value = data[row_i][i]
            if value == '.':
                value = '0'
            if value == '-':
                value =''
            print (f'|{libelle}-{mois_libelles[i]}={value}')

def print_stat_record (libelle, row_i):
    if row_i > 0:
        for i in range (1, 14):
            print (f'|{libelle}-{mois_libelles[i]}={data[row_i][i]} | {libelle}-date-{mois_libelles[i]}={data[row_i+1][i].replace("-",".")}')

def next_data_row_i (row_i):
    next_i = row_i+1
    while data[next_i][0] != '':
        if 'non disponible' in data[next_i][0]:
            return 0
        next_i += 1
    return next_i

data = []
mois_libelles = ['', 'jan', 'fev', 'mar', 'avr', 'mai', 'jui', 'jul', 'aou', 'sep', 'oct', 'nov', 'dec', 'ann']

fiche_id = '35281001'
fiche_url = f'https://donneespubliques.meteofrance.fr/FichesClim/FICHECLIM_{fiche_id}.data'

ficheclim = urllib.request.urlopen(fiche_url).read()
meteodatastr = ficheclim.decode('utf-8')
with io.StringIO(meteodatastr) as meteodata:
    reader = csv.reader(meteodata, delimiter=';', skipinitialspace=True)
    for row in reader:
        data.append(row)

row_i= TMax_i = TMin_i = TMoy_i = TRecMax_i = TRecMin_i = DIns_i = Brouillard_i = Orage_i = Grele_i = Neige_i = Rr1_i = Rr5_i = Rr10_i = PMoy_i = 0
for row in data:
    if len(row) > 0:
        if ('maximale (Moyenne en' in row[0]):
            TMax_i = next_data_row_i (row_i)
        if ('minimale (Moyenne en' in row[0]):
            TMin_i = next_data_row_i (row_i)
        if ('moyenne (Moyenne en' in row[0]):
            TMoy_i = next_data_row_i (row_i)
        if ('Hauteur moyenne mensuelle' in row[0]):
            PMoy_i = next_data_row_i (row_i)
        if ('température la plus élevée' in row[0]):
            TRecMax_i = next_data_row_i (row_i)
        if ('température la plus basse' in row[0]):
            TRecMin_i = next_data_row_i (row_i)
        if ("Durée d'insolation" in row[0]):
            DIns_i = next_data_row_i (row_i)
        if ("Brouillard" in row[0]):
            Brouillard_i = row_i
        if ("Orage" in row[0]):
            Orage_i = row_i
        if ("Grêle" in row[0]):
            Grele_i = row_i
        if ("Neige" in row[0]):
            Neige_i = row_i
        if ("Rr >=  1 mm" in row[0]):
            Rr1_i = row_i
        if ("Rr >=  5 mm" in row[0]):
            Rr5_i = row_i
        if ("Rr >= 10 mm" in row[0]):
            Rr10_i = row_i

    row_i += 1

print ('{{Climat')
print (f'|titre={data[2][0]} {data[3][0]}')
print (f'|source={{{{Lien Web|url={fiche_url.replace("data","pdf")}|titre=Fiche {fiche_id}|site=donneespubliques.meteofrance.fr|date={data[4][0]}|id=MétéoFrance {fiche_id}|libellé=MétéoFrance}}}}')

print_stat ('tmin', TMin_i)
print_stat ('tmoy', TMoy_i)
print_stat ('tmax', TMax_i)
print_stat ('prec', PMoy_i)
print_stat_record ('tmax-record', TRecMax_i)
print_stat_record ('tmin-record', TRecMin_i)
print_stat ('soleil', DIns_i)
print_stat ('orage-jour', Orage_i)
print_stat ('neige-jour', Neige_i)
print_stat ('brouillard-jour', Brouillard_i)
print_stat ('grêle-jour', Grele_i)
print_stat ('pluie-jour+1mm', Rr1_i)
print_stat ('pluie-jour+5mm', Rr5_i)
print_stat ('pluie-jour+10mm', Rr10_i)

print ('}}')


print (f'{{{{Météo France|')
print (f'|Ville=<a compléter>')
if DIns_i > 0 and data[DIns_i][13] != '-': print (f'|SoleilVille={int(round(float(data[DIns_i][13])))}')
if PMoy_i > 0 and data[PMoy_i][13] != '-': print (f'|PluieVille={int(round(float(data[PMoy_i][13])))}')
if Neige_i > 0 and data[Neige_i][13] != '-': print (f'|NeigeVille={int(round(float(data[Neige_i][13])))}')
if Orage_i > 0 and data[Orage_i][13] != '-': print (f'|OrageVille={int(round(float(data[Orage_i][13])))}')
if Brouillard_i > 0 and data[Brouillard_i][13] != '-': print (f'|BrouillardVille={int(round(float(data[Brouillard_i][13])))}')
print (f'}}}}')
