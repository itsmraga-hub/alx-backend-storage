#!/usr/bin/env python3
"""
    Write a Python function that lists all documents in a collection:
"""


def list_all(mongo_collection):
    """
        Python function that lists all documents in a collection
    """
    docs = mongo_collection.find()
    if docs.count() > 0:
        return docs
    return []
