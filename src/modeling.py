from numpy import vdot
import pandas as pd

pd.set_option("display.max_rows", None, "display.max_columns", None)

class Turma():
    def __init__(self, disciplina, professor, dias_horario, numero_alunos, curso, periodo, acessibilidade, qualidade):
        self.disciplina = disciplina
        self.professor = professor
        self.dias_horario = dias_horario
        self.numero_alunos = numero_alunos
        self.curso = curso
        self.periodo = periodo
        self.acessibilidade = acessibilidade
        self.qualidade = qualidade

def find_position(solution, id_sala):
    n = len(solution)
    for i in range(n):
        if solution['id_sala'][i] == id_sala:
            return i

def compare_rate(numero_cadeiras, numero_alunos):
    taxa_ocupacao = numero_alunos * 100 / numero_cadeiras
    return taxa_ocupacao >= 70
    
    
def find_class(turma, horario, salas, solution):
    for i in salas.index:
        numCadeiras = salas['numero_cadeiras'][i]
        numAlunos = turma.numero_alunos
        if compare_rate(numCadeiras, numAlunos) and salas['acessivel'][i] == turma.acessibilidade and salas['qualidade'][i] >= turma.qualidade:
            if salas['id_sala'][i] not in solution['id_sala']:
                return salas['numero_cadeiras'][i], salas['id_sala'][i]
            elif salas['id_sala'][i] in solution['id_sala']:
                idx_sala = find_position(solution, salas['id_sala'][i])
                if solution['horario'][ 0 if idx_sala == None else idx_sala ] != horario:
                    return salas['numero_cadeiras'][i], salas['id_sala'][i]

def allocation(salas, turmas):
    solution = { 'horario': [], 'id_sala': [], 'disciplina': [], 'professor': [], 'numero_cadeiras': [], 'numero_alunos': [] }
  
    for i in turmas.index:
        dias_horario = turmas['dias_horario'][i].split("-")
        disciplina = turmas.loc[i, 'disciplina']
        professor = turmas.loc[i, 'professor']
        numero_alunos = turmas.loc[i, 'numero_alunos']
        curso = turmas.loc[i, 'curso']
        numero_alunos = turmas.loc[i, 'numero_alunos']
        curso = turmas.loc[i, 'curso']
        periodo = turmas.loc[i, 'período']
        acessibilidade = turmas.loc[i, 'acessibilidade']
        qualidade = turmas.loc[i, 'qualidade']

        turma = Turma(disciplina, professor, dias_horario, numero_alunos, curso, periodo, acessibilidade, qualidade)
        
        for horario in dias_horario:
            
            if find_class(turma, horario, salas, solution) == None :
                pass
            else:
                numero_cadeiras, sala_horario = find_class(turma, horario, salas, solution)
                solution['horario'].append(horario)
                solution['id_sala'].append(sala_horario)
                solution['disciplina'].append(turma.disciplina)
                solution['professor'].append(turma.professor)
                solution['numero_cadeiras'].append(numero_cadeiras)
                solution['numero_alunos'].append(turma.numero_alunos)
    
    return pd.DataFrame(solution)
