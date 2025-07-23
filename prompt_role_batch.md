
# Implement Following Tasks 
## Task-1: Create following class in .\app\models.py to implement tables with columns provided. Optimize the colums for scalability and query performance.

### 1. ClassName
- name: upto 8 character uppercase alpha like KARMAH

### 2. ClassBatch
- class_name_id : foreign key to ClassName table
- batch_no : one alpha followed by 2 number like B07
- start_date: when the batch is startred
- status: foreing key to ClassBatchStatus table

### 3: ClassBatchStaus - a lookup table
- status: Registration, InProgress, Terminated, Completed, Terminated

### 4. ClassRegion - a subgroup of class batch
- class_name_id : foreign key to ClassName table
- class_batch_id : foreign key to ClassBatchNo table
- section: One upper case alpha like S, U, C, A
- description: One sentence description


### 5. ClassGroupIndex - A sub group in a class region with start and end index. 
- class_region_id : foreign key to ClassRegion table
- description: One sentence description
- start_index: number upto 4 digits (optional)
- end_index: number upto 4 digits (optional)

### 6 ClassGroupMentor - A user can be mentor in multiple class group and multiple user can be mentor in a class group
- user_id : foreign key to User table
- class_name_id : foreign key to ClassName table
- class_batch_id : foreign key to ClassBatchNo table 
- class_region_id : foreign key to ClassRegion table (optional)
- class_group_id : foreign key to ClassGroup table (optional)


### 7. UserStatus - a lookup table listing all the possible status of a user
- status: upto 16 caracter alpha like Active, Guest, DroppedOut, Terminated, Transfered, NextBatch, PassedAway
- description: One sentence description

### 8. StudentGroup - To assign a student to a group. Combination of class_group_id and student_id is unique
- student_id : foreign key to Student table
- class_group_id : foreign key to ClassGroup table
- index_no: number upto 4 digits between start_index and end_index of ClassGroup (optional)
- status_id: foreign key to StudentStatus table

### 9. ClassBatchTeacher - multiple user can be teacher in a class batch
- user_id : foreign key to Teacher table
- class_batch_id : foreign key to ClassBatch table



## Task-2: Role Based Access Control

### 1. Role - Create lookup table for all roles
- role: 16 character role code
- level: upto 3 digit unique number defining role proviledged 
- description: One sentence description

### 2. UserRole - Assign role to user
role_id: foreign key to Role table (optimize for search)
user_id: foreign key to User table (optimize for search)
class_region_id: foreign key to ClassRegion table (optional)
class_batch_id: foreign key to ClassBatch table (optional)
class_group_id: foreign key to ClassGroup table (optional)

## Task-3: Each of the above table should have following column - possibly using class inheritance for cleaner code
- created_by: user id who has created the record
- created_at: date and time when the record is created
- updated_by: user id who has updated the record
- updated_at: date and time when the record is updated


## Task-4: Create new forms in .\app\forms.py, new routes in .\app\routes.py and new templates html files in .\app\templates\ directory  to Add, Remove, Update, List, Search . In List and search submenu, add facility to select date range. Good to also have selection like 'In last one month', 'In Last 3 months', 'In last one week' etc
	1. ClassName
	2. ClassBatch
	3. ClassRegion
	4. ClassGroupIndex
	5. ClassGroupMentor
	6. UserStatus
	7. StudentGroup
	8. ClassBatchTeacher
	9. Role
	10. UserRole
	11. ClassBatchStaus
	
## Task-5: Update subitemsMenu of Navigation menu in .\app\templates\base.html to Add, Remove, Update, List, Search ten items listed above.

## Task-6: Understand the requirement and implement any other features that should make this application modern, cool, efficient, and attractive.