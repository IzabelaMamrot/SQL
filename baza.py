import sqlite3

con=sqlite3.connect('baza.db')
con.row_factory = sqlite3.Row 
cur = con.cursor()
def tworzenie_tabel():
	cur.execute("DROP TABLE IF EXISTS Klienci;")
	cur.execute("DROP TABLE IF EXISTS Faktury;")
	cur.execute("DROP TABLE IF EXISTS Miasta;")
	cur.execute("DROP TABLE IF EXISTS Grupy_klientow;")

	cur.execute("""CREATE TABLE IF NOT EXISTS Klienci(
				ref INTEGER PRIMARY KEY ASC,
				nazwa text,
				miasto text,
				grupaklienta text,
				foreign key(miasto) references Miasta(nazwa),
				foreign key(grupaklienta) references Grupy_klientow(symbol)
				)""")
				
	cur.execute("""CREATE TABLE IF NOT EXISTS Faktury(
				ref integer primary key,
				symbol text,
				data text,
				klient integer,
				brutto float,
				rabat float,
				foreign key(klient) references Klienci(ref)
				)""")
	cur.execute("""CREATE TABLE IF NOT EXISTS Miasta(
				nazwa text primary key,
				liczba_mieszkancow text
				)""")
	cur.execute("""CREATE TABLE IF NOT EXISTS Grupy_klientow(
				symbol text primary key,
				nazwa_grupy text,
				domyslny_rabat float
				)""")
def add_klienci():
	klient = (
			(12374, "Lineks Sp. z o.o.", "KRAKOW", "VIP"),
			(12375, "Barton sp. j.", "WROCLAW", "HURT"),
			(12376, "Multisys S.A", "WROCLAW", "HURT"),
			(12377, "Dantona Sp. z o.o.", "WROCLAW", "HURT"),
			(12378, "Erfur Sp. z o.o.", "WROCLAW", "DETAL"),
			(12379, "Aninaret sp. j.", "KRAKOW", "DETAL"),
			(12380, "Gravix sp. j.", "WARSZAWA", "DETAL"),
			(12381, "Hutawon sp. z o.o.", "WARSZAWA", "DETAL"),
			(12382, "Irys sp. z o.o.", "LADEK", "DETAL")	
		)
	cur.executemany("INSERT INTO Klienci VALUES(?,?,?,?);", klient)
	con.commit()
def add_faktury():
	faktura = (
		(None, "F/1/09/12", "1.09.2012", 12374, 18450.00, 15.00),
		(None, "F/2/09/12", "1.09.2012", 12374, 30750.00, 15.00),
		(None, "F/3/09/12", "5.09.2012", 12374, 184.50, 10.00),
		(None, "F/4/09/12", "5.09.2012", 12375, 6150.00, 5.00),
		(None, "F/5/09/12", "6.09.2012", 12375, 5289.00, 5.00),
		(None, "F/6/09/12", "7.09.2012", 12376, 664.20, 0.00),
		(None, "F/7/09/12", "8.09.2012", 12377, 1230.00, 5.00),
		(None, "F/1/10/12", "1.10.2012", 12378, 984.00, 5.00),
		(None, "F/1/10/12", "1.10.2012", 12374, 9827.70, 5.00)
		)
	cur.executemany("INSERT INTO Faktury VALUES(?,?,?,?,?,?);", faktura)
	con.commit()

def add_miasta():
	miasta = (
		("WROCLAW", "1mln"),
		("LADEK", "100tys"),
		("KRAKOW", "1mln"),
		("WARSZAWA", "2mln")
		)
	cur.executemany("INSERT INTO Miasta VALUES(?,?);", miasta)
	con.commit()
	
def add_grupa():
	grupy = (
		("HURT", "Hurtownicy", 5.00),
		("DETAL", "Detalisci", 0.00),
		("VIP", "Kluczowi klienci", 10.00)
		)
	cur.executemany("INSERT INTO Grupy_klientow VALUES(?,?,?);", grupy)
	con.commit()
	
def kwerenda():
	cur.execute("SELECT * FROM Klienci")
	klienci = cur.fetchall()
	for i in klienci:
		print (
			i ['nazwa']
			)
#1
def sortowanie():
	print("sortowanie")
	cur.execute("SELECT ref FROM Klienci EXCEPT SELECT klient FROM Faktury ORDER BY ref ASC")
	
	klienci = cur.fetchall()
	for i in klienci:
		cur.execute("SELECT nazwa FROM Klienci WHERE ref = ?",(i))
		seg=cur.fetchall()
		for i in seg:
			print (i ['nazwa'])
		
#2
def top3():
	print ("TOP 3")
	cur.execute("SELECT klient FROM Faktury ORDER BY brutto DESC LIMIT 3")
	top = cur.fetchall()
	for i in top:
		cur.execute("SELECT nazwa FROM Klienci WHERE ref = ?",(i))
		seg = cur.fetchall()
		for i in seg:
			print (i ['nazwa'])
	print()

#3
def wrzesien():
	cur.execute("SELECT * FROM Faktury WHERE data like '%.09%'")
	klienci = cur.fetchall()
	for i in klienci:
		cur.execute("SELECT grupaklienta FROM Klienci WHERE grupaklienta like '%T%'")
		seg = cur.fetchall()
		for i in seg:
			print(
				i['grupaklienta']
				)
#4		
def poczatek_A():
	cur.execute("SELECT * FROM Klienci WHERE nazwa like 'A%'")
	klienci = cur.fetchall()
	for i in klienci:
		print (
			i ['nazwa']
			)
			
def koniec_A():
	cur.execute("SELECT * FROM Klienci WHERE nazwa like '% A'")
	klienci = cur.fetchall()
	for i in klienci:
		print (
			i ['nazwa']
			)	
#5			
def wieksza_niz():
	print ("Faktury na wiecej niz 25k")
	lista_klientow = []
	cur.execute("SELECT ref FROM Klienci")
	idklienta = cur.fetchall()
	for i in idklienta:
		cur.execute("SELECT SUM (brutto) FROM Faktury WHERE Klient = ?", (i))
		seg = cur.fetchall()
		for i in seg:
			if (i[0] != None and i[0]>25000):
				lista_klientow.append(i[0])
	print ("Liczba klientow ktora wydala wiecej niz 25000: ", (len(lista_klientow)))
	print()

#6
def detal():
	cur.execute("SELECT ref FROM Klienci WHERE grupaklienta = ?", ("DETAL",))
	klienci = cur.fetchall()
	cur.execute("SELECT domyslny_rabat FROM Grupy_klientow WHERE symbol = ?", ("DETAL",))
	domyslny = cur.fetchone()[0]
	for i in klienci:
		cur.execute("SELECT symbol,data,brutto,rabat FROM Faktury WHERE klient = ?", (i))
		seg = cur.fetchall()
		for i in seg:			
			print (
				i ['symbol'],
				i ['data'],
				i ['brutto'], end =' ')
			if (i ['rabat'] == domyslny):
				print ("zgodny")
			else:
				print("niezgodny")
				
#7
def zestawienie():
	cur.execute("SELECT brutto FROM Faktury WHERE data like '%.09%'")
	klienci = cur.fetchall()

	for i in klienci:
		print (
			i [0], end = ' '
			)
		if (i ['brutto'] > 4900):
			print ("V")
		else:
			print("S")
	print()
#8
def najwiecej():
	cur.execute("SELECT * FROM Klienci")
	klienci = cur.fetchall()
	cur.execute("SELECT brutto FROM Faktury")
	for i in klienci:
		#print(
		#	i['miasto']
		#	)
		
		#cur.execute("SELECT SUM (brutto) FROM Faktury")
		seg = cur.fetchall()
		for i in seg:
			print(
				i['brutto']
				)
		
#9
	
def analiza():
	print ("Analiza klientow")
	lista_klientow = []
	id_klientow = []
	cur.execute("SELECT ref FROM Klienci")
	idklienta = cur.fetchall()
	for i in idklienta:
		cur.execute("SELECT Klient FROM Faktury WHERE Klient = ?", (i))
		idk = cur.fetchall()
		for i in idk:
			id_klientow.append(i[0])
		cur.execute("SELECT SUM (brutto) FROM Faktury WHERE Klient = ?", (i))
		seg = cur.fetchall()
		for i in seg:
			if (i[0] != None):
				lista_klientow.append(i[0])
	print(lista_klientow)
	print(id_klientow)
			
tworzenie_tabel()
add_grupa()
add_miasta()
add_klienci()
add_faktury()
#kwerenda()

sortowanie()
top3()
wrzesien()
poczatek_A()
koniec_A()
wieksza_niz()
detal()
zestawienie()
najwiecej()
analiza()
#print("0 - WYJSCIE")
#print("1 - SORTUJ KLIENTOW BEZ FAKTURY")
#print("2 - TOP3 KLIENTOW KTORZY KUPILI TOWARY ZA NAJWYZSZA KWOTE")
#print("3")
#print("4")
#print("5")
#print("6")
#print("7")
#print("8")
#print("9")
#x=int(input())
#while True:
#	if x==0:
#		break
#	elif x==1:
#		pass
#	elif x==2:
#		pass
#	elif x==3:
#		pass
#	elif x==4:
#		pass
#	elif x==5:
#		pass
#	elif x==6:
#		pass
#	else:
#		print("Nie ma takiej komendy")

#menu=input("")
		