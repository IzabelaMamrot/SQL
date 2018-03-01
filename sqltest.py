import sqlite3

con = sqlite3.connect('test.db')
con.row_factory = sqlite3.Row #wywolanie po nazwie zamias po id
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS klasa;")
cur.execute("""
    CREATE TABLE IF NOT EXISTS klasa (
        id INTEGER PRIMARY KEY ASC,
        nazwa varchar(250) NOT NULL,
        profil varchar(250) DEFAULT ''
    )""")
#PRIMARY KEY niepowtarzalny n, do powiazan
#ASC sortuje od najmniejszego do najwieksz. DSC sortuje od najwiekszego do najmniejszego
#NOT NULL - nie moze byc pusta
#DEFAULT ' '  - jesli nic nie wypisszemy, to jakby w 'human' to automatycznie nam to wpisze, a jesli nic to zostawi puste

cur.executescript("""
    DROP TABLE IF EXISTS uczen;
    CREATE TABLE IF NOT EXISTS uczen (
        id INTEGER PRIMARY KEY ASC,
        imie varchar(250) NOT NULL,
        nazwisko varchar(250) NOT NULL,
        klasa_id INTEGER NOT NULL,
        FOREIGN KEY(klasa_id) REFERENCES klasa(id)
    )""")
#DROP usuwa jesli istnieje
#CREATE tworzy na nowo
#FOREIGN KEY(klasa_id) REFERENCES klasa(id) tworzy relacje 1 do wielu
#do jedej klasy klasa_id moze byc przypisane wiele ucznio, o tym samym nr ID


# wstawiamy jeden rekord danych
cur.execute('INSERT INTO klasa VALUES(NULL, ?, ?);', ('1A', 'matematyczny'))
cur.execute('INSERT INTO klasa VALUES(NULL, ?, ?);', ('1B', 'humanistyczny'))

# wykonujemy zapytanie SQL, ktore pobierze id klasy "1A" z tabeli "klasa".
cur.execute('SELECT id FROM klasa WHERE nazwa = ?', ('1A',))
klasa_id = cur.fetchone()[0]  #[0] przypisujemy tylko id do klasa_id, jak byloby bez [0] do 
						#przypisaloby nam do klasa_id - id,nazwe,profil

#jak jest "?" zawsze tworzymy tuple ","

# tupla "uczniowie" zawiera tuple z danymi poszczegolnych uczniow
uczniowie = (
    (None, 'Tomasz', 'Nowak', klasa_id),
    (None, 'Jan', 'Kos', klasa_id),
    (None, 'Piotr', 'Kowalski', klasa_id)
) #None uzywa sie do tupli, tworzymy zmienna do ktorej przypisujemy dane

# wstawiamy wiele rekordow
cur.executemany('INSERT INTO uczen VALUES(?,?,?,?)', uczniowie)

# zatwierdzamy zmiany w bazie
con.commit()

def czytajdane():
    cur.execute(
        """
        SELECT uczen.id,imie,nazwisko,nazwa FROM uczen,klasa
        WHERE uczen.klasa_id=klasa.id
        """)
#Wypisze wszytkie info o uczniach ktorzy sa w klasie 1A
    uczniowie = cur.fetchall() #zapisuje wszyttko z selekta
    for uczen in uczniowie:
        print(uczen['id'], uczen['imie'], uczen['nazwisko'], uczen['nazwa'])
    print()
    
# zmiana klasy ucznia o identyfikatorze 2
cur.execute('SELECT id FROM klasa WHERE nazwa = ?', ('1B',))
klasa_id = cur.fetchone()[0]
cur.execute('UPDATE uczen SET klasa_id=? WHERE id=?', (klasa_id, 2))

# usuniecie ucznia o identyfikatorze 3
cur.execute('DELETE FROM uczen WHERE id=?', (3,))

czytajdane()