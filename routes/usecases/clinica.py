from repositories.clinica import ClinicaRepository

class ClinicaUseCase:
    def __init__(self):
        self.clinica_repository = ClinicaRepository

    def create_clinica(self, data):
        return self.clinica_repository.create_clinica(data)

    def get_clinicas(self, cnpj=None, nome=None):
        return self.clinica_repository.get_clinicas(cnpj, nome)

    def update_clinica(self, clinica_id, data):
        return self.clinica_repository.update_clinica(clinica_id, data)

    def delete_clinica(self, clinica):
        return self.clinica_repository.delete_clinica(clinica)

    def create_medico(self, clinica_id, data):
        return self.clinica_repository.create_medico(clinica_id, data)

    def get_medicos(self, clinica_id):
        return self.clinica_repository.get_medicos(clinica_id)

    def update_medico(self, clinica, data):
        return self.clinica_repository.update_medico(clinica, data)
