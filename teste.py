import requests



# URL original
url = "https://dl.ymcdn.org/v2/b627f2d38ff5d54bdd44f1032098fc77/bwGftC32wNw?_l=SHVuZ3JpYSstK1RlbXBvcmFsKyUyOE9mZmljaWFsK011c2ljK1ZpZGVvJTI5&_t=K1Nd0Q=="

# Fazendo a requisição sem seguir redirecionamentos
response = requests.get(url, allow_redirects=False, stream=True)

# Verifica se há redirecionamento
if response.status_code == 302:
    # Obtém o cabeçalho Location
    location_url = response.headers.get("Location")
    print("URL de redirecionamento:", location_url, response.status_code)
else:
    print("Nenhum redirecionamento encontrado.")
