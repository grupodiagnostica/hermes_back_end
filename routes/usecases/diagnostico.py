# usecases.py
from repositories.diagnostico import DiagnosticoRepository

class DiagnosticoUseCase:
    def __init__(self):
        self.diagnostico_repository = DiagnosticoRepository

    def create_diagnostico(self, data):
        return self.diagnostico_repository.create_diagnostico(data)

    def get_diagnosticos(self, id=None, id_medico=None, id_clinica=None, id_paciente=None):
        return self.diagnostico_repository.get_diagnosticos(id, id_medico, id_clinica, id_paciente)

    def update_diagnostico(self, diagnostico_id, data):
        return self.diagnostico_repository.update_diagnostico(diagnostico_id, data)

    def delete_diagnostico(self, diagnostico_id):
        return self.diagnostico_repository.delete_diagnostico(diagnostico_id)
    
    def get_atendimentos_por_ano(self, clinica_id,data):
        return self.diagnostico_repository.get_atendimentos_por_ano(clinica_id,data)

    def diagnostico_classificacoes(self, id_clinica):
        return self.diagnostico_repository.diagnostico_classificacoes(id_clinica)

    def get_diagnosticos_por_ano(self, clinica_id, data):
        return self.diagnostico_repository.get_diagnosticos_por_ano(clinica_id, data)

    def get_comparacoes_diagnosticos_classificacoes(self, clinica_id):
        return self.diagnostico_repository.get_comparacoes_diagnosticos_classificacoes(diagnostico_id)
