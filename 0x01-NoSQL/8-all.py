#!/usr/bin/env python3
"""
List all documents 
"""

def list_all(mongo_collection):
    """
    Prototype: def list_all(mongo_collection)
    """
    documents = mongo_collection.find()
    return documents
