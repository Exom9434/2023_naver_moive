from datacrawling import MovieRankingAnalyzer
from preprocessing import Preprocessor

# crawler = MovieRankingAnalyzer(csv_filename= "movie_ranking.csv", driver_path = "chromedriver")

# review_data = crawler.find_ratings()
# review_data.to_csv("movie_review.csv", index=False, sep='\t') 

preprocessor = Preprocessor("movie_review.csv")

df = preprocessor.clean_vacant()
df = preprocessor.clean_text()
df = preprocessor.labeling(5)

preprocessor.df.drop(["Unnamed: 0","ratings"], axis=1, inplace = True)

preprocessor.df.to_csv("modified_movie_review.csv", index = False, sep = '\t')

df = preprocessor.tokenizer(df)

