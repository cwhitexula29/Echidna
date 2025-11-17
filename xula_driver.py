from urllib import response
from imdbData2 import IMDB
import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import requests
from Movie import Movie
from Rank_show_duration import rank_tv_shows_by_duration
from Rank_movie_duration import RankMovieDuration
from PIL import Image



def find_movie_by_actor(movies_df, actor_name):
    # Convert actor name to lowercase for case-insensitive comparison
    actor_name_lower = actor_name.lower()
    # Filter movies where the actor is in the Stars list
    filtered_movies = movies_df[movies_df['Stars'].apply(
        lambda stars: isinstance(stars, list) and 
        any(actor_name_lower in star.lower() for star in stars)
    )]
    return filtered_movies

def rank_shows_by_rating(shows_df):
    # Sort by rating and get only top 5 shows
    ranked_shows = shows_df.sort_values(by='Rating', ascending=False).head(5).reset_index(drop=True)
    # Add 1 to index to start counting from 1
    ranked_shows.index = ranked_shows.index + 1
    return ranked_shows

def get_centennial_campaign_impact(url):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/118.0.5993.90 Safari/537.36"
            ),
            "Referer": "https://www.google.com/",
            "Accept-Language": "en-US,en;q=0.9",
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        campaign_header = soup.find(
            lambda tag: tag.get_text(strip=True).upper() == "CAMPAIGN IMPACT"
        )

        impact_paragraphs = []
        if campaign_header:
            for sibling in campaign_header.find_all_next():
                if sibling.name in ["h2", "h3"]:
                    break

                if sibling.name in ["p", "span", "div"]:
                    text = sibling.get_text(strip=True)
                    if text and len(text.split()) > 5:  
                        impact_paragraphs.append(text)
                        break  
        if not impact_paragraphs:
            impact_paragraphs = ["Campaign impact text not found."]

        title_tag = soup.find("h1")
        title_text = title_tag.get_text(strip=True) if title_tag else "No title found"

        return {
            "title": title_text,
            "impact_text": impact_paragraphs,
            "source_url": url,
        }   



def print_welcome_message():
    print(r"""
            ╔═══════════════════════════════════════════════════════╗
            ║              🎬  WELCOME VIEWERS! 🎥                  🍿
            ║            Welcome to Movie/TV Review                 ║
            ╚═══════════════════════════════════════════════════════╝
    """)

#Brand.png added by cwhitexula29
def show_brand_popup():
    import tkinter as tk
    from PIL import Image, ImageTk

    window = tk.Tk()
    window.title("Welcome")

    img = Image.open("assets/brand.png")
    img = img.resize((350, 350))
    img_tk = ImageTk.PhotoImage(img)

    label = tk.Label(window, image=img_tk)
    label.image = img_tk
    label.pack()

    btn = tk.Button(window, text="Continue", command=window.destroy)
    btn.pack(pady=10)

    window.mainloop()


def main():
    #calling brand popup function
    show_brand_popup()

    tv_raw = pd.read_csv("TV_Data.csv")
    print("\n--- Loaded TV Data ---")
    print(tv_raw.head())

    all_tv = []

    for html_content in tv_raw["html"]:
        imdb_page = IMDB(html_content)
        df_show = imdb_page.movieData()  
        all_tv.append(df_show)

    tv_df = pd.concat(all_tv, ignore_index=True)

    top_tv_by_duration = rank_tv_shows_by_duration(tv_df, top_n=10)

    print("\n--- Top 10 Longest TV Shows ---")
    print(top_tv_by_duration)

    movie_ranker = RankMovieDuration("Movie_Data.csv")
    top_movies_by_duration = movie_ranker.rank_by_duration(top_n=10)

    print("\n--- Top 10 Longest Movies ---")
    print(top_movies_by_duration)








    campaign_data = get_centennial_campaign_impact("https://www.xula.edu/about/centennial.html")
    
    print()
    print("---------------------------------------------------------------------------------")
    print("Get to know a little bit more about XULA before looking at our IMDB Data Display!")
    print("---------------------------------------------------------------------------------")

    print(f"{campaign_data['title']}: {campaign_data['impact_text']}\n")

    csv_path = "Movie_Data.csv"
        
    df = pd.read_csv(csv_path)

    csv_path2 = "TV_Data.csv"
        
    df2 = pd.read_csv(csv_path2)

    #ascii art added by @cwhitexula29
    print(r"""
 __     __    __     _____     ______        ______   ______     ______      __    __     ______     __   __   __     ______     ______    
/\ \   /\ "-./  \   /\  __-.  /\  == \      /\__  _\ /\  __ \   /\  == \    /\ "-./  \   /\  __ \   /\ \ / /  /\ \   /\  ___\   /\  ___\   
\ \ \  \ \ \-./\ \  \ \ \/\ \ \ \  __<      \/_/\ \/ \ \ \/\ \  \ \  _-/    \ \ \-./\ \  \ \ \/\ \  \ \ \'/   \ \ \  \ \  __\   \ \___  \  
 \ \_\  \ \_\ \ \_\  \ \____-  \ \_____\       \ \_\  \ \_____\  \ \_\       \ \_\ \ \_\  \ \_____\  \ \_/     \ \_\  \ \_____\  \/\_____\ 
  \/_/   \/_/  \/_/   \/____/   \/_____/        \/_/   \/_____/   \/_/        \/_/  \/_/   \/_____/   \/_       \/_/   \/_____/   \/_____/ 
                                                                                                                                           
          """)
    print("Welcome to the IMDB Top Movies Data Display!")
    print()
    user_input = input('What would you like see?(Type "Title", "Date", "Runtime", "Genre", "Rating", "Metascore", "Description", "Director", "Stars", "Votes", "Gross"): ')
    user_options = ["Title", "Date", "Runtime", "Genre", "Rating", "Metascore", "Description", "Director", "Stars", "Votes", "Gross"]
    print("You selected:", user_input)

    all_movies = []
    all_shows = []


    for html_content in df['html']:
        imdb_page = IMDB(html_content)
        movie_df = imdb_page.movieData()
        all_movies.append(movie_df)
    
    for html_content2 in df2['html']:
        imdb_page2 = IMDB(html_content2)
        show_df = imdb_page2.movieData()
        all_shows.append(show_df)
    
    full_df2 = pd.concat(all_shows, ignore_index=True)
    full_df = pd.concat(all_movies, ignore_index=True)
    if user_input.strip().lower() == 'genre':
        print("\n🎬 Movie Genres 🎬")
        # Collect all genres in a single list
        all_genres = []
        for genre in full_df['Genre']:
            if isinstance(genre, list):
                all_genres.extend(genre)
            else:
                all_genres.append(genre)
        # Print all genres in one line
        print(', '.join(all_genres))
    elif user_input not in user_options:
        print(f"Invalid input. Next time please choose from the following options:{user_options}")
    else:
        print("Here is our movie data for ", user_input + ":")
        print(full_df[user_input].to_string(index=False))

    print()
    specific_input = input("Would you like to see a specific movie's data? (yes/no): ").strip().lower()
    if specific_input == 'yes':
        movie_title = input('Enter the movie title: ').strip()
        specific_movie = full_df[full_df['Title'].str.lower() == movie_title.lower()]
        if not specific_movie.empty:
            print(specific_movie.to_string(index=False))
        else:
            print("Movie not found.")
    print()
    see_star = input("Would you like to find movies by a specific actor? (yes/no): ").strip().lower()
    if see_star == 'yes':
        actor_name = input('Enter the star\'s name: ').strip()
        movies_with_actor = find_movie_by_actor(full_df, actor_name)
        print(f"\n🎬 Movies featuring {actor_name} 🎬")
        if not movies_with_actor.empty:
            print(movies_with_actor[['Title', 'Date', 'Genre', 'Rating']].to_string(index=False))
        else:
            print(f"No movies found featuring {actor_name}.")

    print()
    print("\nNow displaying top 5 TV shows ranked by rating!:")
    print(rank_shows_by_rating(full_df2))

    #random movie feature added by @cwhitexula29
    from random_movie import RandomMovie

    random_movie = RandomMovie(full_df)
    suggestion = random_movie.get_random_movie()

    print("\n🎬 Random Movie Suggestion 🎬")
    print(f"{suggestion['Title']} ({suggestion['Date']}) - {suggestion['Genre']} | Rating: {suggestion['Rating']}")

    #director filter feature added by @cwhitexula29
    #commenting out for now to avoid import errors done by dnichol28
    # from director_file import DirecrtorFilter

    # director_filter = DirecrtorFilter(full_df)

    # director_input = input('\nEnter a director\'s name to filter movies: ').strip()
    # movies_by_director = director_filter.filter_by_director(director_input)

    # print("\n🎬 Movies by", director_input, "🎬")
    # if isinstance(movies_by_director, str):
    #     print(movies_by_director)
    # else:
    #     print(movies_by_director[['Title', 'Date', 'Genre', 'Rating']].to_string(index=False))

    #fake movie feature added by cwhitexula29
    from fake_movie import FakeMovie

    fake = FakeMovie()
    fake_movie = fake.generate_movie()

    print("\n 🎬 Fake Movie Generator 🎬")
    print(f"{fake_movie['Title']} ({fake_movie['Date']}) — {fake_movie['Genre']} | Rating: {fake_movie['Rating']}")
    
    #TV show recommender feature added by @cwhitexula29

    from tv_recommendation import TVShowRecommender

    tv_recommender = TVShowRecommender(full_df2)
    tv_suggestion = tv_recommender.recommend_show()

    print("\n📺 Recommended TV Show 📺")
    print(f"{tv_suggestion['Title']} ({tv_suggestion['Date']}) - {tv_suggestion['Genre']} | Rating: {tv_suggestion['Rating']}")


if __name__ == "__main__":
    main()
