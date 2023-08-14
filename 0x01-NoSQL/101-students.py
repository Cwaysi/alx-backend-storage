#!/usr/bin/env python3
"""
Return all students sorted 
"""


def top_students(mongo_collection):
    """
    Prototype: def top_students(mongo_collection):
    """
    return mongo_collection.aggregate([
        {
            "$project":
            {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort":
            {
                "averageScore": -1
            }
        }
    ])
