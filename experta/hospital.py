from experta import KnowledgeEngine, Rule, Fact, Field

class Planta(Fact):
    """Información sobre la planta."""
    necesita_agua = Field(str, default="")
    luz_solar = Field(str, default="")
    tipo_hojas = Field(str, default="")

class IdentificadorDePlantas(KnowledgeEngine):
    @Rule(Planta(necesita_agua="poca", luz_solar="alta", tipo_hojas="pequeñas y gruesas"))
    def es_cactus(self):
        print("La planta es probablemente un Cactus.")

    @Rule(Planta(necesita_agua="mucha", luz_solar="baja", tipo_hojas="grandes y delgadas"))
    def es_helecho(self):
        print("La planta es probablemente un Helecho.")

    @Rule(Planta(necesita_agua="moderada", luz_solar="media", tipo_hojas="coloridas y duraderas"))
    def es_orquidea(self):
        print("La planta es probablemente una Orquídea.")


# identificador = IdentificadorDePlantas()
# identificador.reset()  # Preparar el motor de inferencia
#
# # Recoger características de la planta del usuario
# necesita_agua = input("¿Cuánta agua necesita la planta? (poca/mucha/moderada): ").lower()
# luz_solar = input("¿Cuánta luz solar necesita la planta? (baja/media/alta): ").lower()
# tipo_hojas = input("Describe las hojas de la planta (pequeñas y gruesas/grandes y delgadas/coloridas y duraderas): ").lower()
#
# # Declarar un hecho Planta con las características recogidas
# identificador.declare(Planta(necesita_agua=necesita_agua, luz_solar=luz_solar, tipo_hojas=tipo_hojas))
# identificador.run()

class Diagnostic(Fact):
    """informacion del paciente"""
    herida = Field(str, default="ninguna")
    enfermedad = Field(str, default="ninguna")

class Hospital_Diagnostic (KnowledgeEngine):
    """posibles heridas: laceracion, quemadura,punzon,golpe,ninguna """
    """posibles enfermedades: virus,inflamacion,mental,ninguna"""

    #laceracion
    @Rule(Diagnostic(herida="laceracion", enfermedad="virus"))
    def lac_virus(self):
        print("lac_virus")

    @Rule(Diagnostic(herida="laceracion", enfermedad="inflamacion"))
    def lac_infl(self):
        print("lac_infl")

    @Rule(Diagnostic(herida="laceracion", enfermedad="mental"))
    def lac_ment(self):
        print("lac_ment")

    @Rule(Diagnostic(herida="laceracion", enfermedad="ninguna"))
    def lac_non(self):
        print("lac_non")

    #quemadura
    @Rule(Diagnostic(herida="quemadura", enfermedad="virus"))
    def quem_vir(self):
        print("quem_vir")

    @Rule(Diagnostic(herida="quemadura", enfermedad="inflamacion"))
    def quem_infl(self):
        print("quem_infl")

    @Rule(Diagnostic(herida="quemadura", enfermedad="mental"))
    def quem_ment(self):
        print("quem_ment")

    @Rule(Diagnostic(herida="quemadura", enfermedad="ninguna"))
    def quem_non(self):
        print("quem_non")

    #punzon
    @Rule(Diagnostic(herida="punzon", enfermedad="virus"))
    def pun_vir(self):
        print("pun_vir")

    @Rule(Diagnostic(herida="punzon", enfermedad="inflamacion"))
    def pun_infl(self):
        print("punzon y infl")

    @Rule(Diagnostic(herida="punzon", enfermedad="mental"))
    def pun_ment(self):
        print("punzon y ment")

    @Rule(Diagnostic(herida="punzon", enfermedad="ninguna"))
    def pun_non(self):
        print("punzon y non")

    #golpe
    @Rule(Diagnostic(herida="golpe", enfermedad="virus"))
    def golp_vir(self):
        print("golpeado y virus")

    @Rule(Diagnostic(herida="golpe", enfermedad="inflamacion"))
    def golp_infl(self):
        print("golpeado y inlf")

    @Rule(Diagnostic(herida="golpe", enfermedad="mental"))
    def golp_ment(self):
        print("golpeado y loco")

    @Rule(Diagnostic(herida="golpe", enfermedad="ninguna"))
    def golp_non(self):
        print("golpeado")

    #ninguna
    @Rule(Diagnostic(herida="ninguna", enfermedad="virus"))
    def non_vir(self):
        print("con virus")

    @Rule(Diagnostic(herida="ninguna", enfermedad="inflamacion"))
    def non_infl(self):
        print("quemao")

    @Rule(Diagnostic(herida="ninguna", enfermedad="mental"))
    def non_ment(self):
        print("loco")

    @Rule(Diagnostic(herida="ninguna", enfermedad="ninguna"))
    def non_non(self):
        print("dale pal gao pp")


identificador= Hospital_Diagnostic()
identificador.reset()

herida=input("tipo de herida?laceracion/quemadura/punzon/golpe/ninguna")
enfermedad=input("tipo de enfermeda?virus/inflamacion/mental/ninguna")
identificador.declare(Diagnostic(herida=herida,enfermedad=enfermedad))
identificador.run()