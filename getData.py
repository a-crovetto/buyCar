import scrapy
from scrapy.http import HtmlResponse
from cryptography.hazmat.bindings._openssl import ffi, lib

# http://autos.mercadolibre.com.uy/montevideo/_OrderId_PRICE_YearRange_1995-0_PriceRange_62000-320000
# _Desde_100000
product_url=''

class HousingSpider(scrapy.Spider):
    name = "searchResults"
    # allowed_domains = ["housing.com"]
    start_urls = (
        'http://autos.mercadolibre.com.uy/montevideo/_OrderId_PRICE_YearRange_1995-0_PriceRange_62000-320000'
    )
    custom_settings = {'USER_AGENT' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'}

    def parse_item(self, response):
        hrefs = response.selector.css("a")
        print hrefs
    # yield { 'url': response.url,'script length': len(script),    'script': script,    }
#response = HtmlResponse(url='http://stackoverflow.com/questions/27323740/scrapy-convert-html-string-to-htmlresponse-object')
#searchResults

#searchResults .article .rowItem .list-view-item-title a

#response = HtmlResponse(url='http://autos.mercadolibre.com.uy/montevideo/_OrderId_PRICE_YearRange_1995-0_PriceRange_62000-320000')

#searchResults .article .rowItem .list-view-item-title a::attr(href)
