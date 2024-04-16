import asyncio
import random
from pyppeteer import launch


async def captura(url: str, name: str, pasta: str) -> None:
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'load'})
    await page.setViewport({'width': 1080, 'height': 2000})
    await page.screenshot({'path': f'./screnshots/{pasta}/{name}.png'})
    with open(f'./html/{pasta}/{name}.html', 'w', encoding='utf-8') as arquivo:
        arquivo.write(await page.content())
    await browser.close()


async def process_chunk(chunk, pasta: str) -> None:
    erros: str = ''
    nome: int = random.randint(1, 100)
    print(f'ola do processo {nome}')
    for url in chunk:
        i: str = url.split('/')[2]
        print(f'processo {nome} esta buscando {i}')
        i = i.replace('.', '-')
        try:
            await captura(url, i, pasta)
        except(Exception) as e:
            erros = erros + f'Erro no site {i} string do erro: {str(e)}'
            print(f'Error {i} passando para o proximo')
    if erros:
        with open(f'./logs/log-processo-{nome}.txt', 'w') as arquivo:
            arquivo.write(erros)


def ler_arquivo_links(nome_arquivo) -> list:
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        links = [linha.strip() for linha in linhas]
    return links


async def main(urls: list, pasta: str) -> None:
    tasks = []
    chunk_size = len(urls) // 4
    url_chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]
    for chunk in url_chunks:
        tasks.append(asyncio.create_task(process_chunk(chunk, pasta)))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    arquivo = ler_arquivo_links('arquivo.txt')
    muda = False
    minimalistas = []
    coloridos = []
    for url in arquivo:
        if url.startswith('#'):
            muda = True
            continue
        if muda:
            coloridos.append(url)
        else:
            minimalistas.append(url)
    print('iniciando processos')
    print('minimalistas')
    asyncio.get_event_loop().run_until_complete(main(minimalistas, 'minimalista'))
    print('coloridos')
    asyncio.get_event_loop().run_until_complete(main(coloridos, 'coloridos'))
    print('olhe a pasta logs para verificar os erros')
