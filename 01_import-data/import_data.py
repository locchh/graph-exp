import os
import csv
from pathlib import Path
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

DATA_DIR = Path(__file__).parent / "data"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

def run_read_query(query, parameters=None):
    """Execute a read query and return results"""
    with driver.session(database=NEO4J_DATABASE) as session:
        result = session.execute_read(lambda tx: tx.run(query, parameters or {}).data())
        return result

def run_write_query(query, parameters=None):
    """Execute a write query"""
    def write_tx(tx):
        tx.run(query, parameters or {})
    
    with driver.session(database=NEO4J_DATABASE) as session:
        session.execute_write(write_tx)

def run_query(query, parameters=None):
    """Execute a query and return results (for backward compatibility)"""
    with driver.session(database=NEO4J_DATABASE) as session:
        result = session.run(query, parameters or {})
        data = result.data()
        return data

def clear_database():
    """Clear all nodes and relationships"""
    print("Clearing database...")
    run_query("MATCH (n) DETACH DELETE n")
    print("✓ Database cleared")

def create_constraints():
    """Create unique constraints and indexes"""
    print("\nCreating constraints and indexes...")
    
    # Movie unique constraint
    run_query("""
        CREATE CONSTRAINT movieId_Movie_uniq IF NOT EXISTS
        FOR (m:Movie) REQUIRE m.movieId IS UNIQUE
    """)
    print("✓ Movie unique constraint created")
    
    # Person unique constraint
    run_query("""
        CREATE CONSTRAINT person_tmdbId_Person_uniq IF NOT EXISTS
        FOR (p:Person) REQUIRE p.person_tmdbId IS UNIQUE
    """)
    print("✓ Person unique constraint created")

def import_persons():
    """Import Person nodes from persons.csv"""
    print("\nImporting Person nodes...")
    
    csv_file = DATA_DIR / "persons.csv"
    count = 0
    
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = """
                CREATE (p:Person {
                    person_tmdbId: toInteger($person_tmdbId),
                    name: $name,
                    born: $born,
                    bornIn: $bornIn,
                    died: $died,
                    bio: $bio,
                    person_imdbId: $person_imdbId,
                    person_poster: $person_poster,
                    person_url: $person_url
                })
            """
            
            params = {
                'person_tmdbId': row.get('person_tmdbId', ''),
                'name': row.get('name', ''),
                'born': row.get('born') if row.get('born') else None,
                'bornIn': row.get('bornIn', ''),
                'died': row.get('died') if row.get('died') else None,
                'bio': row.get('bio', ''),
                'person_imdbId': row.get('person_imdbId', ''),
                'person_poster': row.get('person_poster', ''),
                'person_url': row.get('person_url', '')
            }
            
            try:
                run_query(query, params)
                count += 1
                if count % 1000 == 0:
                    print(f"  Imported {count} persons...")
            except Exception as e:
                print(f"  Error importing person {row.get('name')}: {e}")
    
    print(f"✓ Imported {count} Person nodes")

def import_movies():
    """Import Movie nodes from movies.csv"""
    print("\nImporting Movie nodes...")
    
    csv_file = DATA_DIR / "movies.csv"
    count = 0
    
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = """
                CREATE (m:Movie {
                    movieId: toInteger($movieId),
                    title: $title,
                    budget: toFloat($budget),
                    countries: $countries,
                    movie_imdbId: $movie_imdbId,
                    imdbRating: toFloat($imdbRating),
                    imdbVotes: toInteger($imdbVotes),
                    languages: $languages,
                    plot: $plot,
                    movie_poster: $movie_poster,
                    released: $released,
                    revenue: toFloat($revenue),
                    runtime: toInteger($runtime),
                    movie_tmdbId: toInteger($movie_tmdbId),
                    movie_url: $movie_url,
                    year: toInteger($year),
                    genres: $genres
                })
            """
            
            params = {
                'movieId': row.get('movieId', ''),
                'title': row.get('title', ''),
                'budget': row.get('budget') if row.get('budget') else 0,
                'countries': row.get('countries', ''),
                'movie_imdbId': row.get('movie_imdbId', ''),
                'imdbRating': row.get('imdbRating') if row.get('imdbRating') else 0,
                'imdbVotes': row.get('imdbVotes') if row.get('imdbVotes') else 0,
                'languages': row.get('languages', ''),
                'plot': row.get('plot', ''),
                'movie_poster': row.get('movie_poster', ''),
                'released': row.get('released') if row.get('released') else None,
                'revenue': row.get('revenue') if row.get('revenue') else 0,
                'runtime': row.get('runtime') if row.get('runtime') else 0,
                'movie_tmdbId': row.get('movie_tmdbId', ''),
                'movie_url': row.get('movie_url', ''),
                'year': row.get('year') if row.get('year') else 0,
                'genres': row.get('genres', '')
            }
            
            try:
                run_query(query, params)
                count += 1
                if count % 100 == 0:
                    print(f"  Imported {count} movies...")
            except Exception as e:
                print(f"  Error importing movie {row.get('title')}: {e}")
    
    print(f"✓ Imported {count} Movie nodes")

def import_acted_in_relationships():
    """Import ACTED_IN relationships from acted_in.csv"""
    print("\nImporting ACTED_IN relationships...")
    
    csv_file = DATA_DIR / "acted_in.csv"
    count = 0
    failed = 0
    
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                movie_id = int(row.get('movieId', 0))
                person_id = int(row.get('person_tmdbId', 0))
                role = row.get('role', '')
                
                query = """
                    MATCH (m:Movie {movieId: $movieId})
                    MATCH (p:Person {person_tmdbId: $person_tmdbId})
                    CREATE (p)-[:ACTED_IN {role: $role}]->(m)
                """
                
                params = {
                    'movieId': movie_id,
                    'person_tmdbId': person_id,
                    'role': role
                }
                
                run_write_query(query, params)
                count += 1
                if count % 1000 == 0:
                    print(f"  Created {count} ACTED_IN relationships...")
            except Exception as e:
                failed += 1
    
    print(f"✓ Created {count} ACTED_IN relationships (failed: {failed})")

def import_directed_relationships():
    """Import DIRECTED relationships from directed.csv"""
    print("\nImporting DIRECTED relationships...")
    
    csv_file = DATA_DIR / "directed.csv"
    count = 0
    failed = 0
    
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                movie_id = int(row.get('movieId', 0))
                person_id = int(row.get('person_tmdbId', 0))
                
                query = """
                    MATCH (m:Movie {movieId: $movieId})
                    MATCH (p:Person {person_tmdbId: $person_tmdbId})
                    CREATE (p)-[:DIRECTED]->(m)
                """
                
                params = {
                    'movieId': movie_id,
                    'person_tmdbId': person_id
                }
                
                run_write_query(query, params)
                count += 1
                if count % 100 == 0:
                    print(f"  Created {count} DIRECTED relationships...")
            except Exception as e:
                failed += 1
    
    print(f"✓ Created {count} DIRECTED relationships (failed: {failed})")

def import_ratings():
    """Import ratings from ratings.csv"""
    print("\nImporting ratings...")
    
    csv_file = DATA_DIR / "ratings.csv"
    count = 0
    
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = """
                MATCH (m:Movie {movieId: toInteger($movieId)})
                SET m.avgRating = toFloat($rating),
                    m.ratingCount = toInteger($ratingCount)
            """
            
            params = {
                'movieId': row.get('movieId', ''),
                'rating': row.get('rating') if row.get('rating') else 0,
                'ratingCount': row.get('ratingCount') if row.get('ratingCount') else 0
            }
            
            try:
                run_query(query, params)
                count += 1
                if count % 1000 == 0:
                    print(f"  Updated {count} movies with ratings...")
            except Exception as e:
                print(f"  Error updating ratings for movie {row.get('movieId')}: {e}")
    
    print(f"✓ Updated {count} movies with ratings")

def verify_import():
    """Verify the import by checking node and relationship counts"""
    print("\nVerifying import...")
    
    movie_count = run_read_query("MATCH (m:Movie) RETURN count(m) as count")[0]['count']
    person_count = run_read_query("MATCH (p:Person) RETURN count(p) as count")[0]['count']
    acted_in_count = run_read_query("MATCH (p:Person)-[r:ACTED_IN]->(m:Movie) RETURN count(r) as count")[0]['count']
    directed_count = run_read_query("MATCH (p:Person)-[r:DIRECTED]->(m:Movie) RETURN count(r) as count")[0]['count']
    
    print(f"✓ Movies: {movie_count}")
    print(f"✓ Persons: {person_count}")
    print(f"✓ ACTED_IN relationships: {acted_in_count}")
    print(f"✓ DIRECTED relationships: {directed_count}")

def main():
    """Main import function"""
    try:
        print("=" * 60)
        print("Neo4j Data Import Script")
        print("=" * 60)
        
        clear_database()
        create_constraints()
        import_persons()
        import_movies()
        import_acted_in_relationships()
        import_directed_relationships()
        import_ratings()
        verify_import()
        
        print("\n" + "=" * 60)
        print("✓ Import completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Import failed: {e}")
        raise
    finally:
        driver.close()

if __name__ == "__main__":
    main()
