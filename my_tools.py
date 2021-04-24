from bs4 import BeautifulSoup
import re
from threading import Thread
import fileinput
import cloudscraper
import json


class MyTools():

    def __init__(self, filename='websites.txt'):
        self.filename = filename
        self.all_sites = []
        self.full_info = None
        self.json_full_info = None

    def get_filename(self):
        return self.filename

    def set_all_sites(self, site_list):
        self.all_sites = site_list

    def get_all_sites(self):
        return self.all_sites

    def read_file_input(self, file_input):
        site_list = []
        for row in file_input:
            site = row.split('\n')[0].strip()
            site_list.append(site)
        self.set_all_sites(site_list=site_list)

    def read_filename(self):
        with open(self.filename, 'r') as f:
            read = f.read()
            site_list = read.split('\n')
            if not site_list[-1]:
                site_list = site_list[:-1]
            self.set_all_sites(site_list=site_list)

    def get_response(self, url):
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        return response

    def get_site_html(self, url):
        try:
            response = self.get_response(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        except Exception as e:
            #print(e)
            pass

    def set_output(self, url, phones, logo):
        output = {
            'logo': logo,
            'phones': phones,
            'website': url
        }
        return output

    def get_logo(self, page, url):
        try:
            body = page.find('body')
            img = body.find('img')
            try:
                source = img['src']
            except:
                txt_img = img.decode()
                source = txt_img.split('src="')[1].split('"')[0]
            try:
                response = self.get_response(source)
            except:
                u = url.split('//')
                root = u[1].split('/')[0]
                final_root = u[0] + r'//' + root
                source = final_root + source
            return source
        except Exception as e:
            #print(e)
            return ''

    def list_regex(self):
        regex = [
            "\+{0,1}\s{0,1}\d{0,5}\s{0,1}\({0,1}\d{0,5}\){0,1}\s{0,1}\d{1,5}\-{0,1}\s*\d{0,5}\-{0,1}\s{0,1}\d{0,5}"]
        return regex

    def find_phone_list(self, page):
        regex = self.list_regex()
        phone_list = []
        for item in regex:
            phones = re.findall(item, page)
            for phone in phones:
                if len(phone.strip()) > 7:
                    clear_phone = phone.replace('-', ' ').replace('/', ' ')
                    phone_list.append(clear_phone.strip())
        return phone_list

    def sub_process(self, url, all_sites_info, index):
        page = self.get_site_html(url)
        phones = self.find_phone_list(page.text)
        logo = self.get_logo(page, url)
        output_infos = self.set_output(url, phones, logo)
        all_sites_info[index] = output_infos

    def get_all_sites_info(self):
        if not self.all_sites:
            self.read_filename()
        all_urls = self.all_sites

        # All memory slots is created now in list below, to be possible works simultaneously within multi thread process
        all_sites_info = [None for _ in range(len(all_urls))]
        thread_list = []
        for index, url in enumerate(all_urls):
            try:
                x = Thread(target=self.sub_process, args=(url, all_sites_info, index))
                thread_list.append(x)
                x.start()
            except Exception as e:
                #print(e)
                pass
        for item in thread_list:
            item.join()

        json_all_sites_info = json.dumps(all_sites_info)
        self.set_json_full_info(json_all_sites_info)
        self.set_full_info(all_sites_info)

    def set_full_info(self, all_sites_info):
        self.full_info = all_sites_info

    def set_json_full_info(self, json_all_sites_info):
        self.json_full_info = json_all_sites_info

    def get_full_info(self):
        return self.full_info

    def print_full_info(self):
        for info in self.get_full_info():
            print(info)


if __name__ == '__main__':
    file_input = fileinput.input()
    tool = MyTools()
    tool.read_file_input(file_input)
    tool.get_all_sites_info()
    tool.print_full_info()
