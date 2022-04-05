import math
import random
#import numpy as np

S=10 #dimensiunea populatiei
left=-1 #domeniul de definitie
right=2
a=-1
b=1
c=2 #coeficientii fitnesului
precision=5
pRecomb=0.25
pMutation=0.01
steps=50
maxiList= []

def BinarySearch(intervalSelectie, valoare):

  low = 0
  high = len(intervalSelectie)

  while low < high:

    mid = math.floor((low + high) / 2)

    if intervalSelectie[mid] == valoare:
      return mid
    elif intervalSelectie[mid] < valoare and mid != low:
      low = mid
    elif intervalSelectie[mid] > valoare and mid != high:
      high = mid
    else:
    # terminate with index pointing to the first element greater than low
      high = low = low + 1

  return low

class Individ:

    def __init__(self,value = None):

        self.a = a
        self.b = b
        self.c = c
        self.pSelectie=0
        self.precision = precision
        self.lenCromozom = math.log2((right - left) * (10 ** precision))

        if self.lenCromozom != int(self.lenCromozom):
            self.lenCromozom = int(self.lenCromozom)+1  #aproximarea la parte intreaga superioara

        if value == None:
            self.value = round(random.uniform(left,right), precision) ###AICI TREBUIE SA VERIFIC CU EXCLUSIV/INCLUSIV

        else:
            self.value = value

        self.fitness = self.a * (self.value * self.value) + (self.b * self.value) + self.c
        #((self.value * self.value) * self.a)

        ##########CODIFICARE
        self.chromosome = ""
        addZero = ""
        x = ""
        nr = round((self.value-left)*(10**self.precision)) #(value-a)*(10^p)
        x = bin(nr)
        x = str(x)
        x = x[2:]  # pentru ca aveam ab01000 etc
        concat = self.lenCromozom - len(x)  # cati de 0 mai am de pus in fata
        while concat > 0:
            addZero = addZero + "0"
            concat -= 1
        self.chromosome = addZero + x

    def calculate_fitness(self):

        if self.value > right:
            self.fitness = 0
        else:
            self.fitness = self.a * (self.value * self.value) + (self.b * self.value) + self.c

    def __repr__(self):
        return f"({self.value},{self.chromosome},{self.fitness})"


def decodify(chromosome):

    p = precision
    power=1
    while p>0:
        power = power * 10
        p-=1
    x = round(int(chromosome, 2)/power+left, precision)
    return x

def obtineIndivid(chromosome):

    val1=decodify(chromosome)
    individ1 = Individ(val1)
    individ1.calculate_fitness()

    return individ1
#daca decodarea da mai mare decat b -> ii dau 0 la fitness

def CrossOver(participaLaRecomb,cromozomiDupaRecombinare):

    if len(participaLaRecomb) == 1 : #daca am un singur cromozom acesta nu se modifica

        i=len(participaLaRecomb)
        print("Cromozomul", participaLaRecomb[0][1], "nu se modifica")

        val1 = decodify(participaLaRecomb[0][0])
        individ1 = Individ(val1)
        individ1.calculate_fitness()
        cromozomiDupaRecombinare.insert(participaLaRecomb[0][1] - 1, individ1)



    elif len(participaLaRecomb) %2 == 1 and len(participaLaRecomb) >1: #il las pe primul in pace si il inserez

        i=1
        val1 = decodify(participaLaRecomb[0][0])
        individ1 = Individ(val1)
        individ1.calculate_fitness()
        cromozomiDupaRecombinare.insert(participaLaRecomb[0][1] - 1, individ1)

    else:
        i=0

    while i<len(participaLaRecomb): #iau cate un tuplu pe rand

        sir1 = ""
        sir2 = ""
        breakPoint = random.randint(0, len(participaLaRecomb[i][0]))

        print("Recombinare dintre cromozomul:", participaLaRecomb[i][1], "cu cromozomul", participaLaRecomb[i+1][1],":")

        for indexGena in range(breakPoint): # primul element din tuplul[i] cu primul element din tuplul[i+1]

            if participaLaRecomb[i][0][indexGena] != participaLaRecomb[i+1][0][indexGena]:

                if participaLaRecomb[i][0][indexGena] == "0":

                    sir1 += "1"
                    sir2 += "0"

                else:

                    sir1 +="0"
                    sir2 += "1"

            else:

                sir1 += participaLaRecomb[i][0][indexGena]
                sir2 += participaLaRecomb[i][0][indexGena]

        sir1 += participaLaRecomb[i][0][breakPoint:]
        sir2 += participaLaRecomb[i+1][0][breakPoint:]

        print(participaLaRecomb[i][0], " ",participaLaRecomb[i+1][0], "punct ", breakPoint)
        print("Rezultat ", sir1, " ",sir2)


        val1 = decodify(sir1)
        val2 = decodify(sir2)
        individ1 =  Individ(val1)
        individ2= Individ(val2)
        individ1.calculate_fitness()
        individ2.calculate_fitness()

        cromozomiDupaRecombinare.insert(participaLaRecomb[i][1] - 1,individ1)
        cromozomiDupaRecombinare.insert(participaLaRecomb[i+1][1] - 1, individ2)

        i=i+2

    return cromozomiDupaRecombinare




print("Populatia initiala: ")
step=1
while step<steps:

    print("Pasul:",step)
    generation = []
    fitnessSum = 0
    if step != 1:

        generation = NextGeneration
        print("La pasul: ", step, "am generatia", generation)
        for individ in NextGeneration:
            fitnessSum += individ.fitness
    else:
        for i in range(S):
            individ = Individ()
            print(i+1,":", individ.chromosome, " x= ", individ.value, " f= ", individ.fitness)
            fitnessSum += individ.fitness
            generation.append(individ)

    print("\nProbabilitati selectie: ")

    i=1
    sumProbabilitati=0
    intervalSelectie=[]

    for individ in generation:

        individ.pSelectie = individ.fitness/fitnessSum
        sumProbabilitati += individ.pSelectie #calculez sumele partiale
        intervalSelectie.append(sumProbabilitati)
        print("cromozom", i, "probabilitate", individ.pSelectie)
        i+=1

    amAdaugatZero=0
    if intervalSelectie[0] != 0:
        amAdaugatZero=1
        intervalSelectie.insert(0,0)

    print("Intervale probabilitati selectie: ")
    print(intervalSelectie)

    dupaSelectie=[]
    for i in range(S):
         u = random.uniform(0,1)
         index = BinarySearch(intervalSelectie,u) # este numarand din 0
         if index == S:
             dupaSelectie.append(generation[index-1])
             print("u=", u, "cromozomul: ", index)
         else:
             dupaSelectie.append(generation[index])
             print("u=",u, "cromozomul: ", index+1)

    print("\nDupa selectie: ")
    i=1
    for individ in dupaSelectie:
        print(i,":",individ.chromosome, "x= ", individ.value,"f= ",individ.fitness)
        i+=1

    print("\nProbabilitatea de incrucisare ",pRecomb)
    i=1
    participaLaRecomb=[]
    cromozomiDupaRecombinare=[]
    for individ in dupaSelectie:
        u = random.uniform(0, 1)
        tuplu=()
        aux = []
        if u<pRecomb:

            print(i,":",individ.chromosome, "u= ", u,"<", pRecomb,"participa")
            aux = [individ.chromosome,i]
            tuplu = tuple(aux)
            participaLaRecomb.append(tuplu) #salvez cromozomii care participa la recombinare

        else:
            print(i,":",individ.chromosome, "u= ", u)
            cromozomiDupaRecombinare.append(dupaSelectie[i-1])
        i+=1

    #participa la recombinare e un tuplu dintre cromozom si index- ul la care se afla

    CromozomiDupaRecombinare = CrossOver(participaLaRecomb,cromozomiDupaRecombinare)

    print("\nDupa recombinare")
    i=1
    for individ in CromozomiDupaRecombinare:
        print(i,":",individ.chromosome, "x= ", individ.value,"f= ",individ.fitness)
        i+=1

    #########################################################

    print(CromozomiDupaRecombinare)

    print("\nProbabilitatea de mutatie pentru fiecare gena ",pMutation)
    print("Au fost modificati cromozomii:")

    CromozomiDupaMutatii=[]

    i=1
    for individ in CromozomiDupaRecombinare:

        sir1 = ""
        modificat = 0
        for indexGena in range(len(individ.chromosome)):

            u = random.uniform(0, 1)

            if u<pMutation:

                modificat = 1
                if individ.chromosome[indexGena] == "0":

                    sir1 += "1"
                else:

                    sir1 += "0"
            else:

                sir1 += individ.chromosome[indexGena]

        val1 = decodify(sir1)
        individ1 = Individ(val1)
        individ1.calculate_fitness()
        CromozomiDupaMutatii.append(individ1)

        if modificat == 1:
            print(i)

        i+=1

    i=1
    maxi = left
    NextGeneration = []

    for individ in CromozomiDupaMutatii:
        print(i,":",individ.chromosome, "x= ", individ.value,"f= ",individ.fitness)

        if individ.fitness > maxi:
            maxi = individ.fitness
        i+=1

    NextGeneration = CromozomiDupaMutatii

    maxiList.append(maxi)
    #print(maxi)
    step +=1

print(maxiList)
#fara element elitist
