#!/usr/bin/python
"""
availability.py - checks for device availability at the library
"""
import time
import getopt
import sys
import ast
from selenium import webdriver
from bs4 import BeautifulSoup


class Availability:
    """
    Availability class - TBD
    """
    base_url = "https://biblioottawalibrary.ca"
    node_modifier = "/en/node/"
    login_button_text = "Log In "
    login_register_button_text = "Log In / Register"
    user_name_id = "edit-name"
    user_pin_id = "edit-user-pin"
    user_login_button_name = "edit-submit"
    availability_link_text = "future-availability-body"

    login_xpath_match = '//button[contains(text(), "{}")]'

    def __init__(self, user_name, user_pin, nodes):
        """
        __init__ - let's spark this up!
        """
        self.firefox_profile = webdriver.FirefoxProfile()
        self.web_driver = webdriver.Firefox(firefox_profile=self.firefox_profile)

        self.user_barcode = user_name
        self.user_pin = user_pin
        self.nodes = ast.literal_eval(nodes)

    def connect(self):
        """
        connect - strangely doesn't connect at times.  Might put in some other
                  magic code for later to check this.  Might not...
        """
        self.web_driver.get(self.base_url)

    def close(self):
        """
        close - quit the drivers
        """
        self.web_driver.quit()

    def login(self):
        """
        login - login function - barcode, pin, press buttton
        """

        self.web_driver.find_element_by_xpath(self.login_xpath_match.
                                              format(self.login_button_text)).click()
        time.sleep(5)
        # TODO: change this up to the top
        xpath_match = '//a[contains(text(), "{}")]'

        self.web_driver.find_element_by_xpath(xpath_match.
                                              format(self.login_register_button_text)).click()
        # TODO: replace with element availability (reducing time)
        time.sleep(5)
        self.web_driver.find_element_by_id(self.user_name_id).send_keys(self.user_barcode)
        self.web_driver.find_element_by_id(self.user_pin_id).send_keys(self.user_pin)
        self.web_driver.find_element_by_id(self.user_login_button_name).click()
        # TODO: replace with element availability (reducint time)
        time.sleep(5)

    def get_availability(self, node_id):
        """
        get_availability - navigate to the page, parse tables, dump to screen
        """
        found_rows = False
        print('Machine: {}'.format(node_id))
        self.web_driver.get(self.base_url + self.node_modifier + node_id + "/schedule")
        # TODO: move it all up!!!
        xpath_match = '//a[contains(@href, "{}")]'
        self.web_driver.find_element_by_xpath(xpath_match.
                                              format(self.availability_link_text)).click()

        # TODO: move it up!
        available_tables = self.web_driver.find_elements_by_xpath('//table')
        for table in available_tables:
            if table:
                table_soup = BeautifulSoup(table.get_attribute('innerHTML'), 'lxml')
                caption = table_soup.find('caption')
                # TODO: move this up too!  ugly!!!
                xpath_match = './/tr[@class="form-opl-booking-row-available"]'
                available_rows = table.find_elements_by_xpath(xpath_match)
                if available_rows:
                    found_rows = True
                    if caption:
                        print(caption.contents[0])
                    for row in available_rows:
                        tds_soup = BeautifulSoup(row.get_attribute('innerHTML'), 'lxml')
                        td_fields = tds_soup.find_all('td')
                        print("\t{} to {}".format(td_fields[1].text, td_fields[2].text))
                else:
                    found_rows = False
        if not found_rows:
            print("\tNone Found")

def usage():
    """
    Basic usage - output how to use this tool.
    """
    print("python ./availability.py -u barcode -p pin -n nodes")

def main():
    """
    main function - parse options, create instance, and do it!
    """
    try:
        opts, _ = getopt.gnu_getopt(sys.argv[1:], "u:p:n:", ["user", "password", "nodes"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    username = None
    password = None
    nodes = None

    for option_tag, arg_tag in opts:
        if option_tag == "-u":
            username = arg_tag
        elif option_tag == "-p":
            password = arg_tag
        elif option_tag == "-n":
            nodes = arg_tag
        else:
            assert False, "unhandled option"

    ott_library = Availability(username, password, nodes)
    ott_library.connect()
    ott_library.login()
    for each_node in ott_library.nodes:
        ott_library.get_availability(each_node)
    ott_library.close()

if __name__ == "__main__":
    main()
