
from robots.judLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class CorrecaoErrosUsuarioUseCase:
    def __init__(
        self,
        data_input: DadosEntradaFormatadosModel
    ) -> None:
        self.data_input = data_input

    def execute(self)->DadosEntradaFormatadosModel:
        self.data_input.uf = self.data_input.uf.replace("-","")

        if 'Justica' in self.data_input.justica: 
            self.data_input.justica = self.data_input.justica.replace("Justica","Justiça")

        if self.data_input.cpf_cnpj_envolvido == '0':
            self.data_input.cpf_cnpj_envolvido = ''

        if self.data_input.processo_originario != '' and (self.data_input.titulo == 'Indenizatória' or self.data_input.titulo == 'Reclamação Pré-Processual'):
            self.data_input.processo_originario = ''

        if self.data_input.complemento_comarca == 'Capital Copacabana':
            self.data_input.complemento_comarca = 'Copacabana'

        elif self.data_input.complemento_comarca == '2° JD':
            self.data_input.complemento_comarca = '2ª JD'

        elif self.data_input.complemento_comarca == '29° JD':
            self.data_input.complemento_comarca = '29º JD da Comarca de Belo Horizonte'

        if self.data_input.comarca == 'Norte da Ilha':
            self.data_input.comarca = 'Norte Da Ilha'

        elif self.data_input.comarca == 'Embu das Artes':
            self.data_input.comarca = 'Embu Das Artes'

        elif self.data_input.comarca == 'Arujá':
            self.data_input.comarca = 'Guarujá'

        if self.data_input.vara == 'Juizado Especial Cível':
            self.data_input.vara = 'Juizado Especial Cível - JEC'

        elif self.data_input.vara == 'Juizado-Especial-Civel-JEC':
            self.data_input.vara = 'Juizado Especial Cível - JEC'

        elif self.data_input.vara == 'Vara Civel':
            self.data_input.vara = 'Vara Cível - VC'

        elif self.data_input.vara == 'Vara-Civel-VC':
            self.data_input.vara = 'Vara Cível - VC'

        elif self.data_input.vara == 'Vara do Juizado Especial':
            self.data_input.vara = 'Vara Do Juizado Especial'

        elif self.data_input.vara == 'Vara Descentralizada de Santa Felicidade':
            self.data_input.vara = 'Vara Descentralizada De Santa Felicidade'

        elif self.data_input.vara == 'Vara do Juizado Especial Cível':
            self.data_input.vara = 'Vara Do Juizado Especial Cível'

        elif self.data_input.vara == 'Vara do Juizado Especial Central':
            self.data_input.vara = 'Vara Do Juizado Especial Central'

        elif self.data_input.vara == 'Vara Juizado Especial Cível e Criminal':
            self.data_input.vara = 'Do Juizado Especial Cível E Criminal'

        elif self.data_input.vara == 'Vara do Juizado das Relações de Consumo':
            self.data_input.vara = 'Do Juizado Especial Cível Das Relações De Consumo'

        if len(self.data_input.data_distribuicao.split("/")[-1]) == 2:
            dia, mes, ano = self.data_input.data_distribuicao.split('/')
            if len(ano):
                ano = '20' + ano
            self.data_input.data_distribuicao =  f'{dia}/{mes}/{ano}'
        return self.data_input