"""Tests for Lesson model"""
import pytest
import json
from datetime import datetime, timedelta
from backend.main import create_app
from backend.core.database import db
from backend.models.teacher import Teacher
from backend.models.learning_experience import LearningExperience
from backend.models.lesson import Lesson

@pytest.fixture
def app():
    """Create test app"""
    app = create_app('development')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_lesson_creation(app):
    """Test that Lesson can be created"""
    with app.app_context():
        # Create teacher
        teacher = Teacher(
            email='teacher@test.com',
            first_name='Test',
            last_name='Teacher',
            password_hash='hash123'
        )
        db.session.add(teacher)
        db.session.commit()
        teacher_id = teacher.id
        
        # Create learning experience
        le = LearningExperience(
            teacher_id=teacher_id,
            unit_number=22,
            experience_number=1,
            core_concept='Comparing Fractions',
            learning_intention='Use visual models to compare fractions',
            success_criteria=json.dumps(['I can compare fractions']),
            subject='Maths',
            year_level=6
        )
        db.session.add(le)
        db.session.commit()
        le_id = le.id
        
        # Create lesson
        lesson = Lesson(
            teacher_id=teacher_id,
            learning_experience_id=le_id,
            week_number=1,
            date_scheduled=datetime.now(),
            duration_minutes=60,
            location='Room 6',
            notes='First lesson on fractions',
            status='draft'
        )
        db.session.add(lesson)
        db.session.commit()
        
        assert lesson.id is not None
        assert lesson.teacher_id == teacher_id
        assert lesson.learning_experience_id == le_id
        assert lesson.week_number == 1
        assert lesson.status == 'draft'
        print("✅ Lesson creation: PASS")

def test_lesson_to_dict(app):
    """Test that Lesson converts to dict"""
    with app.app_context():
        teacher = Teacher(
            email='teacher2@test.com',
            first_name='Test',
            last_name='Teacher',
            password_hash='hash123'
        )
        db.session.add(teacher)
        db.session.commit()
        teacher_id = teacher.id
        
        le = LearningExperience(
            teacher_id=teacher_id,
            unit_number=22,
            experience_number=1,
            core_concept='Test',
            learning_intention='Test',
            success_criteria='[]',
            subject='Maths',
            year_level=6
        )
        db.session.add(le)
        db.session.commit()
        le_id = le.id
        
        lesson = Lesson(
            teacher_id=teacher_id,
            learning_experience_id=le_id,
            week_number=1,
            date_scheduled=datetime.now(),
            duration_minutes=60
        )
        db.session.add(lesson)
        db.session.commit()
        
        lesson_dict = lesson.to_dict()
        
        assert isinstance(lesson_dict, dict)
        assert lesson_dict['week_number'] == 1
        assert lesson_dict['duration_minutes'] == 60
        assert lesson_dict['status'] == 'draft'
        print("✅ Lesson to_dict: PASS")

def test_find_by_teacher_and_week(app):
    """Test finding lessons by teacher and week"""
    with app.app_context():
        teacher = Teacher(
            email='teacher3@test.com',
            first_name='Test',
            last_name='Teacher',
            password_hash='hash123'
        )
        db.session.add(teacher)
        db.session.commit()
        teacher_id = teacher.id
        
        le = LearningExperience(
            teacher_id=teacher_id,
            unit_number=22,
            experience_number=1,
            core_concept='Test',
            learning_intention='Test',
            success_criteria='[]',
            subject='Maths',
            year_level=6
        )
        db.session.add(le)
        db.session.commit()
        le_id = le.id
        
        # Create multiple lessons in different weeks
        for week in range(1, 4):
            lesson = Lesson(
                teacher_id=teacher_id,
                learning_experience_id=le_id,
                week_number=week,
                date_scheduled=datetime.now() + timedelta(weeks=week),
                status='published'
            )
            db.session.add(lesson)
        db.session.commit()
        
        # Find lessons in week 2
        week_2_lessons = Lesson.find_by_teacher_and_week(teacher_id, 2)
        assert len(week_2_lessons) == 1
        assert week_2_lessons[0].week_number == 2
        print("✅ Lesson find_by_teacher_and_week: PASS")

def test_find_by_teacher(app):
    """Test finding all lessons for a teacher"""
    with app.app_context():
        teacher = Teacher(
            email='teacher4@test.com',
            first_name='Test',
            last_name='Teacher',
            password_hash='hash123'
        )
        db.session.add(teacher)
        db.session.commit()
        teacher_id = teacher.id
        
        le = LearningExperience(
            teacher_id=teacher_id,
            unit_number=22,
            experience_number=1,
            core_concept='Test',
            learning_intention='Test',
            success_criteria='[]',
            subject='Maths',
            year_level=6
        )
        db.session.add(le)
        db.session.commit()
        le_id = le.id
        
        # Create 3 lessons
        for i in range(3):
            lesson = Lesson(
                teacher_id=teacher_id,
                learning_experience_id=le_id,
                week_number=i+1,
                date_scheduled=datetime.now() + timedelta(weeks=i+1)
            )
            db.session.add(lesson)
        db.session.commit()
        
        lessons = Lesson.find_by_teacher(teacher_id)
        assert len(lessons) == 3
        print("✅ Lesson find_by_teacher: PASS")

def test_find_by_le(app):
    """Test finding all lessons for a Learning Experience"""
    with app.app_context():
        teacher = Teacher(
            email='teacher5@test.com',
            first_name='Test',
            last_name='Teacher',
            password_hash='hash123'
        )
        db.session.add(teacher)
        db.session.commit()
        teacher_id = teacher.id
        
        le = LearningExperience(
            teacher_id=teacher_id,
            unit_number=22,
            experience_number=1,
            core_concept='Test',
            learning_intention='Test',
            success_criteria='[]',
            subject='Maths',
            year_level=6
        )
        db.session.add(le)
        db.session.commit()
        le_id = le.id
        
        # Create multiple lessons from same LE
        for i in range(3):
            lesson = Lesson(
                teacher_id=teacher_id,
                learning_experience_id=le_id,
                week_number=i+1,
                date_scheduled=datetime.now() + timedelta(weeks=i+1)
            )
            db.session.add(lesson)
        db.session.commit()
        
        lessons = Lesson.find_by_le(le_id)
        assert len(lessons) == 3
        assert all(l.learning_experience_id == le_id for l in lessons)
        print("✅ Lesson find_by_le: PASS")

def test_lesson_publish(app):
    """Test publishing a lesson"""
    with app.app_context():
        teacher = Teacher(
            email='teacher6@test.com',
            first_name='Test',
            last_name='Teacher',
            password_hash='hash123'
        )
        db.session.add(teacher)
        db.session.commit()
        teacher_id = teacher.id
        
        le = LearningExperience(
            teacher_id=teacher_id,
            unit_number=22,
            experience_number=1,
            core_concept='Test',
            learning_intention='Test',
            success_criteria='[]',
            subject='Maths',
            year_level=6
        )
        db.session.add(le)
        db.session.commit()
        le_id = le.id
        
        lesson = Lesson(
            teacher_id=teacher_id,
            learning_experience_id=le_id,
            week_number=1,
            date_scheduled=datetime.now(),
            status='draft'
        )
        db.session.add(lesson)
        db.session.commit()
        
        # Publish lesson
        lesson.publish()
        assert lesson.status == 'published'
        print("✅ Lesson publish: PASS")

def test_lesson_mark_taught(app):
    """Test marking lesson as taught"""
    with app.app_context():
        teacher = Teacher(
            email='teacher7@test.com',
            first_name='Test',
            last_name='Teacher',
            password_hash='hash123'
        )
        db.session.add(teacher)
        db.session.commit()
        teacher_id = teacher.id
        
        le = LearningExperience(
            teacher_id=teacher_id,
            unit_number=22,
            experience_number=1,
            core_concept='Test',
            learning_intention='Test',
            success_criteria='[]',
            subject='Maths',
            year_level=6
        )
        db.session.add(le)
        db.session.commit()
        le_id = le.id
        
        lesson = Lesson(
            teacher_id=teacher_id,
            learning_experience_id=le_id,
            week_number=1,
            date_scheduled=datetime.now(),
            status='published'
        )
        db.session.add(lesson)
        db.session.commit()
        
        # Mark as taught
        lesson.mark_taught()
        assert lesson.status == 'taught'
        print("✅ Lesson mark_taught: PASS")

def test_lesson_archive(app):
    """Test archiving a lesson"""
    with app.app_context():
        teacher = Teacher(
            email='teacher8@test.com',
            first_name='Test',
            last_name='Teacher',
            password_hash='hash123'
        )
        db.session.add(teacher)
        db.session.commit()
        teacher_id = teacher.id
        
        le = LearningExperience(
            teacher_id=teacher_id,
            unit_number=22,
            experience_number=1,
            core_concept='Test',
            learning_intention='Test',
            success_criteria='[]',
            subject='Maths',
            year_level=6
        )
        db.session.add(le)
        db.session.commit()
        le_id = le.id
        
        lesson = Lesson(
            teacher_id=teacher_id,
            learning_experience_id=le_id,
            week_number=1,
            date_scheduled=datetime.now(),
            status='published'
        )
        db.session.add(lesson)
        db.session.commit()
        
        # Archive lesson
        lesson.archive()
        assert lesson.status == 'archived'
        print("✅ Lesson archive: PASS")
