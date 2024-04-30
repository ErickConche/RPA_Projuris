
from robots.judAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class CorrecaoErrosUsuarioUseCase:
    def __init__(
        self,
        data_input: DadosEntradaFormatadosModel
    ) -> None:
        self.data_input = data_input

    def execute(self)->DadosEntradaFormatadosModel:
        if self.data_input.cidade == 'São Gonçalo':
            self.data_input.cidade = 'SAO GONÇALO'

        elif self.data_input.cidade == 'Paraty':
            self.data_input.cidade = 'PARATI'

        if self.data_input.sistema_tribunal == 'eSAJ':
            self.data_input.sistema_tribunal = 'e-SAJ'

        elif self.data_input.sistema_tribunal == 'eproc':
            self.data_input.sistema_tribunal = 'e-proc'
            
        elif self.data_input.sistema_tribunal == 'Projudi':
            self.data_input.sistema_tribunal = 'PROJUDI'

        if self.data_input.cpf_cnpj_envolvido == '000.000.000-00':
            self.data_input.cpf_cnpj_envolvido =''

        if self.data_input.cpf_cnpj_outros_envolvidos1 == '000.000.000-00':
            self.data_input.cpf_cnpj_outros_envolvidos1 =''

        if self.data_input.cpf_cnpj_outros_envolvidos2 == '000.000.000-00':
            self.data_input.cpf_cnpj_outros_envolvidos2 =''

        if self.data_input.cpf_cnpj_outros_envolvidos3 == '000.000.000-00':
            self.data_input.cpf_cnpj_outros_envolvidos3 =''

        if self.data_input.cpf_cnpj_outros_envolvidos4 == '000.000.000-00':
            self.data_input.cpf_cnpj_outros_envolvidos4 =''

        if self.data_input.cpf_cnpj_outros_envolvidos5 == '000.000.000-00':
            self.data_input.cpf_cnpj_outros_envolvidos5 =''

        if self.data_input.cpf_cnpj_outros_envolvidos6 == '000.000.000-00':
            self.data_input.cpf_cnpj_outros_envolvidos6 =''

        if self.data_input.cpf_cnpj_outros_envolvidos7 == '000.000.000-00':
            self.data_input.cpf_cnpj_outros_envolvidos7 =''

        if self.data_input.cpf_cnpj_outros_envolvidos8 == '000.000.000-00':
            self.data_input.cpf_cnpj_outros_envolvidos8 =''

        if self.data_input.cpf_cnpj_outros_envolvidos9 == '000.000.000-00':
            self.data_input.cpf_cnpj_outros_envolvidos9 =''

        if self.data_input.cpf_cnpj_outros_envolvidos10 == '000.000.000-00':
            self.data_input.cpf_cnpj_outros_envolvidos10 =''
        
        if len(self.data_input.data_distribuicao.split("/")[-1]) == 2:
            dia, mes, ano = self.data_input.data_distribuicao.split('/')
            if len(ano):
                ano = '20' + ano
            self.data_input.data_distribuicao =  f'{dia}/{mes}/{ano}'

        return self.data_input