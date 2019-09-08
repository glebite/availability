#!/usr/bin/python
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import getopt, sys
import ast


class Availability:
    def __init__(self, user_name, user_pin, nodes):
        self.firefox_profile = webdriver.FirefoxProfile()
        self.web_driver = webdriver.Firefox(firefox_profile=self.firefox_profile)

        self.user_barcode = user_name
        self.user_pin = user_pin
        self.nodes = ast.literal_eval(nodes)
        
        self.base_url = "https://biblioottawalibrary.ca"
        self.node_modifier = "/en/node/"

        self.login_button_text = "Log In "
        self.login_register_button_text = "Log In / Register"

        self.user_name_id = "user_name"
        self.user_pin_id = "user_pin"
        self.user_login_button_name = "commit"

        self.availability_link_text = "View availability for the next 6 days"

    def connect(self):
        self.web_driver.get(self.base_url)

    def close(self):
        self.web_driver.quit()
        
    def login(self):
        self.web_driver.find_element_by_xpath('//button[contains(text(), "{}")]'.format(self.login_button_text)).click()
        time.sleep(2)
        self.web_driver.find_element_by_xpath('//a[contains(text(), "{}")]'.format(self.login_register_button_text)).click()
        time.sleep(2)
        self.web_driver.find_element_by_id(self.user_name_id).send_keys(self.user_barcode)
        self.web_driver.find_element_by_id(self.user_pin_id).send_keys(self.user_pin)
        self.web_driver.find_element_by_name(self.user_login_button_name).click()
        time.sleep(2)
        
    def get_availability(self, node_id):
        print('Machine: {}'.format(node_id))
        self.web_driver.get(self.base_url + self.node_modifier + node_id + "/schedule")
        
        self.web_driver.find_element_by_xpath('//a[contains(text(), "{}")]'.format(self.availability_link_text)).click()

        available_tables = self.web_driver.find_elements_by_xpath('//table')
        for table in available_tables:
            if table:
                table_soup = BeautifulSoup(table.get_attribute('innerHTML'), 'lxml')
                caption = table_soup.find('caption')
                available_rows = table.find_elements_by_xpath('.//tr[@class="form-opl-booking-row-available"]')
                if available_rows:
                    if caption:
                        print(caption.contents[0])
                    for row in available_rows:
                        tds_soup = BeautifulSoup(row.get_attribute('innerHTML'), 'lxml')
                        td_fields = tds_soup.find_all('td')
                        print("\t{} to {}".format(td_fields[1].text, td_fields[2].text))

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "u:p:n:", ["user", "password", "nodes"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    username = None
    password = None
    nodes = None

    for o, a in opts:
        if o == "-u":
            username = a
        elif o == "-p":
            password = a
        elif o == "-n":
            nodes = a
        else:
            assert False, "unhandled option"

    ott_library = Availability(username, password, nodes)
    ott_library.connect()
    ott_library.login()
    for each_node in ott_library.nodes:
        ott_library.get_availability(each_node)
    ott_library.close()

if __name__=="__main__":
    main()
