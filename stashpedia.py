import discord
import requests
import bs4 as bs
import urllib.parse
import re

"""

@FunkoFucked at it again - All y'all other groups keep being late, I had this shit made LAST YEAR.

Stop flexing stupid shit like this in your shitty washed groups where you charge people way too much, 
this is literally 12 minutes/76 lines of code while I had katyelisehenry shaking her ass in the background.

"""
r = requests.session()

search_url = 'https://stashpedia.com/search?terms='
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.60 FunkoFuckedTookStock'
}

client = discord.Client()
token = 'NDcyMTc3MTcxODI2MjFunkoFuckedTookStockbP5gA1lYDHNUFOAoENGM'


@client.event
async def on_ready():
    print('{} started - FunkoFucked says hi :)'.format(client.user.name))

def site_search(keyword):
    product_urls = []
    keyword = urllib.parse.quote_plus(keyword)
    search_query = search_url + f'{keyword}'
    print(search_query)
    search_result = r.get(search_query, headers = headers)
    soup = bs.BeautifulSoup(search_result.text, 'lxml')
    # Find search result URLs
    for find_url in soup.find_all('a', {'class': 'fill-height'}):
        url = find_url.get('href')
        url = f'https://stashpedia.com{url}'
        product_urls.append(url)
    first_result = product_urls[0]

    return first_result

def site_result(url):
    result_parse = r.get(url, headers = headers)
    soup = bs.BeautifulSoup(result_parse.text, 'lxml')
    product_name = soup.find('img', {'id': 'mainImage'}).get('alt')
    # for whatever reason, bs4 is not picking up H1 and H2 tags. that or i may have been dropped as a baby or somethin... extremely greedy regex will do for now
    product_type = re.findall(r'''class="productTypeText">(.*)?<''', result_parse.text)
    product_type = product_type[0]
    product_img = soup.find('img', {'id': 'mainImage'}).get('src')
    product_img = 'https://stashpedia.com' + product_img
    # you can keep adding more stuff here
    product_category = soup.find('div', {'itemprop': 'category'}).get_text()
    product_price = re.findall(r'''class="valueText">(.*)?<''', result_parse.text)
    product_price = product_price[0]
    return product_name, product_type, product_img, product_category, product_price


@client.event
async def on_message(message):
    if message.content.startswith('.stash '):
        keyword = message.content.split('.stash ')[1]
        url = site_search(keyword)
        name, _type, image, category, price =  site_result(url)
        embed = discord.Embed(color=15691628)
        embed.set_thumbnail(url=image)
        embed.add_field(name="Product Name", value="[{}]({})".format(name, url), inline=False)
        embed.add_field(name="Trending at", value="{}".format(price), inline=True)
        embed.add_field(name="Category", value="{}".format(category), inline=True)
        embed.add_field(name="Who took stock?", value="FunkoFucked did", inline=True)

        await client.send_message(message.channel, embed=embed)

client.run(token)