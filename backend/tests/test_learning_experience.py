"""Tests for LearningExperience model"""
import pytest
import json
from backend.main import create_app
from backend.core.database import db
from backend.models.teacher import Teacher
from backend.models.learning_experience import LearningExperience

@pytest.fixture
def app():
    """Create test app"""
    app = create_app('development')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

def test_learning_experience_creation(app):
    """Test that LearningExperience can be created"""
    with app.app_context():
        # Create teacher in same session
        teacher = Teacher(
            email='teacher@test.com',
            first_name='Test',
            last_name='Teacher',
            password_hash='hash123'
        )
        db.session.add(teacher)
        db.session.commit()
        teacher_id = teacher.id
        
        # Create LE in same session
        le = LearningExperience(
            teacher_id=teacher_id,
            unit_number=22,
            experience_number=1,
            core_concept='Comparing Fractions',
            learning_intention='Use visual models to compare fractions',
            success_criteria=json.dumps([
                'I can draw models to compare fractions',
                'I can find common denominators',
                'I can order fractions from smallest to largest'
            ]),
            subject='Maths',
            year_level=6,
            nesa_outcome_code='MA3-RN-01'
        )
        db.session.add(le)
        db.session.commit()
        
        assert le.id is not None
        assert le.teacher_id == teacher_id
        print("✅ LearningExperience creation: PASS")

def test_learning_experience_to_dict(app):
    """Test that LearningExperience converts to dict"""
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
            core_concept='Comparing Fractions',
            learning_intention='Use visual models to compare fractions',
            success_criteria=json.dumps(['I can compare fractions']),
            subject='Maths',
            year_level=6
        )
        db.session.add(le)
        db.session.commit()
        
        le_dict = le.to_dict()
        
        assert isinstance(le_dict, dict)
        assert le_dict['core_concept'] == 'Comparing Fractions'
        assert le_dict['subject'] == 'Maths'
        assert le_dict['unit_number'] == 22
        assert 'created_at' in le_dict
        assert 'updated_at' in le_dict
        print("✅ LearningExperience to_dict: PASS")

def test_learning_experience_success_criteria_list(app):
    """Test success criteria list conversion"""
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
        
        criteria = [
            'I can draw models to compare fractions',
            'I can find common denominators',
            'I can order fractions'
        ]
        
        le = LearningExperience(
            teacher_id=teacher_id,
            unit_number=22,
            experience_number=1,
            core_concept='Comparing Fractions',
            learning_intention='Test',
            success_criteria=json.dumps(criteria),
            subject='Maths',
            year_level=6
        )
        db.session.add(le)
        db.session.commit()
        
        retrieved_criteria = le.get_success_criteria_list()
        assert isinstance(retrieved_criteria, list)
        assert len(retrieved_criteria) == 3
        assert retrieved_criteria[0] == 'I can draw models to compare fractions'
        print("✅ LearningExperience success_criteria_list: PASS")

def test_find_by_teacher(app):
    """Test finding LEs by teacher"""
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
        
        for i in range(3):
            le = LearningExperience(
                teacher_id=teacher_id,
                unit_number=22,
                experience_number=i+1,
                core_concept=f'Concept {i}',
                learning_intention='Test',
                success_criteria='[]',
                subject='Maths',
                year_level=6
            )
            db.session.add(le)
        db.session.commit()
        
        les = LearningExperience.find_by_teacher(teacher_id)
        assert len(les) == 3
        print("✅ LearningExperience find_by_teacher: PASS")

def test_find_by_unit(app):
    """Test finding LEs by unit"""
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
        
        le1 = LearningExperience(
            teacher_id=teacher_id,
            unit_number=22,
            experience_number=1,
            core_concept='Concept 1',
            learning_intention='Test',
            success_criteria='[]',
            subject='Maths',
            year_level=6
        )
        le2 = LearningExperience(
            teacher_id=teacher_id,
            unit_number=23,
            experience_number=1,
            core_concept='Concept 2',
            learning_intention='Test',
            success_criteria='[]',
            subject='Maths',
            year_level=6
        )
        db.session.add(le1)
        db.session.add(le2)
        db.session.commit()
        
        unit_22_les = LearningExperience.find_by_unit(teacher_id, 22)
        assert len(unit_22_les) == 1
        assert unit_22_les[0].unit_number == 22
        print("✅ LearningExperience find_by_unit: PASS")

def test_learning_experience_query_by_id(app):
    """Test querying LE by ID"""
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
        
        retrieved = LearningExperience.query_by_id(le_id)
        assert retrieved is not None
        assert retrieved.id == le_id
        print("✅ LearningExperience query_by_id: PASS")
