import re
import azure.functions as func
import logging

app = func.FunctionApp()

@app.route(route="validar-cpf", auth_level=func.AuthLevel.ANONYMOUS,
           methods=["POST"])
def validar_cpf(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Inicializando validação de CPF')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(f"Formato de corpo de requisição inválido!",
                                 status_code=400)

    cpf = req_body.get('cpf')

    if sup_validar_cpf(cpf):
        return func.HttpResponse(f"CPF validado com sucesso!")
    else:
        return func.HttpResponse("CPF inválido!")

def sup_validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)

    if len(cpf) != 11:
        return False

    if cpf == cpf[0]*11:
        return False

    # Primeiro dígito verificador
    soma = sum([int(cpf[i]) * (10-i) for i in range(9)])
    digito1 = (soma * 10 % 11) % 10

    # Segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10

    return cpf[-2:] == f"{digito1}{digito2}"