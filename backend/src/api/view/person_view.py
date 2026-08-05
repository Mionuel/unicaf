# RETURNING returns the newly created person's data
new_person = """
    INSERT INTO "Person" (name, credit, bonus_points) 
    VALUES (%s, %s, %s)
    RETURNING id, name, credit, bonus_points;
"""

all_people = """
    SELECT * FROM "Person";
"""

get_person_by_id = """
    SELECT * FROM "Person" 
    WHERE id = %s;
"""
