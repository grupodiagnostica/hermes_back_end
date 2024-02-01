# usecases.py
from repositories import ClinicaRepository, MedicoRepository

class ClinicaUseCase:
    def __init__(self, clinica_repository):
        self.clinica_repository = clinica_repository

    def create_clinica(self, data):
        return self.clinica_repository.create_clinica(data)

    def get_clinicas(self, cnpj=None, nome=None):
        return self.clinica_repository.get_clinicas(cnpj, nome)

    def update_clinica(self, clinica, data):
        return self.clinica_repository.update_clinica(clinica, data)

    def delete_clinica(self, clinica):
        return self.clinica_repository.delete_clinica(clinica)

    def create_medico(self, clinica, data):
        return self.clinica_repository.create_medico(clinica, data)

    def get_medicos(self, clinica):
        return self.clinica_repository.get_medicos(clinica)

    def update_medico(self, clinica, data):
        return self.clinica_repository.update_medico(clinica, data)
