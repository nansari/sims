
# Implement Following Tasks 
## Task-1: Create following class in .\app\models.py to implement tables with columns provided colums

### 1. ClassName
- name: upto 8 character uppercase alpha like KARMAH

### 2. ClassBatch
- class_name_id : foreign key to ClassName table
- batch_no : one alpha followed by 2 number like B07

### 3. ClassRegion - a subgroup of class batch
- class_name_id : foreign key to ClassName table
- class_batch_no_id : foreign key to ClassBatchNo table
- section: One upper case alpha like S, U, C, A
- description: One sentence description

### 4 ClassGroupMentor - A user can be mentor in multiple class group
- user_id : foreign key to User table
- class_name_id : foreign key to ClassName table
- class_batch_no_id : foreign key to ClassBatchNo table
- class_region_id : foreign key to ClassRegion table

### 5. ClassGroupIndex - A sub group in a class region with start and end index
- class_region_id : foreign key to ClassRegion table
- description: One sentence description
- start_index: number upto 4 digits (optional)
- end_index: number upto 4 digits (optional)

### 6. ClassGroupMentor - multiple user can be mentor in a class group
- class_group_id : foreign key to ClassGroup table
- user_id : foreign key to User table. it must be part of ClassGroupMentor table

### 7. UserStatus - a lookup table listing all the possible status of a user
- status: upto 16 caracter alpha like Active, Dropped Out, Terminated, Transfered, NextBatch, Retured
- description: One sentence description

### 6. StudentGroup - To assign a student to a group
- student_id : foreign key to Student table
- class_group_id : foreign key to ClassGroup table
- index_no: number upto 4 digits between start_index and end_index of ClassGroup (optional)
- status_id: foreign key to StudentStatus table

### 6. ClassBatchTeacher - multiple user can be teacher in a class batch
- teacher_id : foreign key to Teacher table
- class_group_id : foreign key to ClassGroup table

## Task-2: Role Based Access Control

### 1. Role - Create lookup table for all roles
- role: 16 character role code
- level: upto 3 digit unique number defining role proviledged 
- description: One sentence description

### 2. UserRole - Assign role to user
role_id: foreign key to Role table
user_id: foreign key to User table
class_batch_id: foreign key to ClassBatch table (optional)
class_region_id: foreign key to ClassRegion table (optional)
class_group_id: foreign key to ClassGroup table (optional)

## Task-3: Each of the above table will have following column
- created_by: user id who has created the record
- created_at: date and time when the record is created
- updated_by: user id who has updated the record
- updated_at: date and time when the record is updated

## Task-4: Create Forms and Routes to add/list/update/delete the above tables
### 1. 
### 2. 

## Tast-5: Update base.html to create hyperlink
### 1. <describe which link will go where>