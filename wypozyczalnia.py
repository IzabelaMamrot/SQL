import sqlite3

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
select_all_films()

def select_one_film():
	with sqlite3.connect('wypozycz.db') as db:
		c=db.cursor()
		sql="Select * from Film where FilmID = 1"
		c.execute(sql)
		wynik=c.fetchone() #lista wszytk 
		print(wynik)
select_one_film()

def select_genre(typ):
	with sqlite3.connect('wypozycz.db') as db:
		c=db.cursor()
		sql="SELECT * FROM Film WHERE typ = ?"
		c.execute(sql,(typ,))
		wynik=c.fetchall()
		return wynik

wybierz = input("Jaki gatunek filmowy chcesz zobaczyc? \n") 
films = select_genre(wybierz)
print(films)








