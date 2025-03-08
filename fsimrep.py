#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "altair",
#     "duckdb",
#     "pandas",
#     "tqdm",
#      "tabulate"
# ]
# ///
import json
import os
from typing import List, Optional
import sys
import argparse
from datetime import datetime
from dataclasses import dataclass
import duckdb
import pandas as pd
import altair as alt
import logging
import tabulate
from tqdm import tqdm
import time
import pathlib


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

@dataclass
class RepoSimilarity:
    """Type-safe model for repository similarity data."""
    full_name: str
    similarity_score: float
    common_users: int
    total_stars: int
    desc: str
    topics: List[str]

class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass

class StarEventsQuery:
    """Query builder for star events analysis with progress tracking and error handling."""
    
    def __init__(self, db_path: str):
        """Initialize database connection and create necessary views.
        
        Args:
            db_path: Path to the DuckDB database file
            
        Raises:
            DatabaseError: If database connection or view creation fails
        """
        try:
            # Initialize DuckDB connection
            self.conn = duckdb.connect(":memory:")
            localpath = pathlib.Path(__file__).resolve().parent.absolute()
            self.conn.execute(f"set file_search_path = '{localpath}';")
            logger.info("Successfully connected to DuckDB")
            
        except Exception as e:
            raise DatabaseError(f"Failed to initialize database: {str(e)}")
    def calculate_similarity(
        self,
        repo_name: str,
        min_stars: int = 5,
        min_common_users: int = 10,
        limit: int = 10
    ) -> List[RepoSimilarity]:
        logger.info(f"Calculating similarities for {repo_name}")
        start_time = time.time()
        try:
            # Optimized query with better table joins and filtering
            query: str = f"""--sql
            WITH  repo_pairs AS (
                    SELECT a.login, a.date,
                    a.repo as repo_a, b.repo as repo_b, 
                    r1.c as repo_a_stars, r2.c as repo_b_stars
                FROM 'starbase/*.parquet' a
                JOIN 'starlite.parquet' r1
                    ON a.repo = r1.repo
                JOIN 'starbase/*.parquet' b
                    ON a.login = b.login
                    AND a.repo != b.repo
                JOIN 'starlite.parquet' r2
                    ON b.repo = r2.repo
                WHERE a.repo ='{repo_name}'
            ),
            
            similarity_metrics AS (
                SELECT
                    repo_a,
                    repo_b,
                    COUNT(DISTINCT login) as common_users,
                    repo_b_stars as total_stars,
                    MIN(date) as earliest_common_star,
                    MAX(date) as latest_common_star,
                    CAST(COUNT(DISTINCT login) AS FLOAT) / NULLIF(repo_b_stars, 0) as jaccard_similarity
                FROM repo_pairs
                GROUP BY repo_a, repo_b, repo_b_stars
                HAVING COUNT(DISTINCT login) >= {min_common_users}
            ),
            results AS (
            SELECT
                repo_b as full_name,
                jaccard_similarity as similarity_score,
                common_users,
                total_stars,
                earliest_common_star,
                latest_common_star
            FROM similarity_metrics
            WHERE jaccard_similarity > 0
            ORDER BY jaccard_similarity DESC
            LIMIT {limit}
            )
                    
            SELECT 
            results.full_name,
            round(results.similarity_score, 3) as similarity_score,
            results.common_users,
            results.total_stars,
            ifnull(x.topics, []) as topics,
            ifnull(x.description, '') as desc,
            FROM results
            LEFT JOIN  'repos.parquet' as x on x.full_name = results.full_name
            ORDER BY similarity_score DESC
            LIMIT {limit}


            """.replace("#", "--")
            
            logger.info("Executing similarity query...")
            result = self.conn.execute(query).fetchdf()
            url="https://github.com/"
            # Convert results to typed objects with progress tracking
            logger.info("Processing query results...")
            similarities = []
              # link_code = f"\033]8;;{url}\a{display_text}\033]8;;\a"
            for _, row in tqdm(result.iterrows(), total=len(result), desc="Processing results"):
                similarities.append(
                    RepoSimilarity(
                        full_name=(
                            'github.com/'+ row['full_name']
                        ),
                        similarity_score=float(row['similarity_score']),
                        common_users=int(row['common_users']),
                        total_stars=int(row['total_stars']),
                        desc=row['desc'],
                        topics=row['topics']
                    )
                )
            
            execution_time = time.time() - start_time
            logger.info(f"Similarity calculation completed in {execution_time:.2f} seconds")
            return similarities
            
        except Exception as e:
            print(e)



def print_summary_stats(similarities: List[RepoSimilarity]) -> None:
    """Print summary statistics of similarity analysis with error handling."""
    # logger.info("\simiralities: \n", similarities)
    try:
        df = pd.DataFrame([vars(s) for s in similarities])
        
        logger.info("\nSummary Statistics:")
        logger.info("-" * 50)
        logger.info(f"Total similar repositories found: {len(df)}")
        
        if len(df) == 0:
            logger.info("No similar repositories found.")
            return
        logger.info(f"Average similarity score: {df['similarity_score'].mean():.3f}")
        logger.info(f"Median similarity score: {df['similarity_score'].median():.3f}")
        logger.info(f"Max similarity score: {df['similarity_score'].max():.3f}")
        
        logger.info("\nTop 5 Most Similar Repositories (with details):")
        summary_df = df[['full_name', 'similarity_score', 'common_users', 'total_stars', 'topics', 'desc']].tail(100)
        logger.info("\n" + summary_df.round(3).to_string(index=False))
        
    except Exception as e:
        logger.error(f"Failed to print summary statistics: {str(e)}")


if __name__ == "__main__":
    try:
        query = StarEventsQuery('stars2.ddb')

        # Set up argument parser
        parser = argparse.ArgumentParser(
            description='Calculate repository similarities based on common stargazers'
        )
        parser.add_argument('repo', help='Repository name (e.g., facebook/react)')
        parser.add_argument('--min-stars', type=int, default=10,
                          help='Minimum number of stars for comparison (default: 10)')
        parser.add_argument('--limit', type=int, default=50,
                          help='Maximum number of similar repositories to return (default: 100)')
        parser.add_argument('--min-common-users', type=int, default=5,
                          help='Minimum number of common users required (default: 10)')

        args = parser.parse_args()

        similarities = query.calculate_similarity(
            repo_name=args.repo,
            min_stars=args.min_stars,
            limit=args.limit,
            min_common_users=args.min_common_users
        )
        print(tabulate.tabulate(
            tabular_data=[
                [s.full_name, s.similarity_score, s.common_users, s.total_stars, s.desc
                 ] for s in similarities
            ],

            # maxcolwidths=100,                    
                                 headers=("repo", "Sim Score", "X Users", "Total Stars", "Topics", "Description"),
                                 maxcolwidths=[None, 10, 10, 40, 50],
                                tablefmt='fancy_grid',
                                
                                ))    
        
        # print_summary_stats(similarities)
    except DatabaseError as e:
        logger.error(f"Database error occurred: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
