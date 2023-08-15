#!/usr/bin/env python3
"""
    Write a Python function that changes all topics of a school document
    based on the name:
"""


def update_topics(mongo_collection, name, topics):
    """
        Python function that changes all topics of a school document
        based on the name:
    """
    q = { "name": name }
    mongo_collection.update_many(
        q, {
            "$set": {
                "topics": topics
                }
            }
            )
