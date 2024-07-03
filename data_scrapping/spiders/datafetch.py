import scrapy
import json
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    base_url = "https://www.bayut.com"
    start_urls = ['https://www.bayut.com/to-rent/property/dubai/']
    
    def parse(self, response):
        link_elements = response.css('.dde89f38 a')

        for link_element in link_elements:
            link_url = self.base_url + link_element.attrib.get('href')
            yield scrapy.Request(link_url, callback=self.parse_currency_price)
        
        next_page = response.css('ul._48341ab4 li a[title="Next"]::attr(href)').get()

        if next_page:
            next_page_url = self.base_url + next_page
            yield response.follow(next_page_url, self.parse)
        
    def parse_currency_price(self, response):
        currency = response.css('span[aria-label="Currency"]')
        amount = response.css('span[aria-label="Price"]')
        RefNo = response.css('span[aria-label="Reference"]')
        purpose = response.css('span[aria-label="Purpose"]')
        type = response.css('span[aria-label="Type"]')
        added_on = response.css('span[aria-label="Reactivated date"]') 
        furnishing = response.css('span[aria-label="Furnishing"]')
        location = response.css('div[aria-label="Property header"]')
        beds =  response.css('span[aria-label="Beds"]')
        baths = response.css('span[aria-label="Baths"]')
        area = response.css('span[aria-label="Area"]')
       
        agent_info = response.xpath('//span[@class="_4c376836"]')
        agent_name = agent_info.xpath('.//a/text()').get()
        description = response.xpath('//span[@class="_3547dac9"]//text()').getall()
        image  = response.xpath('//picture[@class="a659dd2e"]//img/@src').get()
        script_data = response.xpath('//div[@class="_3624d529"]//script/text()').get()
        breadcrumb_json = json.loads(script_data)  

        breadcrumbs = []
        for item in breadcrumb_json['itemListElement']:
            breadcrumbs.append(item['name'])

        breadcrumb_string = " > ".join(breadcrumbs)
      
       
        # Extract the text content of the elements
        currency_value = currency.css('::text').get()
        amount_value = amount.css('::text').get()
        Refno_value = RefNo.css('::text').get()
        purpose_value = purpose.css('::text').get()
        type_value = type.css('::text').get()
        added_on_value = added_on.css('::text').get()
        furnishing_value = furnishing.css('::text').get()
        location_value = location.css('::text').get()
        beds_value = beds.css('::text').get()
        baths_value =baths.css('::text').get()
        area_value = area.css('::text').get()
        joined_description = ''.join(description).strip()
        yield {
            'property_id':Refno_value,
            'purpose':purpose_value,
            'type':type_value,
            'added_on':added_on_value,
            'furnishing':furnishing_value, 
            'price': {
                'currency': currency_value,
                'amount':amount_value
                },
            'location':location_value,
            'bed_bath_size':{
                'bedrooms': beds_value,
                'bathrooms': baths_value,
                'size': area_value
                },
            'permit_number':'',
            'agent_name':agent_name,
            'image_url':image,
            'breadcrumbs':breadcrumb_string,
            'description':joined_description
            }
