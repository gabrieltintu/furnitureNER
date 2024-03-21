import requests
from bs4 import BeautifulSoup
import csv
import os

# scrape text content from a URL
def scrape_url(url):
	try:
		response = requests.get(url)

		# check if the request was successful
		if response.status_code == 200:
			# parse the HTML content of the webpage
			soup = BeautifulSoup(response.content, 'html.parser')

			# extract text from the webpage
			text = soup.get_text()

			# filter empty lines
			lines = text.split('\n')
			non_empty_lines = [line.strip() for line in lines if line.strip()]
			text = '\n'.join(non_empty_lines)

			return text
		else:
			return None
	except requests.exceptions.RequestException as e:
		return None
	except socket.gaierror as e:
		return None


def get_urls_from_csv(csv_file):
	working_urls = []
	not_working_urls = []

	with open(csv_file, 'r', newline='') as csvfile:
		csv_reader = csv.reader(csvfile)
		file_idx = 1
		for idx, row in enumerate(csv_reader):
			url = row[0]
			webpage_text = scrape_url(url)
			if webpage_text:
				# save the scraped text to a file
				output_file = os.path.join("html_to_txt", f"text_{file_idx}.txt")
				file_idx += 1
				with open(output_file, "w", encoding="utf-8") as file:
					file.write(webpage_text)
				print(f"Text scraped from {url} successfully saved to {output_file}")
				working_urls.append(url)
			else:
				print(f"Text scraping failed for {url}.")
				not_working_urls.append(url)
			

	# write not working URLs to a file
	not_working_urls_file = os.path.join("html_to_txt", "not_working_urls.txt")
	with open(not_working_urls_file, 'w') as file:
		for url in not_working_urls:
			file.write(url + '\n')

	return working_urls

csv_file_path = "urls.csv"

working_urls = get_urls_from_csv(csv_file_path)

print("Extraction completed.")

print("Working URLs:")
for url in working_urls:
	print(url)