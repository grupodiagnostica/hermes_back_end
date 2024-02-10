from repositories.medico import MedicoRepository

class MedicoUseCase:
    def __init__(self):
        self.medico_repository = MedicoRepository()

    def create_medico(self, data):
        return self.medico_repository.create_medico(data)

    def get_medicos(self, id_pessoa=None, crm=None, especialidade=None):
        return self.medico_repository.get_medicos(id_pessoa, crm, especialidade)

    def update_medico(self, medico_id, data):
        return self.medico_repository.update_medico(medico_id, data)

    def delete_medico(self, medico_id):
        return self.medico_repository.delete_medico(medico_id)

    def get_clinicas_medico(self, medico_id):
        return self.medico_repository.get_clinicas_medico(medico_id)

    def existe_medico(self, medico_crm):
        return self.medico_repository.existe_medico(medico_crm)