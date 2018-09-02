from bs4 import BeautifulSoup
import scrapy

class BroadwaySpider(scrapy.Spider):
	name = "broadway"

	def start_requests(self):
		yield scrapy.Request('https://www.broadwayworld.com/grosses.cfm', self.parse1)

	dates = []

	def parse1(self, response):
		soup = BeautifulSoup(response.text, "lxml")
		# Get the 520 dates into the list
		datelist = soup.find('select', {'name':'days'}).find_all('option')
		datelist = datelist[:1040]
		for date in datelist:
			self.dates.append(date.get_text())
		
		self.dates.sort(reverse=True)
		self.log(self.dates)
		for date in self.dates:
			yield scrapy.FormRequest('https://www.broadwayworld.com/grosses.cfm', formdata={'days':date}, callback=self.parse2, meta={'date':date})

	def parse2(self, response):
		soup = BeautifulSoup(response.text, "lxml")
		table = soup.find('table').find('table').find_next_sibling('table')
		trs = table.find_all('tr', {'onmouseover':"style.backgroundColor='#FFFF99';"})
		for tr in trs:
			show = {}
			tds = tr.find_all('td')
			show['week'] = response.meta['date']
			show['name'] = tds[0].find('b').get_text().strip()
			show['grosses'] = tds[1].get_text().strip()
			show['potential_gross'] = tds[4].get_text().strip()
			show['grosses_percentage'] = tds[5].get_text().strip()
			show['average_ticket'] = tds[6].get_text().strip()
			show['top_ticket'] = tds[7].get_text().strip()
			show['seat_sold'] = tds[8].get_text().strip()
			show['total_seat'] = tds[9].get_text().strip()
			show['per'] = tds[10].get_text().strip()
			show['seat_percentage'] = tds[11].get_text().strip()
			yield show
