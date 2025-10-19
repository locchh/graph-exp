#!/usr/bin/env python3
"""
Movie Search CLI Application
Connects to Neo4j and searches for top-rated movies by genre.
"""

import os
import sys
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


def get_top_movies_by_genre(genre: str) -> list:
    """
    Query Neo4j for top 5 movies by IMDb rating for a given genre.
    
    Args:
        genre: Genre name to search for
        
    Returns:
        List of movie dictionaries with title, year, imdbRating, and genres
    """
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            query = """
                MATCH (m:Movie)
                WHERE m.genres IS NOT NULL 
                  AND m.imdbRating IS NOT NULL
                  AND m.genres CONTAINS $genre
                RETURN m.title, m.year, m.imdbRating, m.genres
                ORDER BY m.imdbRating DESC
                LIMIT 5
            """
            
            result = session.run(query, {"genre": genre})
            movies = []
            
            for record in result:
                movies.append({
                    "title": record["m.title"],
                    "year": record["m.year"],
                    "imdbRating": record["m.imdbRating"],
                    "genres": record["m.genres"]
                })
            
            return movies
    finally:
        driver.close()


def display_movies(genre: str, movies: list) -> None:
    """
    Display movies in a formatted table.
    
    Args:
        genre: The genre that was searched
        movies: List of movie dictionaries
    """
    if not movies:
        print(f"\nNo movies found for genre: {genre}")
        return
    
    print(f"\n{'='*80}")
    print(f"Top 5 Movies by IMDb Rating - Genre: {genre}")
    print(f"{'='*80}")
    print(f"{'Rank':<6} {'Title':<40} {'Year':<6} {'Rating':<8}")
    print(f"{'-'*80}")
    
    for idx, movie in enumerate(movies, 1):
        title = movie["title"][:37] + "..." if len(movie["title"]) > 40 else movie["title"]
        print(f"{idx:<6} {title:<40} {movie['year']:<6} {movie['imdbRating']:<8}")
    
    print(f"{'='*80}\n")


def main():
    """Main entry point for the application."""
    print("\n" + "="*80)
    print("Neo4j Movie Search - Find Top Rated Movies by Genre")
    print("="*80)
    
    try:
        genre = input("\nEnter a genre name (e.g., Comedy, Action, Drama): ").strip()
        
        if not genre:
            print("Error: Genre name cannot be empty")
            sys.exit(1)
        
        print(f"\nSearching for top movies in genre: {genre}...")
        movies = get_top_movies_by_genre(genre)
        display_movies(genre, movies)
        
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
