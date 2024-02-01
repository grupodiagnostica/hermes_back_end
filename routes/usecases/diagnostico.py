# usecases.py
from repositories import DiagnosticoRepository

class DiagnosticoUseCase:
    def __init__(self, diagnostico_repository):
        self.diagnostico_repository = diagnostico_repository

    def create_diagnostico(self, data):
        return self.diagnostico_repository.create_diagnostico(data)

    def get_diagnosticos(self, id=None, id_medico=None, id_clinica=None, id_paciente=None):
        return self.diagnostico_repository.get_diagnosticos(id, id_medico, id_clinica, id_paciente)

    def update_diagnostico(self, diagnostico_id, data):
        return self.diagnostico_repository.update_diagnostico(diagnostico_id, data)

    def delete_diagnostico(self, diagnostico_id):
        return self.diagnostico_repository.delete_diagnostico(diagnostico_id)
    
    def diagnostico_atendimentos(self, data):
        return self.diagnostico_repository.diagnostico_atendimentos(data)

    def diagnostico_classificacoes(self, id=None, id_medico=None, id_clinica=None, id_paciente=None):
        return self.diagnostico_repository.diagnostico_classificacoes(id, id_medico, id_clinica, id_paciente)

    def diagnostico_diagnosticos(self, diagnostico_id, data):
        return self.diagnostico_repository.diagnostico_diagnosticos(diagnostico_id, data)

    def diagnostico_diagnosticos_classificacoes(self, diagnostico_id):
        return self.diagnostico_repository.diagnostico_diagnosticos_classificacoes(diagnostico_id)
