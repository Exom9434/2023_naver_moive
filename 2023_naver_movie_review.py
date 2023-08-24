from datacrawling import MovieRankingAnalyzer
from preprocessing import Preprocessor

crawler = MovieRankingAnalyzer(csv_filename= "movie_ranking.csv", driver_path = "chromedriver")

review_data = crawler.find_ratings()