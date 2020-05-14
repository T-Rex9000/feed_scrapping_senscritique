from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
import re


def check_rate(string):
    rate = re.search("([1-9]|10)\/10", string)
    if rate:
        return rate.group(1)


def check_wish(string):
    if "a envie de voir le film" in string or "a envie de lire le livre" in string:
        return True


def retrieve_actor_in_content(content):
    actor = content.find("a", {"class": "elfs-story-actor"})
    return actor.text


def retrieve_date_in_footer(footer):
    time = footer.find("time").attrs["datetime"][:10]
    return pd.to_datetime(time)


def parse_elfe_story(innercontent):
    content = innercontent.find("span", {"class": "elfs-story-compile"})
    footer = innercontent.find("div", {"class": "elfs-story-footer"})

    rate = check_rate(content.text)
    wish = check_wish(content.text)
    actor = retrieve_actor_in_content(content)

    if rate:
        type = "rate"
    elif wish:
        type = "wish"
    else:
        type = "unknown"

    datetime = retrieve_date_in_footer(footer)

    row = {"type": type,
           "actor": actor,
           "detail": rate,
           "datetime": datetime}

    return row


def parse_args(args):
    url = args[1]

    try:
        month_limit = int(args[2])
    except:
        month_limit = 1

    try:
        year_limit = int(args[3])
    except:
        year_limit = 1996

    return url, month_limit, year_limit


if __name__ == "__main__":
    url, month_limit, year_limit = parse_args(sys.argv)

    # Retrieve piece
    piece = url.split("/")[-2]

    # Create PJS instance
    browser = webdriver.PhantomJS()

    # Visit feed page
    browser.get(f"{url}/actualites")

    # Initialize page and story counts
    last_n_stories = 0
    c = 1

    df = []
    end_of_feed = False

    # Keep going until number of stories is the same for two iterations
    while True:
        # Find "Afficher plus d'actualites" button
        element = browser.find_element_by_xpath('//button[@data-rel="feeds-more"]')

        # Wait for button to be displayed
        timer = 0
        while not element.is_displayed():
            time.sleep(0.5)
            timer += 0.5
            if timer > 30:
                end_of_feed = True
                break

        # Check if the end of the feed has been reached
        if end_of_feed:
            print("End (timer)")
            break

        # Click button
        element.click()

        # Retrieve stories
        soup = BeautifulSoup(browser.page_source)
        stories = soup.find_all("div", {"class": "elfs-story-innercontent"})

        # Parse new stories
        new_stories = stories[last_n_stories:]

        for story in new_stories:
            parsed_story = parse_elfe_story(story)
            df.append(parse_elfe_story(story))

        print(f"Page {c}: {len(stories)} activites recuperees\n"
              f"Derniere date: {df[-1]['datetime'].month}/{df[-1]['datetime'].year}")

        # Check if date limit has been reached
        if df[-1]["datetime"].year <= year_limit and df[-1]["datetime"].month <= month_limit:
            print("End (limit)")
            break

        # Check if end of feed has been reached
        if len(stories) == last_n_stories:
            print("End (stories)")
            break

        last_n_stories = len(stories)
        c += 1

    # Close PJS
    browser.close()

    # Save feed
    df = pd.DataFrame(df)
    df.to_csv(f"feed_{piece}.csv", index=False)
