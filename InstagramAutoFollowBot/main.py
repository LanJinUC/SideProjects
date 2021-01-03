from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
import time
CHROME_DRIVER_PATH = "chromedriver path on your local computer"
SIMILAR_ACCOUNT = "THE INFLUNCER'S ACCOUNT"
USERNAME = "YOUR USERNAME"
PASSWORD = "YOUR PASSWORD"

class InstaFollower:

    def __init__(self, path):
        self.driver = webdriver.Chrome(executable_path=path)


    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(5)

        username = self.driver.find_element_by_name("username")
        password = self.driver.find_element_by_name("password")

        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)

        time.sleep(2)
        password.send_keys(Keys.ENTER)

    def find_followers(self):
        time.sleep(5)
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}")

        time.sleep(2)
        followers = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
        followers.click()

        time.sleep(2)
        modal = self.driver.find_element_by_xpath('/html/body/div[5]/div/div')
        for i in range(10):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            print(i)
            time.sleep(1)

    def follow(self):
        all_buttons = self.driver.find_elements_by_css_selector("li button")
        # find all li elements in list
        fBody = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        scroll = 0
        while scroll < 5:  # scroll 5 times
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
            time.sleep(2)
            scroll += 1

        fList = self.driver.find_elements_by_xpath("//div[@class='isgrP']//li")
        for button in all_buttons:
            try:
                button.click()
                print("click button")
                time.sleep(1)
            except ElementClickInterceptedException:
                time.sleep(2)
                cancel_button = self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[3]/button[1]')
                cancel_button.click()


        print("fList len is {}".format(len(fList)))

        print("ended")
        # driver.quit()

    def getUserFollowers(self, username, max):
        self.driver.get('https://www.instagram.com/' + username)
        followersLink = self.driver.find_element_by_css_selector('ul li a')
        followersLink.click()
        time.sleep(2)
        followersList = self.driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))

        followersList.click()
        actionChain = webdriver.ActionChains(self.driver)
        while (numberOfFollowersInList < max):
            fBody = self.driver.find_element_by_xpath("//div[@class='isgrP']")
            scroll = 0
            while scroll < 100:  # scroll 5 times
                self.driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
                time.sleep(0.3)
                scroll += 1
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
            print(numberOfFollowersInList)

        followers = []
        all_buttons = self.driver.find_elements_by_xpath("//button[contains(.,'Follow')]")
        for button in all_buttons:
            try:
                button.click()
                print("click button")
                time.sleep(2)
            except ElementClickInterceptedException:
                time.sleep(2)
                cancel_button = self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[3]/button[1]')
                cancel_button.click()
        # for user in followersList.find_elements_by_css_selector('li'):
        #     userLink = user.find_element_by_css_selector('a').get_attribute('href')
        #     print(userLink)
        #     followers.append(userLink)
        #     if (len(followers) == max):
        #         break
        # return followers


bot = InstaFollower(CHROME_DRIVER_PATH)
bot.login()
bot.find_followers()
bot.getUserFollowers(SIMILAR_ACCOUNT, 50)
