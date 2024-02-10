from models import db, Diagnostico
from sqlalchemy import extract

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
        diagnosticos = query.all()
        # Converta os resultados em um formato JSON
        diagnosticos_list = []
        for diagnostico in diagnosticos:
            # ... (formato da resposta JSON)
           diagnosticos_list.append({
            'id': diagnostico.id,
            'modelo': diagnostico.modelo,
            'id_medico': diagnostico.id_medico,
            'id_clinica' : diagnostico.id_clinica,
            'data_hora': str(diagnostico.data_hora),
            'raio_x': diagnostico.raio_x,
            'id_paciente': diagnostico.id_paciente,
            'laudo_medico': diagnostico.laudo_medico,
            'mapa_calor': diagnostico.mapa_calor,
            'resultado_modelo': diagnostico.resultado_modelo,
            'resultado_real': diagnostico.resultado_real,
            'paciente': {
            'id': diagnostico.paciente.id,
            'id_pessoa': diagnostico.paciente.id_pessoa,
            'sexo': diagnostico.paciente.sexo,
            'tipo_sanguineo': diagnostico.paciente.tipo_sanguineo,
            'cidade': diagnostico.paciente.cidade,
            'estado': diagnostico.paciente.estado,
            'numero': diagnostico.paciente.numero,
            'logradouro': diagnostico.paciente.logradouro,
            'bairro': diagnostico.paciente.bairro,
            'detalhes_clinicos': diagnostico.paciente.detalhes_clinicos,
            'pessoa': {
                'id': diagnostico.paciente.pessoa.id,
                'cpf': diagnostico.paciente.pessoa.cpf,
                'data_nascimento': str(diagnostico.paciente.pessoa.data_nascimento),
                'nome': diagnostico.paciente.pessoa.nome,
                'telefone': diagnostico.paciente.pessoa.telefone,
                'cargo': diagnostico.paciente.pessoa.cargo
            }
            }
        })
        return diagnosticos_list

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

    def get_atendimentos_por_ano(self, clinica_id, anoRef):
        diagnosticos = Diagnostico.query.filter(extract('year', Diagnostico.data_hora) == anoRef).filter(Diagnostico.id_clinica == clinica_id).all()
        if not diagnosticos:
            return 0
        messes = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
        for i in range(len(messes)): messes[i] += f'/{anoRef % 2000}'
        atendimentos = [0 for _ in range(len(messes))]

        for diagnostico in diagnosticos:
            atendimentos[diagnostico.data_hora.month - 1] += 1

        result = {'result': 1, 'labels': messes, 'data': atendimentos}

        return result

    def diagnostico_classificacoes(self, clinica_id):
        diagnosticos = Diagnostico.query.filter(Diagnostico.id_clinica == clinica_id).all()
        if not diagnosticos:
            return 0

        labels = ['Convergente', 'Divergente']
        classificacoes = [0, 0]

        for diagnostico in diagnosticos:
            if diagnostico.resultado_real == diagnostico.resultado_modelo:
                classificacoes[0] += 1
            else:
                classificacoes[1] += 1
        result = {'result': 1, 'labels': labels, 'data': classificacoes}
        return result

    def get_diagnosticos_por_ano(self,clinica_id,anoRef):
        diagnosticos = Diagnostico.query.filter(Diagnostico.id_clinica == clinica_id).all()
        if not diagnosticos:
            return 0

        labels = []
        num_casos = []
        messes = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
        for i in range(len(messes)): messes[i] += f'/{anoRef % 2000}'
        labels_casos:dict[list] = dict()
        
        for diagnostico in diagnosticos:
            if diagnostico.resultado_real not in labels_casos.keys():
                labels_casos[diagnostico.resultado_real] = [0 for _ in range(len(messes))]
                labels_casos[diagnostico.resultado_real][diagnostico.data_hora.month - 1] += 1
            else:
                labels_casos[diagnostico.resultado_real][diagnostico.data_hora.month - 1] += 1

        for label, num_caso in labels_casos.items():
            labels.append(label)
            num_casos.append(num_caso)
        result = {'result': 1, 'labels': messes, 'lines': labels, 'data': num_casos}
        return result
    

    def get_comparacoes_diagnosticos_classificacoes(self,clinica_id):
        diagnosticos = Diagnostico.query.filter(Diagnostico.id_clinica == clinica_id).all()
        if not diagnosticos:
            return 0

        labels = ['Diagnósticos', 'Classificações']
        classes = ['PNEUMONIA', 'COVID19', 'TUBERCULOSE', 'NORMAL']
        num_casos = [[0 for _ in range(len(classes))] for _ in range(len(labels))]
        
        for diagnostico in diagnosticos:
            if diagnostico.resultado_real in classes:
                index = classes.index(diagnostico.resultado_real)
                num_casos[0][index] += 1
            if diagnostico.resultado_modelo in classes:
                index = classes.index(diagnostico.resultado_modelo)
                num_casos[1][index] += 1

        result = {'result': 1, 'labels': labels, 'classes': classes, 'data': num_casos}

        return result
