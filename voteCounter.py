import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import pytesseract

from datetime import datetime, timedelta
import os
import discord
import contextlib
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD-BOT-LD-TOKEN')

option = webdriver.ChromeOptions()
option.add_argument("user-agent=\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36\"")
option.add_argument("--incognito")
browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=option)

browser.get(f"https://live.house.gov")

time.sleep(3)

watch = browser.find_elements_by_xpath("//div[@id='watch']")[0]
watch.click()
browser.set_window_size(600, 600)
time.sleep(5)
video = browser.find_elements_by_xpath("//div[@id='media-player']")[0]
video.click()
time.sleep(4)

last_updated = datetime.now()
client = discord.Client()
@client.event
async def on_message(message):
    global last_updated
    if message.content.startswith("!liveHouseUpdate") and message.author != client.user:
        if datetime.now() - last_updated > timedelta(seconds=5):
            browser.find_element_by_tag_name("video").screenshot("screenshot.png")
            # print(pytesseract.image_to_string(Image.open('screenshot.png'), lang="eng"))
            last_updated = datetime.now()
        embed = discord.Embed()
        file = discord.File("screenshot.png", filename="screenshot.png")
        embed.set_image(url="attachment://screenshot.png")
        await message.channel.send(file=file, embed=embed)


@client.event
async def on_ready():
    print(f"Connected {client.user.name} - {client.user.id}\n------")
client.run(TOKEN)