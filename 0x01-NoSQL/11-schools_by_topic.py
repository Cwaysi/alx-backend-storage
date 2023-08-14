#!/usr/bin/env python3
"""
Returns list of schools 
"""


def schools_by_topic(mongo_collection, topic):
    """
    Prototype: def schools_by_topic(mongo_collection, topic):
    """
    return mongo_collection.find({"topics": topic})
