# search.py

import time
import re
import logging
from browser.browser import Browser
from selenium.webdriver.common.by import By  

logger = logging.getLogger(__name__)


class Search:
    def __init__(self, browser_choice):
        self.browser = Browser(browser_choice)

    async def search_internet(self, query, chat_id, context):
        self.browser.setup_driver()

        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            self.browser.driver.get(search_url)
            time.sleep(2)

            first_link = self.browser.driver.find_element(By.CSS_SELECTOR, 'h3').find_element(By.XPATH, '..')
            first_link.click()
            time.sleep(2)

            paragraphs = self.browser.driver.find_elements(By.TAG_NAME, 'p')
            complete_sentences = []

            for paragraph in paragraphs:
                text = paragraph.text
                sentences = re.split(r'(?<=[.!?]) +', text)

                for sentence in sentences:
                    if sentence.strip():
                        complete_sentences.append(sentence.strip())

            response_text = self.format_response(complete_sentences)
            await context.bot.send_message(chat_id=chat_id, text=response_text.strip(), parse_mode='Markdown')

        except Exception as e:
            logger.error(f"Ошибка при выполнении поиска: {e}")
            await context.bot.send_message(chat_id=chat_id, text="Произошла ошибка при выполнении поиска.")

        finally:
            self.browser.quit_driver()

    def format_response(self, complete_sentences):
        response_text = ""
        for sentence in complete_sentences:
            if len(response_text) + len(sentence) + 1 <= 2000:
                response_text += (sentence + " ")
            else:
                break

        if response_text and response_text[-1] not in '.!?':
            response_text = re.sub(r'\s*[^.!?]*$', '', response_text.strip()) 

        return response_text
