"""Worksheet Service - business logic for worksheet generation"""
from backend.core.database import db
from backend.models.worksheet import Worksheet
from backend.models.worksheet_question import WorksheetQuestion
from backend.models.lesson import Lesson
from backend.models.learning_experience import LearningExperience
import json

class WorksheetService:
    """Service for managing and generating worksheets"""
    
    @staticmethod
    def generate_worksheets(lesson_id):
        """
        Generate all four tiered worksheets for a lesson
        
        Args:
            lesson_id: ID of lesson to generate worksheets for
        
        Returns:
            Dictionary with all four worksheets
        """
        lesson = Lesson.query_by_id(lesson_id)
        if not lesson:
            return None
        
        le = LearningExperience.query_by_id(lesson.learning_experience_id)
        if not le:
            return None
        
        # Delete any existing worksheets for this lesson
        existing = Worksheet.find_by_lesson(lesson_id)
        for ws in existing:
            # Delete all questions first
            db.session.query(WorksheetQuestion).filter_by(worksheet_id=ws.id).delete()
            # Then delete the worksheet
            db.session.delete(ws)
        db.session.commit()
        
        # Generate all four tiers
        worksheets = {}
        
        worksheets['mild'] = WorksheetService._generate_tier(
            lesson_id, le, 'mild', 5
        )
        worksheets['medium'] = WorksheetService._generate_tier(
            lesson_id, le, 'medium', 10
        )
        worksheets['spicy'] = WorksheetService._generate_tier(
            lesson_id, le, 'spicy', 15
        )
        worksheets['enrichment'] = WorksheetService._generate_tier(
            lesson_id, le, 'enrichment', 2
        )
        
        return worksheets
    
    @staticmethod
    def _generate_tier(lesson_id, le, tier, question_count):
        """
        Generate a single tier of questions
        
        Args:
            lesson_id: ID of lesson
            le: LearningExperience object
            tier: Tier name (mild, medium, spicy, enrichment)
            question_count: Number of questions to generate
        
        Returns:
            Worksheet object
        """
        # Create worksheet
        worksheet = Worksheet(
            lesson_id=lesson_id,
            tier=tier,
            title=f"{le.core_concept} - {tier.capitalize()}",
            description=f"{tier.capitalize()} tier worksheet for {le.core_concept}",
            subject=le.subject,
            year_level=le.year_level,
            learning_intention=le.learning_intention,
            success_criteria=le.success_criteria,
            question_count=question_count
        )
        
        db.session.add(worksheet)
        db.session.commit()
        
        # Generate questions based on tier
        if tier == 'mild':
            questions = WorksheetService._generate_mild_questions(le, question_count)
        elif tier == 'medium':
            questions = WorksheetService._generate_medium_questions(le, question_count)
        elif tier == 'spicy':
            questions = WorksheetService._generate_spicy_questions(le, question_count)
        else:  # enrichment
            questions = WorksheetService._generate_enrichment_questions(le, question_count)
        
        # Add questions to worksheet
        for i, q in enumerate(questions, 1):
            question = WorksheetQuestion(
                worksheet_id=worksheet.id,
                question_number=i,
                question_text=q['text'],
                tier=tier,
                hints=q.get('hints'),
                model_answer=q.get('model_answer'),
                difficulty_level=q.get('difficulty_level')
            )
            db.session.add(question)
        
        db.session.commit()
        
        return worksheet
    
    @staticmethod
    def _generate_mild_questions(le, count):
        """Generate Mild tier questions (with scaffolding)"""
        questions = []
        for i in range(count):
            questions.append({
                'text': f"Q{i+1}: [Scaffold question about {le.core_concept}]",
                'hints': json.dumps([f"Hint {i+1}: Consider..."]),
                'model_answer': f"Sample answer for mild question {i+1}",
                'difficulty_level': 'Remember/Understand'
            })
        return questions
    
    @staticmethod
    def _generate_medium_questions(le, count):
        """Generate Medium tier questions (grade level)"""
        questions = []
        for i in range(count):
            questions.append({
                'text': f"Q{i+1}: [Grade-level question about {le.core_concept}]",
                'model_answer': f"Sample answer for medium question {i+1}",
                'difficulty_level': 'Apply/Analyze'
            })
        return questions
    
    @staticmethod
    def _generate_spicy_questions(le, count):
        """Generate Spicy tier questions (challenging)"""
        questions = []
        for i in range(count):
            questions.append({
                'text': f"Q{i+1}: [Challenging question about {le.core_concept} - explain your reasoning]",
                'model_answer': f"Sample answer for spicy question {i+1}",
                'difficulty_level': 'Analyze/Evaluate/Create'
            })
        return questions
    
    @staticmethod
    def _generate_enrichment_questions(le, count):
        """Generate Enrichment questions (real-world application)"""
        questions = []
        for i in range(count):
            questions.append({
                'text': f"Q{i+1}: [Real-world scenario requiring {le.core_concept}]",
                'model_answer': f"Sample answer for enrichment question {i+1}",
                'difficulty_level': 'Create/Evaluate'
            })
        return questions
    
    @staticmethod
    def get_worksheet(worksheet_id):
        """Get a worksheet by ID"""
        return Worksheet.query_by_id(worksheet_id)
    
    @staticmethod
    def get_worksheets_by_lesson(lesson_id):
        """Get all worksheets for a lesson"""
        return Worksheet.find_by_lesson(lesson_id)
    
    @staticmethod
    def get_worksheet_by_tier(lesson_id, tier):
        """Get worksheet for a specific tier"""
        return Worksheet.find_by_lesson_and_tier(lesson_id, tier)
    
    @staticmethod
    def get_questions(worksheet_id):
        """Get all questions for a worksheet"""
        return WorksheetQuestion.find_by_worksheet(worksheet_id)
    
    @staticmethod
    def update_question(question_id, **kwargs):
        """Update a worksheet question"""
        question = WorksheetQuestion.query_by_id(question_id)
        if not question:
            return None
        
        for key, value in kwargs.items():
            if hasattr(question, key):
                setattr(question, key, value)
        
        db.session.commit()
        return question
