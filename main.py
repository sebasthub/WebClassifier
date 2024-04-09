import asyncio
import random
from pyppeteer import launch


async def captura(url: str, name: str):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'load'})
    await page.screenshot({'path': f'./screnshots/{name}.png', 'fullPage': True})
    with open(f'./logs/{name}.html', 'w', encoding='utf-8') as arquivo:
        arquivo.write(await page.content())
    await browser.close()


lista: list = ['https://www.muji.us/',
'https://hay.dk/country-selector?redirect=%2fpt%2f',
'https://www.cos.com/en/index.html',
'https://www.etiquetaunica.com.br/uniqlo',
'https://www.naturaeco.com/pt-br/marcas/aesop-2/',
'https://www.stories.com/en/index.html',
'https://www.weekday.com/en/index.html',
'https://www.arket.com/en/index.html',
'https://monocle.com/'
'https://robinhood.com/creditcard/?referral_code=4a1fa686',
'https://www.kinfolk.com/',
'https://www.newyorker.com/',
'https://www.theatlantic.com/world/',
'https://www.theguardian.com/international',
'https://www.nytimes.com/',
'https://www.lemonde.fr/',
'https://elpais.com/america/',
'https://www.folha.uol.com.br/',
'https://oglobo.globo.com/',
'https://medium.com/',
'https://substack.com/home-i',
'https://github.com/',
'https://about.gitlab.com/',
'https://www.dropbox.com/pt_BR/',
'https://www.google.com/intl/pt-br/drive/about.html',
'https://open.spotify.com/intl-pt',
'https://www.apple.com/br/apple-music/',
'https://vimeo.com/'
]


async def main():
    tasks = []
    chunk_size = len(lista) // 4
    url_chunks = [lista[i:i + chunk_size] for i in range(0, len(lista), chunk_size)]
    for chunk in url_chunks:
        tasks.append(asyncio.create_task(process_chunk(chunk)))

    await asyncio.gather(*tasks)


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


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    print('olhe a pasta logs para verificar os erros')