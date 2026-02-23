"""Tests for Worksheet and WorksheetQuestion models and service"""
import pytest
import json
from datetime import datetime
from backend.main import create_app
from backend.core.database import db
from backend.models.teacher import Teacher
from backend.models.learning_experience import LearningExperience
from backend.models.lesson import Lesson
from backend.models.worksheet import Worksheet
from backend.models.worksheet_question import WorksheetQuestion
from backend.services.worksheet_service import WorksheetService

@pytest.fixture
def app():
    """Create test app"""
    app = create_app('development')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_worksheet_creation(app):
    """Test that Worksheet can be created"""
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
            core_concept='Fractions',
            learning_intention='Understand fractions',
            success_criteria=json.dumps(['I can identify fractions']),
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
            duration_minutes=60
        )
        db.session.add(lesson)
        db.session.commit()
        lesson_id = lesson.id
        
        # Create worksheet
        worksheet = Worksheet(
            lesson_id=lesson_id,
            tier='mild',
            title='Fractions - Mild',
            subject='Maths',
            year_level=6,
            question_count=5
        )
        db.session.add(worksheet)
        db.session.commit()
        
        assert worksheet.id is not None
        assert worksheet.tier == 'mild'
        assert worksheet.question_count == 5
        print("✅ Worksheet creation: PASS")

def test_worksheet_question_creation(app):
    """Test that WorksheetQuestion can be created"""
    with app.app_context():
        # Setup
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
            core_concept='Fractions',
            learning_intention='Understand fractions',
            success_criteria=json.dumps(['I can identify fractions']),
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
            date_scheduled=datetime.now()
        )
        db.session.add(lesson)
        db.session.commit()
        lesson_id = lesson.id
        
        worksheet = Worksheet(
            lesson_id=lesson_id,
            tier='mild',
            title='Fractions - Mild',
            subject='Maths',
            year_level=6,
            question_count=5
        )
        db.session.add(worksheet)
        db.session.commit()
        worksheet_id = worksheet.id
        
        # Create question
        question = WorksheetQuestion(
            worksheet_id=worksheet_id,
            question_number=1,
            question_text='What is 1/2?',
            tier='mild',
            hints=json.dumps(['Hint: Think about parts']),
            model_answer='One half'
        )
        db.session.add(question)
        db.session.commit()
        
        assert question.id is not None
        assert question.question_number == 1
        assert question.tier == 'mild'
        print("✅ WorksheetQuestion creation: PASS")

def test_generate_worksheets(app):
    """Test generating all four worksheet tiers"""
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
            core_concept='Fractions',
            learning_intention='Understand fractions',
            success_criteria=json.dumps(['I can identify fractions']),
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
            date_scheduled=datetime.now()
        )
        db.session.add(lesson)
        db.session.commit()
        lesson_id = lesson.id
        
        worksheets = WorksheetService.generate_worksheets(lesson_id)
        
        assert worksheets is not None
        assert 'mild' in worksheets
        assert 'medium' in worksheets
        assert 'spicy' in worksheets
        assert 'enrichment' in worksheets
        
        assert worksheets['mild'].question_count == 5
        assert worksheets['medium'].question_count == 10
        assert worksheets['spicy'].question_count == 15
        assert worksheets['enrichment'].question_count == 2
        
        print("✅ Generate worksheets: PASS")

def test_mild_tier_has_hints(app):
    """Test that Mild tier questions have hints"""
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
            core_concept='Fractions',
            learning_intention='Understand fractions',
            success_criteria=json.dumps(['I can identify fractions']),
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
            date_scheduled=datetime.now()
        )
        db.session.add(lesson)
        db.session.commit()
        lesson_id = lesson.id
        
        worksheets = WorksheetService.generate_worksheets(lesson_id)
        mild_ws = worksheets['mild']
        
        questions = WorksheetService.get_questions(mild_ws.id)
        
        assert len(questions) == 5
        for q in questions:
            assert q.hints is not None
        
        print("✅ Mild tier has hints: PASS")

def test_get_worksheets_by_lesson(app):
    """Test retrieving all worksheets for a lesson"""
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
            core_concept='Fractions',
            learning_intention='Understand fractions',
            success_criteria=json.dumps(['I can identify fractions']),
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
            date_scheduled=datetime.now()
        )
        db.session.add(lesson)
        db.session.commit()
        lesson_id = lesson.id
        
        WorksheetService.generate_worksheets(lesson_id)
        worksheets = WorksheetService.get_worksheets_by_lesson(lesson_id)
        
        assert len(worksheets) == 4
        tiers = {ws.tier for ws in worksheets}
        assert tiers == {'mild', 'medium', 'spicy', 'enrichment'}
        
        print("✅ Get worksheets by lesson: PASS")

def test_get_questions(app):
    """Test retrieving questions from a worksheet"""
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
            core_concept='Fractions',
            learning_intention='Understand fractions',
            success_criteria=json.dumps(['I can identify fractions']),
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
            date_scheduled=datetime.now()
        )
        db.session.add(lesson)
        db.session.commit()
        lesson_id = lesson.id
        
        worksheets = WorksheetService.generate_worksheets(lesson_id)
        medium_ws = worksheets['medium']
        
        questions = WorksheetService.get_questions(medium_ws.id)
        
        assert len(questions) == 10
        for i, q in enumerate(questions, 1):
            assert q.question_number == i
        
        print("✅ Get questions: PASS")

def test_get_worksheet_by_tier(app):
    """Test getting worksheet for a specific tier"""
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
            core_concept='Fractions',
            learning_intention='Understand fractions',
            success_criteria=json.dumps(['I can identify fractions']),
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
            date_scheduled=datetime.now()
        )
        db.session.add(lesson)
        db.session.commit()
        lesson_id = lesson.id
        
        WorksheetService.generate_worksheets(lesson_id)
        
        spicy = WorksheetService.get_worksheet_by_tier(lesson_id, 'spicy')
        
        assert spicy is not None
        assert spicy.tier == 'spicy'
        assert spicy.question_count == 15
        
        print("✅ Get worksheet by tier: PASS")

def test_update_question(app):
    """Test updating a question"""
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
            core_concept='Fractions',
            learning_intention='Understand fractions',
            success_criteria=json.dumps(['I can identify fractions']),
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
            date_scheduled=datetime.now()
        )
        db.session.add(lesson)
        db.session.commit()
        lesson_id = lesson.id
        
        worksheets = WorksheetService.generate_worksheets(lesson_id)
        medium_ws = worksheets['medium']
        
        questions = WorksheetService.get_questions(medium_ws.id)
        q = questions[0]
        
        updated = WorksheetService.update_question(
            q.id,
            question_text='Updated question text',
            model_answer='Updated answer'
        )
        
        assert updated.question_text == 'Updated question text'
        assert updated.model_answer == 'Updated answer'
        
        print("✅ Update question: PASS")

def test_worksheet_to_dict(app):
    """Test worksheet to_dict conversion"""
    with app.app_context():
        teacher = Teacher(
            email='teacher9@test.com',
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
            core_concept='Fractions',
            learning_intention='Understand fractions',
            success_criteria=json.dumps(['I can identify fractions']),
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
            date_scheduled=datetime.now()
        )
        db.session.add(lesson)
        db.session.commit()
        lesson_id = lesson.id
        
        worksheets = WorksheetService.generate_worksheets(lesson_id)
        mild_ws = worksheets['mild']
        
        ws_dict = mild_ws.to_dict()
        
        assert isinstance(ws_dict, dict)
        assert ws_dict['tier'] == 'mild'
        assert ws_dict['question_count'] == 5
        assert 'created_at' in ws_dict
        
        print("✅ Worksheet to_dict: PASS")

def test_question_to_dict(app):
    """Test question to_dict conversion"""
    with app.app_context():
        teacher = Teacher(
            email='teacher10@test.com',
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
            core_concept='Fractions',
            learning_intention='Understand fractions',
            success_criteria=json.dumps(['I can identify fractions']),
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
            date_scheduled=datetime.now()
        )
        db.session.add(lesson)
        db.session.commit()
        lesson_id = lesson.id
        
        worksheets = WorksheetService.generate_worksheets(lesson_id)
        mild_ws = worksheets['mild']
        
        questions = WorksheetService.get_questions(mild_ws.id)
        q = questions[0]
        
        q_dict = q.to_dict()
        
        assert isinstance(q_dict, dict)
        assert q_dict['question_number'] == 1
        assert q_dict['tier'] == 'mild'
        assert 'question_text' in q_dict
        
        print("✅ Question to_dict: PASS")

def test_regenerate_worksheets_clears_old(app):
    """Test that regenerating worksheets clears old ones"""
    with app.app_context():
        teacher = Teacher(
            email='teacher11@test.com',
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
            core_concept='Fractions',
            learning_intention='Understand fractions',
            success_criteria=json.dumps(['I can identify fractions']),
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
            date_scheduled=datetime.now()
        )
        db.session.add(lesson)
        db.session.commit()
        lesson_id = lesson.id
        
        WorksheetService.generate_worksheets(lesson_id)
        first_ws = WorksheetService.get_worksheets_by_lesson(lesson_id)
        first_ids = {ws.id for ws in first_ws}
        
        WorksheetService.generate_worksheets(lesson_id)
        second_ws = WorksheetService.get_worksheets_by_lesson(lesson_id)
        second_ids = {ws.id for ws in second_ws}
        
        assert first_ids != second_ids
        assert len(second_ws) == 4
        
        print("✅ Regenerate worksheets clears old: PASS")
