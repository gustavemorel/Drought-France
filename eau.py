import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.dates import DateFormatter

datedebut='2012-01-01' ; datefin=str(datetime.now())[:10]

url = "https://eau.api.agriculture.gouv.fr/apis/propluvia/statistiques/pctEvolutionJournaliereSurfaceParRestrictionCSV?=&dateDebut="+datedebut+"&dateFin="+datefin+"&typeEau=SUP&typeTerritoire=MET&codeTerritoire=undefined&fileName=EVOL_JOUR_SURFACE_PAR_RESTRICTION.csv"
data = pd.read_csv(url, encoding='latin-1')

date=[datetime.strptime(str(x), '%d/%m/%Y') for x in data[:]['Période']]
crise=[float(x) for x in data[:]['Pourcentage surface Crise']]
renforcee=[float(x) for x in data[:]['Pourcentage surface Alerte renforcée']]
alerte=[float(x) for x in data[:]['Pourcentage surface Alerte']]
total=[(x+y+z)/100 for (x,y,z) in zip(crise,renforcee,alerte)]

fig, ax = plt.subplots()
limin=0 ; limax=0
for year in range(2012,2023):
    for i in range(len(date)) :
        if date[i].year == year :
            limax=i
            date[i]=date[i].replace(year=2000) #pour superposer les années
    if year!=2022 : ax.plot(date[limin+1:limax+1],total[limin+1:limax+1],label=str(year),lw=2)
    if year==2022 : ax.plot(date[limin+1:limax+1],total[limin+1:limax+1],label=str(year),lw=3,color='k')
    limin=limax
    
myFmt = DateFormatter("%d/%m")
ax.xaxis.set_major_formatter(myFmt)
fig.autofmt_xdate()
plt.legend() ; plt.grid()
plt.title('Eaux superficielles - pourcentage de la France en Alerte/Alerte renforcée/Crise')
#plt.savefig('secheresse.png',bbox_inches='tight')
plt.gca().set_yticklabels([f'{x:.0%}' for x in plt.gca().get_yticks()])
plt.xlim(left=date[0].replace(day=1,month=4),right=date[0].replace(day=15,month=10))
plt.show()
