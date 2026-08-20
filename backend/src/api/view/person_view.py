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

update_person = """
    UPDATE "Person" 
    SET credit = credit - %s, bonus_points = %s 
    WHERE id = %s;
"""

random_person = """
    SELECT id FROM "Person" ORDER BY RANDOM() LIMIT 1
"""

add_credits_to_person = """
    UPDATE "Person" 
    SET credit = credit + %s 
    WHERE id = %s
    RETURNING *;
"""

add_credits_to_all = """
    UPDATE "Person" 
    SET credit = credit + %s
    RETURNING *;
"""
