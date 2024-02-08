from typing import List
from modules.logger.Logger import Logger
from robots.judLegalone.useCases.listarEnvolvidos.__model__.ObjEnvolvidosModel import ObjEnvolvidosModel
from robots.judLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel

class ListarEnvolvidosUseCase:
    def __init__(
        self,
        classLogger: Logger,
        data_input: DadosEntradaFormatadosModel
    ) -> None:
        self.classLogger = classLogger
        self.data_input = data_input

    def execute(self)-> List[ObjEnvolvidosModel]:
        try:
            lista_envolvidos: List[ObjEnvolvidosModel] = []
            obj_envolvido: ObjEnvolvidosModel = ObjEnvolvidosModel(
                nome=self.data_input.nome_envolvido,
                cpf_cnpj=self.data_input.cpf_cnpj_envolvido,
                tag_objeto="nome_envolvido"
            )
            lista_envolvidos.append(obj_envolvido)
            obj = self.data_input.__dict__
            index = 1
            qtde_max = 10
            while index <= qtde_max:
                nome_envolvido = f"nome_outros_envolvidos{str(index)}"
                chave = f"cpf_cnpj_outros_envolvidos{str(index)}"
                if obj.get(nome_envolvido) != '':
                    obj_envolvido: ObjEnvolvidosModel = ObjEnvolvidosModel(
                        nome=obj.get(nome_envolvido),
                        cpf_cnpj=obj.get(chave),
                        tag_objeto=nome_envolvido
                    )
                    lista_envolvidos.append(obj_envolvido)
                    index += 1
                else:
                    break
            return lista_envolvidos

        except Exception as error:
            message = "Erro ao listar os envolvidos recebidos"
            self.classLogger.message(message)
            raise error