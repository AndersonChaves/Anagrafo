class EnumParticionamentoEspectral:
    POSITIVO_POSITIVO = 1
    POSITIVO_NEGATIVO = 2


def enum_para_string(enum):
    if enum == EnumParticionamentoEspectral.POSITIVO_POSITIVO:
        return "IGUAIS"
    elif enum == EnumParticionamentoEspectral.POSITIVO_NEGATIVO:
        return "DIFERENTES"
