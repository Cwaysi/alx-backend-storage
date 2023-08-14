#!/usr/bin/env python3
"""
Returns new _id
"""


def insert_school(mongo_collection, **kwargs):
    """
    Returns the new _id
    """
    new_document = mongo_collection.insert_one(kwargs)
    return new_document.inserted_id
