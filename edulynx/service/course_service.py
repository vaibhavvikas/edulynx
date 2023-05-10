from typing import List

import logging

from fastapi import HTTPException

from edulynx.enums import ChapterRating, CourseSort, DomainFilter
from edulynx.models.course import ChapterModel, CourseModel
from edulynx.repository.course_repository import CourseRepository

log = logging.getLogger(__name__)


class CourseService:
    def __init__(self, repo: CourseRepository):
        self.repo = repo

    def get_courses(
        self, sort: CourseSort | None = None, filter: DomainFilter | None = None
    ) -> List[CourseModel]:
        try:
            courses = self.repo.get_courses(sort, filter)
            if not courses or len(courses) == 0:
                raise HTTPException(
                    status_code=422, detail="There are no courses in the system"
                )
        except Exception as e:
            log.error("[CourseService][get_courses]: " + str(e))
            raise e
        return courses

    def get_course_by_id(self, course_id: str) -> CourseModel:
        try:
            course = self.repo.get_course_by_id(course_id)
            if not course:
                raise HTTPException(
                    status_code=422,
                    detail=f"There is no course with the following course_id in the system: {course_id}",
                )
        except Exception as e:
            log.error("[CourseService][get_course_by_id]: " + str(e))
            raise e
        return course

    def get_chapter_by_index(self, course_id: str, index: int) -> ChapterModel:
        try:
            chapter = self.repo.get_chapter_by_index(course_id, index)
            if not chapter:
                raise HTTPException(
                    status_code=422,
                    detail=f"There is no chapter with the following course_id: {course_id} and index: {index} in the system.",
                )
        except Exception as e:
            log.error("[CourseService][get_chapter_by_index]: " + str(e))
            raise e
        return chapter

    def rate_chapter_by_index(
        self, course_id: str, index: int, rating: ChapterRating
    ) -> ChapterModel:
        try:
            chapter = self.repo.rate_chapter_by_index(course_id, index, rating)
            if not chapter:
                raise HTTPException(
                    status_code=422,
                    detail=f"There is no chapter with the following course_id: {course_id} and index: {index} in the system.",
                )
        except Exception as e:
            log.error("[CourseService][get_chapter_by_index]: " + str(e))
            raise e
        return chapter
