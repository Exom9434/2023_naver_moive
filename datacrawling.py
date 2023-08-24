from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
import pandas as pd
import time

class MovieRankingAnalyzer:
    def __init__(self, csv_filename):
        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=self.options)
        self.movie_ranking_df = pd.read_csv(csv_filename)
        
    def movie_search(self, movie_name):

        search_url = f'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=영화+{movie_name}+평점'
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(search_url)
        time.sleep(15)
        self.driver.execute_script("window.scrollTo(0, 800)")
        time.sleep(2)
        
    def close_driver(self):
        if self.driver:
            self.driver.quit()
    
    def find_ratings(self):
        data = []
        times = 0
        
        for movie_name in self.movie_ranking_df["영화명"]:
            self.movie_search(movie_name)
            
            x_path = "/html/body/div[3]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[6]"
            try:
                to_scroll = self.driver.find_element(By.XPATH, x_path)
            except Exception as e:
                print(f"An error occurred: {str(e)} for {movie_name}")
                self.close_driver()
                continue
            
            counts = 0
            movie_comments = []
            movie_ratings = []
            
            while True:
                all_contents = self.driver.find_elements(By.CSS_SELECTOR, "div.lego_review_list._scroller")
                
                flag = False
                
                for content in all_contents:
                    li_comments = content.find_elements(By.CSS_SELECTOR, "span.desc._text")
                    li_ratings = content.find_elements(By.CSS_SELECTOR, "div.area_text_box")
                    
                    for li_comment in li_comments[counts:]:
                        movie_comments.append(li_comment.text)
                    
                    for li_rating in li_ratings[counts:]:
                        rating_value = li_rating.get_attribute("textContent").replace("별점(10점 만점 중)", "").strip()
                        movie_ratings.append(int(rating_value))
                
                if len(movie_comments) == counts:
                    flag = True
                    break
                
                if flag:
                    print('종료')
                    break
                counts = len(movie_comments)
                times += 1
                if times % 100 == 0:
                    print(str(movie_name) + ' ' + str(times) + ' 회 실행했습니다')
                
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", to_scroll)
                time.sleep(3)
            
            if len(movie_comments) == 0:
                self.close_driver()
                continue
            self.close_driver()
            
            movie_data = {
                'movieName': [movie_name] * len(movie_comments),
                'comments': movie_comments,
                'ratings': movie_ratings
            }
            
            data.extend(pd.DataFrame(movie_data).to_dict('records'))
                
        movie_df = pd.DataFrame(data)
        return movie_df