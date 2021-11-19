import random
from time import sleep
from collections import defaultdict
import re
def crawl_followers(browser,acct):
    current_url ='https://www.instagram.com/'
    browser.get(f'{current_url}{acct}')
    followers = set()
    follower_count = browser.find_element_by_xpath("//div[@id='react-root']//header[@class='vtbgv ']//ul[@class='k9GMp ']/li[2]/a/span").get_attribute('innerHTML')


    elems = browser.find_element_by_xpath("//div[@id='react-root']//header[@class='vtbgv ']//ul[@class='k9GMp ']/li[2]/a")
    elems.click()
    sleep(8)
    browser.execute_script("document.getElementsByClassName('isgrP')[0].scrollTo(0,1000)")
    sleep(5)
    elems = browser.find_elements_by_xpath(
        "//body//div[@class='PZuss']//a[contains(@class,'FPmhX') and contains(@class,'_0imsa')]")
    count = 0

    while 1:
        #if len(elems) >= 5 :
        for elem in elems:
            val = elem.get_attribute('innerHTML')
            followers.add(val)
            elems.pop()
        try:
            for i in range(12):
                browser.execute_script("document.getElementsByClassName('PZuss')[0].children[0].remove()")
        except Exception as ex:
            print(ex)




        sleep(2)
        browser.execute_script( "document.getElementsByClassName('isgrP')[0].scrollTo(0,document.getElementsByClassName('isgrP')[0].scrollHeight)")
        #if elems:
         #   for elem in elems:
         #       val = elem.get_attribute('innerHTML')
         #       followers.add(val)

        sleep(3)
        elems = browser.find_elements_by_xpath(    "//body//div[@class='PZuss']//a[contains(@class,'FPmhX') and contains(@class,'_0imsa')]")
        if len(followers) >= 10:
            break
        if not elems:
            break

    return followers


def check_private(browser):

    try:
        is_private = browser.find_element_by_xpath("//div[@id='react-root']//article[@class='ySN3v']//div[@class='QlxVY']/h2").get_attribute(
                'innerText').lower()
        is_private = re.search('private',is_private)
        if is_private:
            print("profile is private")
            return True
    except Exception as ex:
        print("Profile is not private")
        return False

def normalize_follower_count(*counts):
    counts = list(counts)
    for index,count in enumerate(counts):
        if re.search('m',count):
            counts[index] = int(count.replace('m','0'* 6),10)
        elif re.search('k',count):
            if '.' in count:
                count = count.replace('.','')
                counts[index] = int(count.replace('k', '0' * 2), 10)
            else:
                counts[index] =  int(count.replace('k','0'* 3),10)
        else:
            counts[index] = int(count.replace(',',''),10)
    return(counts)

def has_picture(browser):
    try:
        has_pic = browser.find_element_by_xpath("//div[@id='react-root']//header[@class='vtbgv ']//img[@class='be6sR']").get_attribute('src')
        if re.search('.*44884218_345707102882519_2446069589734326272_n.jpg.*',has_pic):
            print("profile has not pic")
            return 1
        else:
            return 0

    except Exception as ex:
        print("profile has pic")
        return 0

def hasLinkInDesc(browser):
    try:
        has_link = browser.find_element_by_xpath(
                "//div[@id='react-root']//header[@class='vtbgv ']//div[@class='-vDIg']/a").get_attribute(
                'innerText')
        if re.search('bit\.ly',has_link):
            return 2
        else:
            return 0.5
    except Exception as ex:
        print("no susp link in description")
        return 0

def acct_heuristics(browser,*counts):
    score = 0
    score += has_picture(browser)
    score += hasLinkInDesc(browser)
    if counts[0] == 0:
        score += 1.5
    return score


def audit_followers(browser, follower_list):
    fake_followers = defaultdict()
    current_url = 'https://www.instagram.com/'
    for follower in follower_list:
        browser.get(f'{current_url}{follower}')
        following_count = ""
        follower_count = ""
        is_private = check_private(browser)
        try:
            post_count = browser.find_element_by_xpath(
                "//div[@id='react-root']//header[@class='vtbgv ']//ul[@class='k9GMp ']/li[1]/span").get_attribute(
                'innerText').split(' ')[0]
        except Exception as ex:
            print("test")
        if is_private:

            following_count =browser.find_element_by_xpath(
            "//div[@id='react-root']//header[@class='vtbgv ']//ul[@class='k9GMp ']/li[2]/span").get_attribute(
            'innerText').split(' ')[0]
            follower_count = browser.find_element_by_xpath(
            "//div[@id='react-root']//header[@class='vtbgv ']//ul[@class='k9GMp ']/li[3]/span").get_attribute(
            'innerText').split(' ')[0]
        else:
            following_count = browser.find_element_by_xpath(
                "//div[@id='react-root']//header[@class='vtbgv ']//ul[@class='k9GMp ']/li[3]/a/span").get_attribute(
                'innerText').split(' ')[0]
            follower_count = browser.find_element_by_xpath(
                "//div[@id='react-root']//header[@class='vtbgv ']//ul[@class='k9GMp ']/li[2]/a/span").get_attribute(
                'innerText').split(' ')[0]
        post_count, following_count, follower_count = normalize_follower_count(post_count,following_count,follower_count)
        score = acct_heuristics(browser,post_count, following_count, follower_count )

        if score >= 1:
            fake_followers.update({follower : {'score' : score } })

        sleep(random.randint(5,10))
    return fake_followers




