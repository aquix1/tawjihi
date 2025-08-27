from flask import Flask, render_template, request, redirect, url_for, flash, session
from mongoengine import connect
from models import Admin, Student
from config import Config
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MongoDB connection
connect(
    db=Config.MONGODB_SETTINGS.get("db"),
    host=Config.MONGODB_SETTINGS.get("host")
)

# Admin authentication required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('يجب تسجيل الدخول أولاً', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def get_results():
    seat_number = request.form.get('seat_number')
    birth_date = request.form.get('birth_date')
    
    student = Student.objects(seat_number=seat_number, birth_date=birth_date).first()
    
    if student:
        # Get top 10 students for leaderboard
        top_students = Student.objects.order_by('-total_score')[:10]
        
        # Get student rank
        all_students = Student.objects.order_by('-total_score')
        rank = 1
        for s in all_students:
            if s.seat_number == student.seat_number:
                break
            rank += 1
        
        return render_template(
            'results.html', 
            student=student, 
            top_students=top_students,
            rank=rank
        )
    else:
        flash('لم يتم العثور على نتائج، يرجى التحقق من رقم الجلوس وتاريخ الميلاد', 'danger')
        return redirect(url_for('index'))

@app.route('/login-admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if admin exists (create one if none exists)
        admin = Admin.objects(username=username).first()
        
        if not admin:
            # Create default admin if none exists
            if username == 'admin' and password == 'admin123':
                admin = Admin(username=username)
                admin.set_password(password)
                admin.save()
            else:
                flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'danger')
                return redirect(url_for('admin_login'))
        
        if admin.check_password(password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('تم تسجيل الدخول بنجاح', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'danger')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    students = Student.objects.order_by('-total_score')
    return render_template('admin_dashboard.html', students=students)

@app.route('/admin/add-student', methods=['POST'])
@admin_required
def add_student():
    try:
        math = float(request.form.get('math'))
        religion = float(request.form.get('religion'))
        history = float(request.form.get('history'))
        geography = float(request.form.get('geography'))
        english = float(request.form.get('english'))
        arabic = float(request.form.get('arabic'))
        social_studies = float(request.form.get('social_studies'))
        total_score = math + religion + history + geography + english + arabic + social_studies

        student = Student(
            seat_number=request.form.get('seat_number'),
            full_name=request.form.get('full_name'),
            birth_date=request.form.get('birth_date'),
            math=math,
            religion=religion,
            history=history,
            geography=geography,
            english=english,
            arabic=arabic,
            social_studies=social_studies,
            total_score=total_score
        )
        student.save()
        flash('تم إضافة الطالب بنجاح', 'success')
    except Exception as e:
        flash(f'حدث خطأ أثناء إضافة الطالب: {str(e)}', 'danger')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

