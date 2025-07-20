
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import ClassNameForm, ClassBatchForm, ClassRegionForm, ClassGroupIndexForm, ClassGroupMentorForm, UserStatusForm, StudentGroupForm, ClassBatchTeacherForm, RoleForm, UserRoleForm, ClassBatchStatusForm
from app.models import ClassName, ClassBatch, ClassRegion, ClassGroupIndex, ClassGroupMentor, UserStatus, StudentGroup, ClassBatchTeacher, Role, UserRole, ClassBatchStatus
from flask_login import current_user, login_required

@app.route('/class_name', methods=['GET', 'POST'])
@login_required
def class_name():
    form = ClassNameForm()
    if form.validate_on_submit():
        class_name = ClassName(name=form.name.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(class_name)
        db.session.commit()
        flash('Class name added successfully!')
        return redirect(url_for('class_name'))
    classes = ClassName.query.all()
    return render_template('class_name.html', title='Class Name', form=form, classes=classes)

@app.route('/class_batch', methods=['GET', 'POST'])
@login_required
def class_batch():
    form = ClassBatchForm()
    if form.validate_on_submit():
        class_batch = ClassBatch(class_name_id=form.class_name_id.data, batch_no=form.batch_no.data, start_date=form.start_date.data, status_id=form.status_id.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(class_batch)
        db.session.commit()
        flash('Class batch added successfully!')
        return redirect(url_for('class_batch'))
    batches = ClassBatch.query.all()
    return render_template('class_batch.html', title='Class Batch', form=form, batches=batches)

@app.route('/class_region', methods=['GET', 'POST'])
@login_required
def class_region():
    form = ClassRegionForm()
    if form.validate_on_submit():
        class_region = ClassRegion(class_name_id=form.class_name_id.data, class_batch_id=form.class_batch_id.data, section=form.section.data, description=form.description.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(class_region)
        db.session.commit()
        flash('Class region added successfully!')
        return redirect(url_for('class_region'))
    regions = ClassRegion.query.all()
    return render_template('class_region.html', title='Class Region', form=form, regions=regions)

@app.route('/class_group_index', methods=['GET', 'POST'])
@login_required
def class_group_index():
    form = ClassGroupIndexForm()
    if form.validate_on_submit():
        class_group_index = ClassGroupIndex(class_region_id=form.class_region_id.data, description=form.description.data, start_index=form.start_index.data, end_index=form.end_index.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(class_group_index)
        db.session.commit()
        flash('Class group index added successfully!')
        return redirect(url_for('class_group_index'))
    indexes = ClassGroupIndex.query.all()
    return render_template('class_group_index.html', title='Class Group Index', form=form, indexes=indexes)

@app.route('/class_group_mentor', methods=['GET', 'POST'])
@login_required
def class_group_mentor():
    form = ClassGroupMentorForm()
    if form.validate_on_submit():
        class_group_mentor = ClassGroupMentor(user_id=form.user_id.data, class_name_id=form.class_name_id.data, class_batch_id=form.class_batch_id.data, class_region_id=form.class_region_id.data, class_group_id=form.class_group_id.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(class_group_mentor)
        db.session.commit()
        flash('Class group mentor added successfully!')
        return redirect(url_for('class_group_mentor'))
    mentors = ClassGroupMentor.query.all()
    return render_template('class_group_mentor.html', title='Class Group Mentor', form=form, mentors=mentors)

@app.route('/user_status', methods=['GET', 'POST'])
@login_required
def user_status():
    form = UserStatusForm()
    if form.validate_on_submit():
        user_status = UserStatus(status=form.status.data, description=form.description.data)
        db.session.add(user_status)
        db.session.commit()
        flash('User status added successfully!')
        return redirect(url_for('user_status'))
    statuses = UserStatus.query.all()
    return render_template('user_status.html', title='User Status', form=form, statuses=statuses)

@app.route('/student_group', methods=['GET', 'POST'])
@login_required
def student_group():
    form = StudentGroupForm()
    if form.validate_on_submit():
        student_group = StudentGroup(student_id=form.student_id.data, class_group_id=form.class_group_id.data, index_no=form.index_no.data, status_id=form.status_id.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(student_group)
        db.session.commit()
        flash('Student group added successfully!')
        return redirect(url_for('student_group'))
    groups = StudentGroup.query.all()
    return render_template('student_group.html', title='Student Group', form=form, groups=groups)

@app.route('/class_batch_teacher', methods=['GET', 'POST'])
@login_required
def class_batch_teacher():
    form = ClassBatchTeacherForm()
    if form.validate_on_submit():
        class_batch_teacher = ClassBatchTeacher(user_id=form.user_id.data, class_batch_id=form.class_batch_id.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(class_batch_teacher)
        db.session.commit()
        flash('Class batch teacher added successfully!')
        return redirect(url_for('class_batch_teacher'))
    teachers = ClassBatchTeacher.query.all()
    return render_template('class_batch_teacher.html', title='Class Batch Teacher', form=form, teachers=teachers)

@app.route('/role', methods=['GET', 'POST'])
@login_required
def role():
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(role=form.role.data, level=form.level.data, description=form.description.data)
        db.session.add(role)
        db.session.commit()
        flash('Role added successfully!')
        return redirect(url_for('role'))
    roles = Role.query.all()
    return render_template('role.html', title='Role', form=form, roles=roles)

@app.route('/user_role', methods=['GET', 'POST'])
@login_required
def user_role():
    form = UserRoleForm()
    if form.validate_on_submit():
        user_role = UserRole(user_id=form.user_id.data, role_id=form.role_id.data, class_region_id=form.class_region_id.data, class_batch_id=form.class_batch_id.data, class_group_id=form.class_group_id.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(user_role)
        db.session.commit()
        flash('User role added successfully!')
        return redirect(url_for('user_role'))
    user_roles = UserRole.query.all()
    return render_template('user_role.html', title='User Role', form=form, user_roles=user_roles)

@app.route('/class_batch_status', methods=['GET', 'POST'])
@login_required
def class_batch_status():
    form = ClassBatchStatusForm()
    if form.validate_on_submit():
        class_batch_status = ClassBatchStatus(status=form.status.data)
        db.session.add(class_batch_status)
        db.session.commit()
        flash('Class batch status added successfully!')
        return redirect(url_for('class_batch_status'))
    statuses = ClassBatchStatus.query.all()
    return render_template('class_batch_status.html', title='Class Batch Status', form=form, statuses=statuses)
