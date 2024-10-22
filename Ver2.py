import psycopg2
from psycopg2 import Error

class AlunoDB:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                dbname="student_db",
                user="postgres",     
                password="123456",
                host="localhost",
                port="5432"
            )
            self.cursor = self.connection.cursor()
            self.setup_database()
                
        except Error as e:
            print(f"Erro ao se conectar ao postgreSQL: {e}")
            try:
                
                self.connection = psycopg2.connect(
                    dbname="postgres",
                    user="postgres",
                    password="123456",
                    host="localhost",
                    port="5432"
                )
                self.connection.autocommit = True
                self.cursor = self.connection.cursor()
                self.cursor.execute("CREATE DATABASE student_db")
                self.cursor.close()
                self.connection.close()
                
                # Reconecção para casos de erro
                self.connection = psycopg2.connect(
                    dbname="student_db",
                    user="postgres",
                    password="123456",
                    host="localhost",
                    port="5432"
                )
                self.cursor = self.connection.cursor()
                self.setup_database()
                
            except Error as e:
                print(f"Erro ao criar DB: {e}")

    def setup_database(self):
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                matricula INTEGER UNIQUE NOT NULL,
                nota_av1 FLOAT NOT NULL,
                nota_av2 FLOAT NOT NULL,
                media FLOAT
            );
            """
            self.cursor.execute(create_table_query)
            
            #Calculo de media*
            
            # Dados para teste de funcionamento do postgree
            self.cursor.execute("SELECT COUNT(*) FROM students")
            if self.cursor.fetchone()[0] == 0:
                initial_data = """
                INSERT INTO students (nome, matricula, nota_av1, nota_av2)
                VALUES 
                    ('João', 1111, 5.0, 6.0),
                    ('Bruno', 1110, 2.0, 5.0),
                    ('Mario', 1112, 3.0, 7.0);
                """
                self.cursor.execute(initial_data)
            
            self.connection.commit()
                
        except Error as e:
            print(f"Erro ao config DB: {e}")
            self.connection.rollback()

    def add_aluno(self):
        try:
            print("\nAdicionando aluno:")
            nome = input("Nome do aluno: ")
            
            while True:
                try:
                    matricula = int(input("Matricula: "))
                    break
                except ValueError:
                    print("Numero invalido, tente novamente")
            
            while True:
                try:
                    av1 = float(input("Nota Av1: "))
                    av2 = float(input("Nota Av2: "))
                    break
                except ValueError:
                    print("Nota invalida, tente novamente")

            insert_query = """
            INSERT INTO students (nome, matricula, nota_av1, nota_av2)
            VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(insert_query, (nome, matricula, av1, av2))
            self.connection.commit()
            print("\nAluno adicionado com sucesso")
            
        except Error as e:
            if "duplicate key" in str(e):
                print("Erro: Matricula ja existente")
            else:
                print(f"Erro: {e}")
            self.connection.rollback()

    def Procura_aluno(self):
        try:
            print("\nProcurando por alunos:")
            search_term = input("Insira a matricula ou nome: ")
            
            if search_term.isdigit():
                query = "SELECT * FROM students WHERE matricula = %s"
                self.cursor.execute(query, (int(search_term),))
            else:
                query = "SELECT * FROM students WHERE nome ILIKE %s"
                self.cursor.execute(query, (f"%{search_term}%",))
            
            results = self.cursor.fetchall()
            
            if not results:
                print("Nenhum resultado.")
            else:
                print("\nResultados:")
                print("\nID | Name | Matricula | AV1 | AV2 | Media")
                print("-" * 50)
                for row in results:
                    print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]:.1f} | {row[4]:.1f} | {row[5]:.1f}")
                    
        except Error as e:
            print(f"Erro: {e}")
            self.connection.rollback()

    def Listar_alunos(self):
        try:
            self.cursor.execute("SELECT * FROM students ORDER BY id")
            results = self.cursor.fetchall()
            
            if not results:
                print("\nBanco vazio.")
            else:
                print("\nlista de alunos:")
                print("\nID | Name | Matricula | AV1 | AV2 | Media")
                print("-" * 50)
                for row in results:
                    print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]:.1f} | {row[4]:.1f} | {row[5]:.1f}")
                    
        except Error as e:
            print(f"Erro: {e}")
            self.connection.rollback()

    def Terminar_conecao(self):
        if hasattr(self, 'connection'):
            self.cursor.close()
            self.connection.close()

def Menu():
    db = AlunoDB()
    
    while True:
        print("\n--- Menu ---")
        print("1. novo aluno")
        print("2. procura")
        print("3. listar todos")
        print("4. terminar")
        
        choice = input("escolha entre 1 e 4 : ")
        
        if choice == '1':
            db.add_aluno()
        elif choice == '2':
            db.Procura_aluno()
        elif choice == '3':
            db.Listar_alunos()
        elif choice == '4':
            db.Terminar_conecao()
            print("terminando")
            break
        else:
            print("escolha invalida.")

if __name__ == "__main__":
    Menu()