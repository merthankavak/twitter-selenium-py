from twitterUserInfo import username, password
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class Twitter:
    def __init__(self, username, password):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option(
            'prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome(
            'chromedriver.exe', chrome_options=self.browserProfile)
        self.browser.maximize_window()
        self.username = username
        self.password = password

    # Twitter sign in
    def signIn(self):
        self.browser.get('https://twitter.com/login')
        time.sleep(2)
        usernameInput = self.browser.find_element_by_xpath(
            "//*[@id='react-root']/div/div/div[2]/main/div/div/div[1]/form/div/div[1]/label/div/div[2]/div/input")
        passwordInput = self.browser.find_element_by_xpath(
            "//*[@id='react-root']/div/div/div[2]/main/div/div/div[1]/form/div/div[2]/label/div/div[2]/div/input")

        usernameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        time.sleep(2)
        passwordInput.send_keys(Keys.ENTER)  # Push enter button for loggin
        time.sleep(2)

    # Search tweets by hashtag
    def search(self, hashtag):
        searchInput = self.browser.find_element_by_xpath(
            "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div[2]/input")
        searchInput.send_keys(hashtag)
        time.sleep(2)
        searchInput.send_keys(Keys.ENTER)  # Push enter button for searching
        time.sleep(2)

        results = []
        tweetLink = self.browser.find_elements_by_xpath(
            "//div[@data-testid='tweet']/div[2]/div[1]/div/div/div[1]/a")
        tweetList = self.browser.find_elements_by_xpath(
            "//div[@data-testid='tweet']/div[2]/div[2]/div[1]/div")
        time.sleep(2)
        print(f"Number of Tweet : {len(tweetList)}")

        for i in range(len(tweetList)):
            results.append(
                f"{tweetList[i].text}\nTweet Link : {tweetLink[i].get_attribute('href')}  ")

        loopCounter = 0
        lastHeight = self.browser.execute_script(
            "return document.documentElement.scrollHeight")

        while True:
            if loopCounter > 3:   # loopCounter : Number of times scrolled
                break
            self.browser.execute_script(
                "window.scrollTo(0,document.documentElement.scrollHeight);")
            time.sleep(2)
            newHeight = self.browser.execute_script(
                "return document.documentElement.scrollHeight")
            if lastHeight == newHeight:
                break
            lastHeight = newHeight
            loopCounter += 1
            tweetList = self.browser.find_elements_by_xpath(
                "//div[@data-testid='tweet']/div[2]/div[2]/div[1]/div")
            tweetLink = self.browser.find_elements_by_xpath(
                "//div[@data-testid='tweet']/div[2]/div[1]/div/div/div[1]/a")
            time.sleep(2)
            print(f"Number of Tweet : {len(tweetList)}")
            for i in range(len(tweetList)):
                results.append(
                    f"{tweetList[i].text}\nTweet Link : {tweetLink[i].get_attribute('href')}  ")

        count = 1
        # Save data in txt file
        with open("tweets.txt", "w", encoding="UTF-8") as file:
            for item in results:
                file.write("\n************************************\n")
                file.write(f"\n{count}- {item}\n")
                count += 1


twitter = Twitter(username, password)
twitter.signIn()
twitter.search("hkunv")
