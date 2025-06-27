import requests

TOKEN = '7627891801:AAEoV04-jl0SDDIkHiqWKl2UpQRfv9l4QdA'
url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'

resp = requests.get(url)
print(resp.json())