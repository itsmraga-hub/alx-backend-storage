#!/usr/bin/env python3
"""
    Write a Python function that returns the list of school having a
    specific topic:
"""


def schools_by_topic(mongo_collection, topic):
    """
        Python function that returns the list of school having a
        specific topic:
    """
    docs = mongo_collection.find({ "topics": topic })
    return list(docs)
