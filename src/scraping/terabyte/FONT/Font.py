import arrow
from selenium import webdriver


def Font_Crawl():
    # Font specific data

    installmentPriceProducts = []          # Font Installment Prices
    pricesProducts = []                    # Font Prices
    namesProducts = []                     # Font Name
    linksProducts = []                     # Font Links
    imgProducts = []                       # Font Image
    local = arrow.utcnow()                 # Scraping date and time
    allData = []                           # Font all data

    # WEB CRAWLER

    driver = webdriver.Chrome()
    link = 'https://www.terabyteshop.com.br/hardware/fontes'
    driver.get(link)

    # Crawling Products == Image
    product = driver.find_elements('tag name', 'img')
    for e in product:
        if 'produto' in e.get_attribute('src'):  # Only separate images with product in the name
            imgProducts.append(e.get_attribute('src'))
    imgProducts = list(dict.fromkeys(imgProducts))

    # Crawling Products == Price
    product = driver.find_elements('class name', 'prod-new-price')  # Possibles class name = jss191, jss69
    for i in product:
        if 'R$' in i.text:
            pricesProducts.append(i.text)

    # Crawling Products == Installment Price
    product = driver.find_elements('class name', 'prod-juros')  # Possibles class name = jss199, jss77
    for i in product:
        installmentPriceProducts.append(i.text)

    # Crawling Products == Name
    product = driver.find_elements('tag name', 'h2')
    for i in product:
        if i.text == "":
            continue
        namesProducts.append(i.text)

    # Crawling Products == Links
    links = driver.find_elements('tag name', 'a')
    for i in links:
        if 'produto' in i.get_attribute('href'):
            linksProducts.append(i.get_attribute('href'))
    linksProducts = list(dict.fromkeys(linksProducts))
    driver.close()

    # Separating data in dictionary for better reading
    for i in range(len(installmentPriceProducts)):
        installmentPrice = installmentPriceProducts[i].split()
        if '.' in installmentPrice[3]:
            installmentPrice[3] = installmentPrice[3].replace('.', '')
        installmentPrice = float(installmentPrice[0].replace('x', '')) * float(installmentPrice[3].replace(',', '.'))
        if '.' in pricesProducts[i]:
            pricesProducts[i] = pricesProducts[i].replace('.', '')
        changeablePrices = pricesProducts[i].replace('R$', '').replace(',', '.').replace(' à vista', '')
        dataDic = {'Store': 'Terabyte', 'Name': namesProducts[i], 'Price': [pricesProducts[i], float(changeablePrices)],
                   'Installment price': [f'R${round(float(installmentPrice), 2)}', round(float(installmentPrice), 2)],
                   'Link': linksProducts[i], 'Image': imgProducts[i], 'Time': local.format('YYYY-MM-DD HH:mm:ss'),
                   'Logo': 'https://img.terabyteshop.com.br/terabyte-logo.svg', 'Type': 'Font',  'Model': '', 'Format': '',
                   'Discount': '', 'Old Prices': '',
                   'Interface': '', 'Capacity': '', 'DDR': '', 'Frequency': '', 'Platform': '', 'Color': ''}
        allData.append(dataDic)
    return allData
