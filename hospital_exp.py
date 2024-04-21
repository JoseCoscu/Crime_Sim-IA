from experta import KnowledgeEngine, Rule, Fact, Field

class Diagnostic(Fact):
    """informacion del paciente"""
    herida = Field(str, default="ninguna")
    enfermedad = Field(str, default="ninguna")

class Hospital_Diagnostic (KnowledgeEngine):
        
    """posibles enfermedades: virus,inflamacion,mental,ninguna posibles heridas: laceracion, quemadura,punzon,golpe,ninguna"""
    def __init__(self):
        super().__init__()
        self.result = None
    #laceracion
    @Rule(Diagnostic(herida="laceracion", enfermedad="virus"))
    def lac_virus(self):

        self.result=( True,15,'antibioticos')

    @Rule(Diagnostic(herida="laceracion", enfermedad="inflamacion"))
    def lac_infl(self):
        self.result=( True, 10, 'antinflamatorios')

    @Rule(Diagnostic(herida="laceracion", enfermedad="mental"))
    def lac_ment(self):
        self.result=( True, 10, 'diacepan')

    @Rule(Diagnostic(herida="laceracion", enfermedad="ninguna"))
    def lac_non(self):
        self.result=( True, 10,None)

    #quemadura
    @Rule(Diagnostic(herida="quemadura", enfermedad="virus"))
    def quem_vir(self):
        self.result=( True, 15, 'antibioticos')

    @Rule(Diagnostic(herida="quemadura", enfermedad="inflamacion"))
    def quem_infl(self):
        self.result=( True, 9, 'antinflamatorios')


    @Rule(Diagnostic(herida="quemadura", enfermedad="mental"))
    def quem_ment(self):
        self.result=( True, 9, 'diacepan')

    @Rule(Diagnostic(herida="quemadura", enfermedad="ninguna"))
    def quem_non(self):
        self.result=( True, 9, None)


    #punzon
    @Rule(Diagnostic(herida="punzon", enfermedad="virus"))
    def pun_vir(self):
        self.result=( True, 15, 'antibioticos')

    @Rule(Diagnostic(herida="punzon", enfermedad="inflamacion"))
    def pun_infl(self):
        self.result=( True, 8, 'antinflamatorios')

    @Rule(Diagnostic(herida="punzon", enfermedad="mental"))
    def pun_ment(self):
        self.result=( True, 8, 'diacepan')

    @Rule(Diagnostic(herida="punzon", enfermedad="ninguna"))
    def pun_non(self):
        self.result=( True, 8, None)

    #golpe
    @Rule(Diagnostic(herida="golpe", enfermedad="virus"))
    def golp_vir(self):
        self.result=( True, 15, 'antibioticos')

    @Rule(Diagnostic(herida="golpe", enfermedad="inflamacion"))
    def golp_infl(self):
        self.result=( True, 5, 'antinflamatorios')


    @Rule(Diagnostic(herida="golpe", enfermedad="mental"))
    def golp_ment(self):
        self.result=( True, 5, 'diacepan')

    @Rule(Diagnostic(herida="golpe", enfermedad="ninguna"))
    def golp_non(self):
        self.result=( True, 5, None)

    #ninguna
    @Rule(Diagnostic(herida="ninguna", enfermedad="virus"))
    def non_vir(self):
        self.result=(False,15,'antibioticos')

    @Rule(Diagnostic(herida="ninguna", enfermedad="inflamacion"))
    def non_infl(self):
        self.result=( False,7,'antinflamatorio')

    @Rule(Diagnostic(herida="ninguna", enfermedad="mental"))
    def non_ment(self):
        self.result=( False, 7, 'diacepan')


    @Rule(Diagnostic(herida="ninguna", enfermedad="ninguna"))
    def non_non(self):
        self.result=( False,0,None)


def diag_hosp(herida,enfermedad):
    identificador= Hospital_Diagnostic()
    identificador.reset()
    identificador.declare(Diagnostic(herida=herida,enfermedad=enfermedad))
    identificador.run()
    return identificador.result

result=diag_hosp('golpe','virus')
print(result)