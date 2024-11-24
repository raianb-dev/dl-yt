import requests

def processa_location(url):
    """
    Função para processar o redirecionamento de uma URL.
    Se a resposta for 302 (redirecionamento), retorna a URL de redirecionamento.
    Caso contrário, retorna a URL original.
    """
    try:
        # Fazendo a requisição sem seguir redirecionamentos
        response = requests.get(url, allow_redirects=False, stream=True)
        
        # Verifica se há redirecionamento (status 302)
        if response.status_code == 302:
            # Obtém o cabeçalho 'Location' que contém a URL de redirecionamento
            location_url = response.headers.get("Location")
            print(f"Redirecionamento encontrado: {location_url}")
            return location_url
        else:
            print(f"Nenhum redirecionamento encontrado, status code: {response.status_code}")
            return url
    except requests.exceptions.RequestException as e:
        print(f"Erro ao processar a URL: {e}")
        return None

