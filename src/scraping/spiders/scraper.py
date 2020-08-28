import scrapy
import pandas as pd

iid = 0

def next_id():
    global iid
    res = iid
    iid += 1
    return res

class MetacriticItem(scrapy.Item):
    ID = scrapy.Field()
    title = scrapy.Field()
    img = scrapy.Field()
    comment = scrapy.Field()
    rating = scrapy.Field()

class MetacriticSpider(scrapy.Spider):
    name = 'metacritic'
    allowed_domains = ['metacritic.com']
    start_urls = ['https://www.metacritic.com/movie/the-adventures-of-sharkboy-and-lavagirl-3-d']
    index = 1

    def parse(self, response):
        item = MetacriticItem()
        item["ID"] = self.index
        self.index += 1
        item['title'] = response.xpath('//div[@class="product_page_title oswald"]/h1/text()').extract_first()
        item['img'] = response.xpath('//img[@class="summary_img"]/@src').extract_first()
        yield item
        yield scrapy.Request(response.request.url + '/user-reviews', self.parse2)
        
    def parse2(self, response):
        movie_data = pd.read_csv(r'C:\Users\Ryan\Downloads\movie_urls.csv')
        next_urls = movie_data['urls'].unique().tolist()
        
        for div in response.xpath('//div[@class="review pad_top1"]'):
            
            item = MetacriticItem()
            if div.xpath('.//span[@class="blurb blurb_expanded"]'):
                item['comment'] = div.xpath('.//span[@class="blurb blurb_expanded"]/text()').extract_first()
            else:
                item['comment'] = div.xpath('.//div[@class="review_body"]/span/text()').extract_first()
                
            if div.xpath('.//div[@class="metascore_w user large movie positive indiv perfect"]'):
                item['rating'] = div.xpath('//div[@class="metascore_w user large movie positive indiv perfect"]/text()').extract_first()
            elif div.xpath('.//div[@class="metascore_w user large movie positive indiv"]'):
                item['rating'] = div.xpath('.//div[@class="metascore_w user large movie positive indiv"]/text()').extract_first()
            elif div.xpath('.//div[@class="metascore_w user large movie mixed indiv"]'):
                item['rating'] = div.xpath('.//div[@class="metascore_w user large movie mixed indiv"]/text()').extract_first()
            else:
                item['rating'] = div.xpath('.//div[@class="metascore_w user large movie negative indiv"]/text()').extract_first()
            yield item
            
        next_page = response.css('a[rel="next"] ::attr(href)').extract_first()
        if next_page is not None:
            request = response.follow(next_page, callback=self.parse2)
            yield request
        else:
            yield scrapy.Request(next_urls[next_id()], self.parse)