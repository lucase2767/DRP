import psycopg2
from psycopg2 import Error
from typing import List, Tuple, Optional
#Separação do back e front end

class BancoDados:
    #separando paremetros para simplificar o codigo de conexão
    def __init__(self, nome_banco="student_db", usuario="postgres", 
                 senha="123456", host="localhost", porta="5432"):
        self.parametros_conexao = {
            "dbname": nome_banco,
            "user": usuario,
            "password": senha,
            "host": host,
            "port": porta
        }
        self.conexao = None
        self.cursor = None
        self.inicializar_banco()

    #logica de inicialização
    def conectar(self) -> None:
        try:
            self.conexao = psycopg2.connect(**self.parametros_conexao)
            self.cursor = self.conexao.cursor()
        except Error as e:
            raise ErroBanco(f"Erro de conexão: {e}")

    def inicializar_banco(self) -> None:
        try:
            try:
                self.conectar()
            except Error:
                temp_params = self.parametros_conexao.copy()
                temp_params["dbname"] = "postgres"
                with psycopg2.connect(**temp_params) as temp_conn:
                    temp_conn.autocommit = True
                    with temp_conn.cursor() as temp_cur:
                        temp_cur.execute(f"CREATE DATABASE {self.parametros_conexao['dbname']}")
                
                self.conectar()
            
            self._configurar_esquema_banco()
            
        except Error as e:
            raise ErroBanco(f"Erro de inicialização do banco: {e}")

    def _configurar_esquema_banco(self) -> None:
        #criação do banco se não existir
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS alunos (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    matricula INTEGER UNIQUE NOT NULL,
                    turma VARCHAR(50) NOT NULL,
                    nota_av1 FLOAT NOT NULL,
                    nota_av2 FLOAT NOT NULL,
                    media FLOAT
                );
            """)
            #Calculo de media
            self.cursor.execute("""
                CREATE OR REPLACE FUNCTION calcular_media()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.media := (NEW.nota_av1 + NEW.nota_av2) / 2;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            """)

            self.cursor.execute("""
                DROP TRIGGER IF EXISTS atualizar_media ON alunos;
                CREATE TRIGGER atualizar_media
                    BEFORE INSERT OR UPDATE ON alunos
                    FOR EACH ROW
                    EXECUTE FUNCTION calcular_media();
            """)

            self.conexao.commit()
        except Error as e:
            self.conexao.rollback()
            raise ErroBanco(f"Erro na configuração do esquema: {e}")

    #Funcionalidades do sistema
    def adicionar_aluno(self, nome: str, matricula: int, turma: str,
                       nota_av1: float, nota_av2: float) -> None:
        try:
            self.cursor.execute("""
                INSERT INTO alunos (nome, matricula, turma, nota_av1, nota_av2)
                VALUES (%s, %s, %s, %s, %s)
            """, (nome, matricula, turma, nota_av1, nota_av2))
            self.conexao.commit()
        except Error as e:
            self.conexao.rollback()
            if "duplicate key" in str(e):
                raise ErroBanco("Número de matrícula já existe")
            raise ErroBanco(f"Erro ao adicionar aluno: {e}")

    def atualizar_aluno(self, id: int, nome: str, matricula: int, 
                       turma: str, nota_av1: float, nota_av2: float) -> None:
        try:
            self.cursor.execute("""
                UPDATE alunos 
                SET nome = %s, matricula = %s, turma = %s, 
                    nota_av1 = %s, nota_av2 = %s
                WHERE id = %s
            """, (nome, matricula, turma, nota_av1, nota_av2, id))
            self.conexao.commit()
        except Error as e:
            self.conexao.rollback()
            if "duplicate key" in str(e):
                raise ErroBanco("Número de matrícula já existe")
            raise ErroBanco(f"Erro ao atualizar aluno: {e}")

    def excluir_aluno(self, id: int) -> None:
        try:
            self.cursor.execute("DELETE FROM alunos WHERE id = %s", (id,))
            self.conexao.commit()
        except Error as e:
            self.conexao.rollback()
            raise ErroBanco(f"Erro ao excluir aluno: {e}")

    def procurar_aluno(self, termo_busca: str) -> List[Tuple]:
        try:
            if termo_busca.isdigit():
                self.cursor.execute(
                    "SELECT * FROM alunos WHERE matricula = %s",
                    (int(termo_busca),)
                )
            else:
                self.cursor.execute(
                    "SELECT * FROM alunos WHERE nome ILIKE %s OR turma ILIKE %s",
                    (f"%{termo_busca}%", f"%{termo_busca}%")
                )
            return self.cursor.fetchall()
        except Error as e:
            raise ErroBanco(f"Erro na busca: {e}")

    def listar_alunos(self) -> List[Tuple]:
        try:
            self.cursor.execute("SELECT * FROM alunos ORDER BY id")
            return self.cursor.fetchall()
        except Error as e:
            raise ErroBanco(f"Erro ao recuperar alunos: {e}")

    def fechar(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.conexao:
            self.conexao.close()

class ErroBanco(Exception):
    pass