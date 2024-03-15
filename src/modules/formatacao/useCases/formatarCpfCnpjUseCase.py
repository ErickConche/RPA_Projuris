
class FormatarCpfCnpjUseCase:
    def __init__(
        self,
        cpf_cnpj:str
    ) -> None:
        self.cpf_cnpj = cpf_cnpj

    def execute(self)->str:
        cnpj_return = self.cpf_cnpj
        if len(self.cpf_cnpj) == 14 and '.' not in self.cpf_cnpj:
            cnpj_return = self.cpf_cnpj[0:2]+"."+self.cpf_cnpj[2:5]+"."+self.cpf_cnpj[5:8]+"/"+self.cpf_cnpj[8:12]+"-"+self.cpf_cnpj[12:14]
        elif len(self.cpf_cnpj) == 11 and '.' not in self.cpf_cnpj:
            cnpj_return = self.cpf_cnpj[0:3]+"."+self.cpf_cnpj[3:6]+"."+self.cpf_cnpj[6:9]+"-"+self.cpf_cnpj[9:12]
        return cnpj_return