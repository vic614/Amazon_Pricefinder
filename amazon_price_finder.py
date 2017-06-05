#! usr/bin/env python

def pricefinder(text):
    import re
    re_object = re.compile(r'<span class=\"a-size-medium a-color-price" id=\"priceblock_ourprice\">\$[0-9.,]*')
    rawprice = re_object.search(str(text))
    if rawprice:
        price = rawprice.group().split('$')[1]
        return price
    else:
        return '0.00'
def titlefinder(text):
    import re
    object_text = re.compile(r'Simpli Home[\w\s,".()]*')
    b = str(text.title)
    a = object_text.search(b)
    c = 'Please check Title'
    if a:
         return a.group()
    else:
         return c
def skufinder(soup):
    import re
    b = str(soup)
    a = re.sub(' ','',b)
    sku_object = re.compile(r'Itemmodelnumber\n</th>\n<tdclass="a-size-base">\n[\w\-\d]*')
    i = sku_object.search(a)
    sku = i.group().split('\n</th>\n<tdclass="a-size-base">\n')[1]
    return sku
def searcher(product = ''):
    import requests
    import random
    from bs4 import BeautifulSoup
    import random
    i = random.randint(3,5)
    j=random.randint(40,53)
    x=random.randint(2,13)
    url_base = 'https://www.amazon.com/gp/product/'
    headers ={
        'User-Agent':'Mozilla/'+str(i)+'.0 (Macintosh; Intel Mac OS X 10.'+str(x)+'; rv:53.0) Gecko/20100101 Firefox/'+str(j)+'.0'
                }
    r = requests.get(url_base+product,headers=headers)
    soup = BeautifulSoup(r.text,'html.parser')
    price = pricefinder(soup)
    title = titlefinder(soup)
    sku = skufinder(soup)
    info = sku,price,title
    return list(info)

def main():
    import pandas
    data = pandas.read_csv('productASIN.csv', header = 0)
    ASIN = list(data.ASIN)
    SKU = list(data.SKU)
    import xlsxwriter
    workbook = xlsxwriter.Workbook('Amazonaudit.xlsx',{'constant_memory':True})
    worksheet = workbook.add_worksheet()
    worksheet.write(0,0,'SKU')
    worksheet.write(0,1,'Status')
    worksheet.write(0,2,'Current_price')
    worksheet.write(0,3,'Title_showing_on_site')
    row = 1
    format1 = workbook.add_format()
    format1.set_num_format('#,##0.00')
    for i in range(0,len(data.index)-1):
        a = searcher(ASIN[i])
        if a[0] == SKU[i]:
            print(a)
            worksheet.write(row,0,a[0])
            worksheet.write(row,1,'Online') 
            worksheet.write(row,2,a[1],format1)
            worksheet.write(row,3,a[2])
            row += 1
        else:
            print(SKU[i],'is offline')
            worksheet.write(row,0,SKU[i])
            worksheet.write(row,1,'Offline')
            worksheet.write(row,2,'0.00',format1)
            worksheet.write(row,3,'')
            row += 1
    workbook.close()
    
main()
