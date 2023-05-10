from typing import Any, List

import logging

from fastapi import APIRouter, HTTPException, status

from edulynx.enums import ChapterRating, CourseSort, DomainFilter
from edulynx.models.course import ChapterModel, CourseModel
from edulynx.repository.course_repository import CourseRepository
from edulynx.service.course_service import CourseService

log = logging.getLogger(__name__)
router = APIRouter(prefix="/courses")
repo = CourseRepository()
service = CourseService(repo)


@router.get("", response_model=List[CourseModel])
async def get_courses(
    sort: CourseSort | None = None, filter: DomainFilter | None = None
) -> Any:
    try:
        courses = service.get_courses(sort, filter)
    except HTTPException as e:
        raise e
    except Exception as e:
        log.error("[CourseRouter][get_courses]: " + str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
    return courses


@router.get("/{course_id}", response_model=CourseModel)
async def get_course_by_id(course_id: str) -> Any:
    try:
        course = service.get_course_by_id(course_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        log.error("[CourseRouter][get_course_by_id]: " + str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
    return course


@router.get("/{course_id}/chapters/{index}", response_model=ChapterModel)
async def get_chapter_by_index(course_id: str, index: int) -> Any:
    try:
        chapter = service.get_chapter_by_index(course_id, index)
    except HTTPException as e:
        raise e
    except Exception as e:
        log.error("[CourseRouter][get_course_by_id]: " + str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
    return chapter


@router.put("/{course_id}/chapters/{index}/rate", response_model=ChapterModel)
async def rate_chapter_by_index(
    course_id: str, index: int, rating: ChapterRating
) -> Any:
    try:
        chapter = service.rate_chapter_by_index(course_id, index, rating)
    except HTTPException as e:
        raise e
    except Exception as e:
        log.error("[CourseRouter][rate_chapter_by_index]: " + str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
    return chapter
