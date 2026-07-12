new_person = """
    INSERT INTO Person (name, credit) 
    VALUES (%s, %s)
"""

all_people = """
    SELECT * FROM Person;
"""
