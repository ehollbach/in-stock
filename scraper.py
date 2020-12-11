import asyncio
import json
import logging
from slacker import notify_channel
from tornado.httpclient import AsyncHTTPClient
from selenium import webdriver

driver = webdriver.Safari()


with open('config.json') as f:
	config = json.load(f)

http_client = AsyncHTTPClient()


class Task:
	def __init__(self, config) -> None:
		super().__init__()

		self.url = config['url']
		self.store = config['store']
		self.rule = config['rule']

		self.logger = logging.getLogger(self.store)
		self.headers = self._init_headers()

	def _init_headers(self):
		driver.get(self.url)
		cookies = driver.get_cookies()
		cookie_str = ";".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

		return {'Cookie': cookie_str}

	async def scrape(self):
		resp = await http_client.fetch(self.url, headers=self.headers)
		self.logger.info(f"{self.url}\t{resp.code}")

		if self.rule == "redirect":
			pass
		elif self.rule == "xpath":
			pass


async def main():
	tasks = []
	for obj in config:
		task = Task(obj)
		tasks.append(task)
	driver.close()  # Done setting cookies
	while True:
		for task in tasks:
			asyncio.create_task(task.scrape())
		await asyncio.sleep(3)


if __name__ == "__main__":
	asyncio.run(main())
