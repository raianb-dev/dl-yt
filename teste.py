import requests

def processa_location (url: str) -> str: 

    # URL original


    # Fazendo a requisição sem seguir redirecionamentos
    response = requests.get(url, allow_redirects=False)

    # Verifica se há redirecionamento
    if response.status_code == 302:
        # Obtém o cabeçalho Location
        location_url = response.headers.get("Location")
        print(location_url)
        return location_url
    return response

