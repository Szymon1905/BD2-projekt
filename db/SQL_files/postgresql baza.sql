

select version();
SHOW data_directory;

SELECT * FROM information_schema.columns
WHERE table_schema = 'public'
   AND table_name   = 'accounts';

-- work
SELECT ACC.account_id, ACC.nick, ACC.password, acc_t.account_type
FROM accounts ACC
INNER JOIN account_types acc_t
ON ACC.account_type_id = acc_t.account_type_id
order by account_id;

DELETE from accounts where accounts.nick like 'test';

UPDATE MOVIES
SET movie_title = value1,
    description = value2,
    account_type_id = value,
    genre = value,
WHERE movie_title LIKE var;

INSERT INTO movies (movie_id, movie_title, account_type_id, description, genre_id) VALUES
(nextval('movie_id_seq'), 'PSI patrol', 2, ' A powerful film about death row, hope, and redemption.', 3);

DELETE FROM MOVIES where movie_title LIKE 'SAW';


SELECT Mo.movie_title, Ge.genre_name, At.account_type FROM movies Mo
                                       INNER JOIN genres Ge ON Ge.genre_id = Mo.genre_id 
                                       INNER JOIN account_types At ON At.account_type_id = Mo.account_type_id 
                                       WHERE Mo.account_type_id = 3
                                       ORDER BY Mo.account_type_id;
									   
SELECT Mo.movie_title, Ge.genre_name, acc_t.account_type
                FROM movies Mo
                INNER JOIN account_types acc_t ON Mo.account_type_id = acc_t.account_type_id 
                INNER JOIN genres Ge ON Mo.genre_id = Ge.genre_id 
                WHERE Mo.account_type_id = 2
                ORDER BY Mo.account_type_id;								   
									   


query:   UPDATE MOVIES
                    SET
                      movie_title = 'SAW 3', description = '', account_type_id = 3, genre_id = 0 WHERE movie_title LIKE 'SAW';

-- work





drop table if exists account_types, accounts, genres, movies;
drop sequence if exists account_id_seq, accounts_account_id_seq,genres_id_seqta,movie_id_seq;
--drop sequence if exists ;


-- typy kont
CREATE TABLE IF NOT EXISTS account_types (
  account_type_id INT PRIMARY KEY,
  account_type VARCHAR(50) NOT NULL
);

INSERT INTO account_types (account_type, account_type_id) VALUES
('Admin',1),
('Bronze',2),
('Silver',3),
('Gold',4);



-- konta
CREATE TABLE IF NOT EXISTS accounts (
    account_id INT PRIMARY KEY,
	nick VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ) NOT NULL,
	account_type_id INT REFERENCES
	account_types(account_type_id) NOT NULL
);

ALTER TABLE accounts
ADD CONSTRAINT password_check_length
CHECK (length(password) > 3);

ALTER TABLE accounts
ADD CONSTRAINT nick_check_length
CHECK (length(nick) > 3);


ALTER TABLE accounts
ALTER COLUMN password set not null;

ALTER TABLE movies
ADD CONSTRAINT movie_title_unique UNIQUE (movie_title);

-- ALTER TABLE Konta DROP CONSTRAINT hasło_check_dlugosc;

--sekwencja do dodawania filmow
CREATE SEQUENCE Account_ID_seq
    START WITH 3
	OWNED BY accounts.account_id
    INCREMENT BY 1;

INSERT INTO accounts (account_id, nick, password, account_type_id) VALUES
(1,'Kasia_Matuszek','I_love_Touhou',1),
(2,'Szymon_Borzdynski','I_love_Factorio',1);

INSERT INTO accounts (account_id, nick, password, account_type_id) VALUES
(nextval('account_id_seq'),'admin','admin',1);

--gatunki filmow
CREATE TABLE IF NOT EXISTS genres (
  genre_id INT PRIMARY KEY,
  genre_name VARCHAR(50) NOT NULL
);

INSERT INTO genres (genre_name, genre_id ) VALUES
('horror',1),
('akcji',2),
('dokumentalny',3),
('komedia',4);

CREATE SEQUENCE genres_id_seq
    START WITH 5
	OWNED BY genres.genre_id
    INCREMENT BY 1;



--filmy
CREATE TABLE IF NOT EXISTS movies (
  movie_id INT PRIMARY KEY,
  movie_title VARCHAR(50) NOT NULL,
  description TEXT,
  genre_id INT REFERENCES genres(genre_id),
  account_type_id INT NOT NULL
);




SELECT Mo.movie_title, Ge.genre_name, acc_t.account_type
FROM movies Mo
INNER JOIN account_types acc_t ON Mo.account_type_id = acc_t.account_type_id 
INNER JOIN genres Ge ON Mo.genre_id = Ge.genre_id order by Mo.account_type_id;


INSERT INTO movies (movie_id, movie_title, account_type_id, description, genre_id) VALUES
(1, 'Zielona Mila', 2, ' A powerful film about death row, hope, and redemption.', 3),
(2, '12 gniewnych ludzi', 2, 'A gripping courtroom drama with a focus on the power of deliberation.', 3),
(3, 'Avengers', 2, 'A blockbuster superhero ensemble, uniting iconic Marvel characters to save the world.', 2),
(4, 'Seven', 3, 'A dark and suspenseful thriller that explores the seven deadly sins.', 1),
(5, 'Mission Impossible', 3, 'An action-packed spy series starring Tom Cruise and known for its thrilling stunts.', 2),
(6, 'Oppenheimer', 4, 'A historical drama shedding light on the life of J. Robert Oppenheimer and the atomic bomb.', 2),
(7, 'SAW', 4, 'A family-friendly movie series featuring the adventures of the iconic Barbie doll.', 1);

INSERT INTO movies (movie_id, movie_title, account_type_id, description, genre_id) VALUES


--sekwencja do dodawania filmow
CREATE SEQUENCE movie_id_seq
    START WITH 8
	OWNED BY movies.movie_id
    INCREMENT BY 1;

SELECT nextval('movie_id_seq');


/*
-- przykładowe query
SELECT F.tytul_filmu, F.id_filmu, t.typ_konta
FROM Filmy F 
INNER JOIN Typy_kont t ON F.id_typu_konta = t.id_typu_konta
WHERE t.typ_konta LIKE 'Bronze' OR t.typ_konta LIKE 'Silver'
ORDER BY t.typ_konta;


SELECT F.tytul_filmu, F.id_filmu, t.typ_konta, g.nazwa_gatunku
FROM Filmy F 
INNER JOIN Typy_kont t ON F.id_typu_konta = t.id_typu_konta
INNER JOIN gatunki_filmow g ON F.id_gatunku = F.id_gatunku
WHERE t.typ_konta LIKE 'Bronze' OR t.typ_konta LIKE 'Silver'
ORDER BY t.typ_konta;




--inne przykładowe query do aplikacji
UPDATE Typy_kont  SET typ_konta = 'Silver' where typ_konta LIKE 'silver';

SELECT F.tytul_filmu, F.id_filmu, t.typ_konta, F.gatunek
FROM filmy F
INNER JOIN Typy_kont t ON F.id_typu_konta = t.id_typu_konta order by tytul_filmu;

UPDATE Konta
SET nazwa = 'Kasia_Matuszek'
WHERE id_konta = 1;

SELECT K.nazwa, K.hasło, t.typ_konta
FROM Konta K
INNER JOIN Typy_kont t ON K.id_typu_konta = t.id_typu order by id_konta;


INSERT INTO filmy (id_filmu, tytul_filmu, id_typu_konta,opis) VALUES
(nextval('id_filmow'),'the room',4,'opis filmu the room');


*/

UPDATE MOVIES
                    SET
                      movie_title = 'SAW 3', description = '', required_account_type = 3, genre_id = 0 WHERE movie_title LIKE 'SAW'