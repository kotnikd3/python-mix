
# v Windows OS je najbrz potrebno namesto Tkinter napisati tkinter
from Tkinter import *

r = 10
class Grafi():
    def __init__(self, master):
        # Spremenljivka, v katero bomo shranjevali trenutno izbrano povezavo, da lahko kasneje pridobimo koordinate iz nje
        self.trenutna = None
		# Bool, ki pove, ali se trenutna povezava rise
        self.risem = False
		# Seznam povezav
        self.povezave = []
		# Slovar v obliki {vozlisce : [povezave]}
        self.graf = {}

#MENIJI
        #Glavni meni
        menu = Menu(master)
        master.config(menu=menu)#glavnemu oknu nastavimo menu

        #Naredimo podmenu Risalnik
        risalni_menu = Menu(menu, tearoff = 0)
        menu.add_cascade(label = "Risalnik", menu = risalni_menu)

        
        #Dodamo izbire v podmenu Risalnik
        risalni_menu.add_command(label = "Koncaj", command = master.destroy)
        #risalni_menu.add_command(label = "Pocisti", command = self.izbrisiVozlisca)

		#gumbi - izbire
        gumbi = Frame(master)
        gumbi.grid(row = 0, column = 1)

        gumb_euler = Button(gumbi, text = "Ali je graf Eulerjev?", command = self.jeEulerjev)
        gumb_euler.grid(row = 0, column = 0)#manjka command

        gumb_pobrisi = Button(gumbi, text = "Pobrisi graf", command = self.pobrisiGraf)
        gumb_pobrisi.grid(row = 0, column = 1)#manjka command

        self.izpisEuler = Label(master, text = "???")
        self.izpisEuler.grid(row = 1, column = 1)
		
#podrocje za risanje
        risalna_povrsina = Frame(master)
        risalna_povrsina.grid(row = 2, column = 1)
        
        self.canvas = Canvas(risalna_povrsina, width = 500, height = 500)
        self.canvas.grid(row = 0, column = 0)


#kliki miske in tipke
        self.canvas.bind("<Button-1>", self.pritisniMiskinGumb)

	# Metoda ustvari vozlisce (ce kliknemo na postor, kjer se ni vozlisca) ali ustvari povezavo (ce drzimo miskin gumb in potegnemo na drugo vozlisce)
    def pritisniMiskinGumb(self, event):
        self.canvas.bind("<B1-Motion>", self.ignoriraj)
        self.canvas.bind("<ButtonRelease-1>", self.ignoriraj)
		# Na zacetku se povezave ne rise
        self.risem = False

		# Preverimo, ali smo kliknili na vozlisce.
        morebitnoVozlisce = self.canvas.find_overlapping(event.x-r, event.y-r,event.x+r,event.y+r)
		
		# Ce ne, ga ustvarimo
        if len(morebitnoVozlisce) == 0:
            vozlisce = self.canvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r,fill = "red")
     		# Dodaj vozlisce
            self.graf[vozlisce] = []
        else: # Drugace vezemo premikanje miske na metodo premikajMisko. V morebitnoVozlisce[0] je pac vozlisce, na katerega smo kliknili.
            self.canvas.bind("<B1-Motion>", lambda event, zacetnoVozlisce = morebitnoVozlisce[0]: self.premikajMisko(event, zacetnoVozlisce))

	# Metoda je zadolzena za ustvarjanje povezave
    def premikajMisko(self, event, zacetnoVozlisce):
		# Na zacetku se povezave ne rise
       if not self.risem:
           self.trenutna = self.canvas.create_line(self.canvas.coords(zacetnoVozlisce)[0]+r, self.canvas.coords(zacetnoVozlisce)[1]+r, self.canvas.coords(zacetnoVozlisce)[2]-r, self.canvas.coords(zacetnoVozlisce)[3]-r, fill="blue")
           # Ko se ustvari en konec povezave, se spreminjajo le koordinate njenega drugega konca
           self.risem = True
       else: # Ko se ustvari en konec povezave, se spreminjajo le koordinate njenega drugega konca
           self.canvas.coords(self.trenutna, self.canvas.coords(self.trenutna)[0], self.canvas.coords(self.trenutna)[1], event.x, event.y)
       # Nato se veze akcijo izpusti miskin gumb na metodo izpustiMiskinGumb
       self.canvas.bind("<ButtonRelease-1>", lambda event, zacetnoVozlisce = zacetnoVozlisce: self.izpustiMiskinGumb(event, zacetnoVozlisce))

	# Metoda je zadolzena za ustvarjanje povezave - za dokoncanje.
    def izpustiMiskinGumb(self, event, zacetnoVozlisce):
	    # Preverimo, ali smo povlekli na vozlisce.
        morebitnoVozlisce = self.canvas.find_overlapping(event.x-r, event.y-r,event.x+r,event.y+r)
        
        if len(morebitnoVozlisce) == 1: # ce ni nobenega, ne ustvari povezave - jo izbrisi
            self.canvas.delete(self.trenutna)
        else: # ce ne, jo ustvari. koordinate konca povezave pridobi iz vozlisca, na katerega smo povlekli misko
            self.canvas.coords(self.trenutna, self.canvas.coords(self.trenutna)[0], self.canvas.coords(self.trenutna)[1], self.canvas.coords(morebitnoVozlisce[0])[0]+r, self.canvas.coords(morebitnoVozlisce[0])[1]+r)
            # povezavod dodaj
            self.graf[zacetnoVozlisce].append(morebitnoVozlisce[0])
            self.graf[morebitnoVozlisce[0]].append(zacetnoVozlisce)
            self.povezave.append(self.trenutna)
        print("GRAF: ", self.graf)
        self.trenutna = None

    def ignoriraj(self, event):
        pass

    def pobrisiGraf(self):
        # Pobrisemo vozlisca
        for vozlisce in self.graf:
           self.canvas.delete(vozlisce)

		# Pobrisemo povezave
        for povezava in self.povezave:
           self.canvas.delete(povezava)

        self.povezave = []
        self.graf.clear()
        self.izpisEuler['text'] = "???"

    def jeEulerjev(self):
        if len(self.graf) == 0:
            self.izpisEuler['text'] = "Grafa NI!"
            return None

        eulerjev = True
        prazen = True

		# Naprej preverimo, ali je graf prazen
        for vozlisce in self.graf:
            if len(self.graf[vozlisce]) != 0:
                prazen = False
                break
        if prazen:
             self.izpisEuler['text'] = "Graf JE prazen!."
             return None

		# Nato preverimo sodost vozlisc
        for vozlisce in self.graf:
            if len(self.graf[vozlisce]) % 2 != 0:
                eulerjev = False
                break

        if eulerjev:
            self.izpisEuler['text'] = "Graf JE eulerjev."
        else:
            self.izpisEuler['text'] = "Graf NI eulerjev."


# Glavnemu oknu recemo "root" (koren), ker so graficni elementi
# organizirani v drevo, glavno okno pa je koren tega drevesa

# Naredimo glavno okno
root = Tk()

aplikacija = Grafi(root)

# Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
# delovati, ko okno zapremo.
root.mainloop()

