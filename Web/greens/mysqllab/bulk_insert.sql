INSERT INTO characters 
(c_id, c_name, c_wit, c_strength, c_attack, c_defense, c_magic)
VALUES
(0, "Archibald", 0, 7, 2, 1, 0),
(1, "Henrik", 4, 3, 3, 1, 2),
(2, "Isadore", 2, 6, 4, 0, 4),
(3, "Lucinda", 4, 3, 1, 8, 1),
(4, "Dominic", 5, 2, 3, 3, 2);

INSERT INTO equipment
(e_id, e_name)
VALUES
(100, "Shield"),
(101, "Sword"),
(102, "Armor"),
(103, "Potion");

INSERT INTO quests 
(q_id, q_desc)
VALUES
(200, "Cross the bridge"),
(201, "Cross the lake"),
(202, "Cross the mountain"),
(203, "Cross the ocean");