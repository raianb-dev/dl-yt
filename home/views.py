import json
import re
from django.shortcuts import redirect, render
import requests
from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from tempfile import NamedTemporaryFile
from time import sleep
from teste import processa_location


def redirect_to_home(request, undefined_path=None):
    # Isso redireciona o usuário para a página inicial
    return redirect('download_audio')

@csrf_exempt
def download_audio(request):
    if request.method == 'POST':
        init = 'init'
        detail = 'detail'
        convert = 'convert'
        progress = 'progress'  # Nova rota para verificar o status do processamento
        video_url = request.POST.get('video_id')
        
        # Verifique se a URL não está vazia
        if not video_url:
            return JsonResponse({'error': 'URL do vídeo não fornecida.'}, status=400)

        # Expressão regular para extrair o video_id da URL
        match = re.search(r'(?:v=|\/)([a-zA-Z0-9_-]{11})(?:[&?]|$)', video_url)
        
        if match:
            video_id = match.group(1)
  
        url = 'https://v.ymcdn.org/api/v3/'

        headers = {
            'accept': '*/*',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'dnt': '1',
            'origin': 'https://pt3.greenconvert.net',
            'priority': 'u=5, v',
            'referer': 'https://pt3.greenconvert.net/',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        }
        
        # Capturar o hash através do video_id
        payload = {'id': f'{video_id}'}
        req = requests.post(url=f'{url}{init}', headers=headers, data=payload)
        res = json.loads(req.text)
        hash_id = res.get('hash')
        print(hash_id)
        if not hash_id:
            return JsonResponse({'error': 'Hash not found'}, status=400)
        
        # Converter o vídeo em .mp3
        payload = {'id': f'{hash_id}', 'format': '64k', 'type': 'direct', 's': 600}
        requests.post(url=f'{url}{convert}', headers=headers, data=payload)

        # Iniciar o processamento no endpoint progress
        while True:
            # Verificar o status do processamento a cada 1 segundo
            progress_payload = {'id': f'{hash_id}'}
            progress_req = requests.post(url=f'{url}{progress}', headers=headers, data=progress_payload)
            progress_res = json.loads(progress_req.text)
            status = progress_res.get('status', False)
            print(f"Status do vídeo: {status}")

            if status:  # Se status for true, significa que o vídeo foi processado
                break
            else:
                sleep(1)  # Aguardar 1 segundo antes de verificar novamente
        
        # Após o processamento ser concluído, buscar o link de download
        payload = {'id': f'{hash_id}', 'format': '64k', 'type': 'sound', 'readType': 'sound', 'direct': 'direct'}
        req = requests.post(url=f'{url}{detail}', headers=headers, data=payload)
        res = json.loads(req.text)
        file_url = res.get('fileUrl', [None])[0]
        file_name = res.get('fileName', 'audio.mp3')
        print(file_url, file_name)
        if not file_url:
            return JsonResponse({'error': 'File URL not found'}, status=400)

        # Download do arquivo
        file_response = requests.get(file_url, allow_redirects=False, stream=True)
        print(file_response.status_code)
        
        # Se a resposta for 302, tenta processar a URL com a função processa_location
        if file_response.status_code == 302:
            # A função processa_location deve retornar uma URL válida
            new_file_url = processa_location(file_url)
            if new_file_url:
                # Fazer a requisição GET novamente para o novo link
                file_response = requests.get(new_file_url, stream=True)
                print(f"Segunda tentativa - Status Code: {file_response.status_code}")
            else:
                return JsonResponse({'error': 'Não foi possível processar a URL.'}, status=400)
            
        # Verificar se a resposta é válida
        if file_response.status_code != 200:
            return JsonResponse({'error': 'Falha ao baixar o arquivo.'}, status=400)

        print('Tipo final de file_response:', type(file_response))           

        # Salvar o arquivo temporariamente
        with NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            for chunk in file_response.iter_content(chunk_size=8192):
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        # Retornar o arquivo como resposta
        response = FileResponse(open(temp_file_path, 'rb'), as_attachment=True, filename=file_name)

        # Remover o arquivo temporário após a resposta
        os.unlink(temp_file_path)

        return response
    return render(request,'index.html')
