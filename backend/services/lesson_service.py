"""Lesson Service - business logic for Lessons"""
from backend.core.database import db
from backend.models.lesson import Lesson
from backend.models.learning_experience import LearningExperience
from datetime import datetime

class LessonService:
    """Service for managing Lessons"""
    
    @staticmethod
    def create_lesson(teacher_id, learning_experience_id, week_number, date_scheduled, 
                     duration_minutes=60, location=None, notes=None):
        """
        Create a new Lesson (instance of LE in weekly plan)
        
        Args:
            teacher_id: ID of teacher
            learning_experience_id: ID of Learning Experience
            week_number: Week number
            date_scheduled: Datetime when lesson is scheduled
            duration_minutes: Duration of lesson (default 60)
            location: Where lesson is held
            notes: Any notes about the lesson
        
        Returns:
            Lesson object
        """
        # Verify LE exists and belongs to teacher
        le = LearningExperience.query_by_id(learning_experience_id)
        if not le or le.teacher_id != teacher_id:
            return None
        
        lesson = Lesson(
            teacher_id=teacher_id,
            learning_experience_id=learning_experience_id,
            week_number=week_number,
            date_scheduled=date_scheduled,
            duration_minutes=duration_minutes,
            location=location,
            notes=notes,
            status='draft'
        )
        
        db.session.add(lesson)
        db.session.commit()
        
        return lesson
    
    @staticmethod
    def get_lesson(lesson_id):
        """Get a Lesson by ID"""
        return Lesson.query_by_id(lesson_id)
    
    @staticmethod
    def get_week_lessons(teacher_id, week_number):
        """Get all published lessons for a teacher in a week"""
        return Lesson.find_by_teacher_and_week(teacher_id, week_number)
    
    @staticmethod
    def get_all_lessons(teacher_id):
        """Get all lessons for a teacher"""
        return Lesson.find_by_teacher(teacher_id)
    
    @staticmethod
    def get_le_lessons(learning_experience_id):
        """Get all scheduled lessons for a Learning Experience"""
        return Lesson.find_by_le(learning_experience_id)
    
    @staticmethod
    def update_lesson(lesson_id, **kwargs):
        """
        Update a Lesson
        
        Args:
            lesson_id: ID of lesson to update
            **kwargs: Fields to update
        
        Returns:
            Updated Lesson object
        """
        lesson = Lesson.query_by_id(lesson_id)
        if not lesson:
            return None
        
        for key, value in kwargs.items():
            if hasattr(lesson, key) and key != 'status':  # Don't allow direct status change
                setattr(lesson, key, value)
        
        db.session.commit()
        return lesson
    
    @staticmethod
    def publish_lesson(lesson_id):
        """Publish a lesson to make it visible in weekly plan"""
        lesson = Lesson.query_by_id(lesson_id)
        if not lesson:
            return None
        
        lesson.publish()
        return lesson
    
    @staticmethod
    def mark_lesson_taught(lesson_id):
        """Mark a lesson as taught"""
        lesson = Lesson.query_by_id(lesson_id)
        if not lesson:
            return None
        
        lesson.mark_taught()
        return lesson
    
    @staticmethod
    def archive_lesson(lesson_id):
        """Archive a lesson"""
        lesson = Lesson.query_by_id(lesson_id)
        if not lesson:
            return None
        
        lesson.archive()
        return lesson
    
    @staticmethod
    def delete_lesson(lesson_id):
        """Delete a lesson"""
        lesson = Lesson.query_by_id(lesson_id)
        if not lesson:
            return None
        
        db.session.delete(lesson)
        db.session.commit()
        return True
