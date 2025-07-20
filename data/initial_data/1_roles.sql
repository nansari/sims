-- DELETE FROM role;
-- DELETE FROM password WHERE id == 1;
-- DELETE FROM user WHERE id = 1;
INSERT INTO role (role, level,description ) VALUES 
('Admin', 10, 'Super user admin of this system'),
('BatchZimmedar', 20, 'Oversees operation and decision make of the batch'),
('Ustad', 30, 'The Teacher'),
('Gender', 40, 'People having access of recors of both genders'),
('Muallim', 50, 'Mentor assigned to a user for guidance'),
('HalqahNaqeeb', 60, 'Naqeeb who conduct Halqah'),
('InfoTechNaqeeb', 70, 'People provide IT support and maintain attendance records'),
('FieldNaqeeb', 80, 'Champions who are working in fields with societies'),
('ClassSupportNaqeeb', 90, 'Naqeeb who helps to run the classes'),
('RegistrationTeam', 100, 'Processes new registration and do first call'),
('Student', 110, 'Student'),
('NoRole', 9999, 'No Role at all');
