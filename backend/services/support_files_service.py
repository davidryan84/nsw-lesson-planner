"""Support Files Service - generates all teacher support files"""
from backend.services.teacher_guide_generator import TeacherGuideGenerator
from backend.services.answer_sheet_generator import AnswerSheetGenerator
from backend.services.exemplar_generator import ExemplarGenerator
from backend.core.database import db
from backend.models.lesson import Lesson
import os

class SupportFilesService:
    """Coordinate generation of all support files for a lesson"""
    
    @staticmethod
    def generate_all(lesson_id, output_dir='/tmp'):
        """
        Generate all support files (Teacher Guide, Answer Sheet, Exemplar)
        
        Args:
            lesson_id: ID of lesson
            output_dir: Where to save files
        
        Returns:
            Dictionary with all generated files
        """
        results = {}
        
        try:
            # Generate Teacher Guide
            guide_result = TeacherGuideGenerator.generate(lesson_id, output_dir)
            if guide_result:
                results['teacher_guide'] = guide_result
        except Exception as e:
            results['teacher_guide_error'] = str(e)
        
        try:
            # Generate Answer Sheet
            answer_result = AnswerSheetGenerator.generate(lesson_id, output_dir)
            if answer_result:
                results['answer_sheet'] = answer_result
        except Exception as e:
            results['answer_sheet_error'] = str(e)
        
        try:
            # Generate Exemplar
            exemplar_result = ExemplarGenerator.generate(lesson_id, output_dir)
            if exemplar_result:
                results['exemplar'] = exemplar_result
        except Exception as e:
            results['exemplar_error'] = str(e)
        
        return results
    
    @staticmethod
    def generate_teacher_guide(lesson_id, output_dir='/tmp'):
        """Generate only teacher guide"""
        return TeacherGuideGenerator.generate(lesson_id, output_dir)
    
    @staticmethod
    def generate_answer_sheet(lesson_id, output_dir='/tmp'):
        """Generate only answer sheet"""
        return AnswerSheetGenerator.generate(lesson_id, output_dir)
    
    @staticmethod
    def generate_exemplar(lesson_id, output_dir='/tmp'):
        """Generate only exemplar"""
        return ExemplarGenerator.generate(lesson_id, output_dir)
