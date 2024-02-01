from models import db, Diagnostico

class DiagnosticoRepository:
    def create_diagnostico(self, data):
        novo_diagnostico = Diagnostico(**data)
        db.session.add(novo_diagnostico)
        db.session.commit()
        return novo_diagnostico

    def get_diagnosticos(self, id=None, id_medico=None, id_clinica=None, id_paciente=None):
        query = Diagnostico.query
        if id:
            query = query.filter(Diagnostico.id == id)
        if id_medico:
            query = query.filter(Diagnostico.id_medico == id_medico)
        if id_clinica:
            query = query.filter(Diagnostico.id_clinica == id_clinica)
        if id_paciente:
            query = query.filter(Diagnostico.id_paciente == id_paciente)
        return query.all()

    def update_diagnostico(self, diagnostico_id, data):
        diagnostico = Diagnostico.query.get(diagnostico_id)
        if not diagnostico:
            return None
        for key, value in data.items():
            setattr(diagnostico, key, value)
        db.session.commit()
        return diagnostico

    def delete_diagnostico(self, diagnostico_id):
        diagnostico = Diagnostico.query.get(diagnostico_id)
        if diagnostico:
            db.session.delete(diagnostico)
            db.session.commit()
            return True
        return False
