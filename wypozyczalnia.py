import sqlite3
import sys

print("Baza filmow \n","Wybierz opcje \n","1 - Dodaj nowy film \n", "2 - Usun nowy film \n", "3 - Pokaz wszystkie filmy \n", "4 - Znajdz film po roku \n", "5 - Wyjscie \n")
x=int(input())

def create_film_table(): #funkcja - musza byc wartosci
	with sqlite3.connect('wypozycz.db') as db:
		c=db.cursor()
	#tworzenie tablicy
		c.execute("""
			CREATE TABLE Film(
			FilmID integer,
			Tytul text,
			Typ real,
			Rok integer,
			Primary Key(FilmID)); """)
		db.commit() #zmiany
#create_film_table()

def insert_records(values):
	with sqlite3.connect('wypozycz.db') as db:
		c=db.cursor()
		sql = """INSERT INTO Film (Tytul, Typ, Rok)
		          VALUES(?,?,?)"""
		c.execute(sql,values)
		db.commit()
film1=("Minionki","Bajka", 2014)
#insert_records(film1)

def select_all_films():
	with sqlite3.connect('wypozycz.db') as db:
		c=db.cursor()
		sql="Select * from Film"
		c.execute(sql)
		wynik=c.fetchall() #lista wszytkich wymagania WSZYSTKIE
		print(wynik)


def select_one_film():
	with sqlite3.connect('wypozycz.db') as db:
		c=db.cursor()
		sql="Select * from Film where FilmID = 1"
		c.execute(sql)
		wynik=c.fetchone() #lista wszytk 
		print(wynik)

def select_genre(typ):
	with sqlite3.connect('wypozycz.db') as db:
		c=db.cursor()
		sql="SELECT * FROM Film WHERE typ = ?"
		c.execute(sql,(typ,))
		wynik=c.fetchall()
		return wynik
		
def select_year(rok):
	with sqlite3.connect('wypozycz.db') as db:
		c=db.cursor()
		sql="SELECT * FROM Film WHERE rok = ?"
		c.execute(sql,(rok,))
		wynik=c.fetchall()
		return wynik
		

#wybierz = input("Jaki gatunek filmowy chcesz zobaczyc? \n") 
#films = select_genre(wybierz)
#print(films)

if x==1:
	y=input("Tytul: ")
	yy=input("Typ: ")
	yyy=int(input("Rok: "))
	z=(y,yy,yyy)
	insert_records(z)

#elif x==2:
	
elif x==3:
	select_all_films()

elif x==4:
	rok=int(input("Podaj rok: "))
	select_year(rok)
print(select_year(rok))
	
elif x==5:
	sys.exit()
else:
	print("Nie ma takiej komendy")
#select_one_film()
#select_all_films()
