import asyncio
import random
from pyppeteer import launch


async def captura(url: str, name: str):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'load'})
    await page.setViewport({'width': 1080, 'height': 2000})
    await page.screenshot({'path': f'./screnshots/{name}.png'})
    with open(f'./logs/{name}.html', 'w', encoding='utf-8') as arquivo:
        arquivo.write(await page.content())
    await browser.close()


async def process_chunk(chunk):
    erros: str = ''
    nome: int = random.randint(1, 100)
    print(f'ola do processo {nome}')
    for url in chunk:
        i: str = url.split('/')[2]
        print(f'processo {nome} esta buscando {i}')
        i = i.replace('.', '-')
        try:
            await captura(url, i)
        except(Exception) as e:
            erros = erros + f'Erro no site {i} string do erro: {str(e)}'
            print(f'Error {i} passando para o proximo')
    if erros:
        with open(f'./logs/log-processo-{nome}.txt', 'w') as arquivo:
            arquivo.write(erros)


def ler_arquivo_links(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        links = [linha.strip() for linha in linhas]
    return links


async def main(urls: list):
    tasks = []
    chunk_size = len(urls) // 4
    url_chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]
    for chunk in url_chunks:
        tasks.append(asyncio.create_task(process_chunk(chunk)))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    arquivo = ler_arquivo_links('arquivo.txt')
    asyncio.get_event_loop().run_until_complete(main(arquivo))
    print('olhe a pasta logs para verificar os erros')
