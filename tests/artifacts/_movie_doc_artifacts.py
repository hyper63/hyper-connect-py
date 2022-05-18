from typing import Dict, List


def movie_bulk_doc_artifacts() -> List[Dict]:
    return [
        {
            "_id": "movie-104",
            "type": "movie",
            "title": "Full Metal Jacket",
            "year": "1987",
        },
        {
            "_id": "movie-105",
            "type": "movie",
            "title": "Predator",
            "year": "1987",
        },
    ]


def movie_doc_artifacts() -> List[Dict]:

    return [
        {
            "_id": "movie-100",
            "type": "movie",
            "title": "Chariots of Fire",
            "year": "1981",
        },
        {
            "_id": "movie-101",
            "type": "movie",
            "title": "Star Wars",
            "year": "1977",
        },
        {
            "_id": "movie-102",
            "type": "movie",
            "title": "Back to the Future",
            "year": "1985",
        },
    ]
