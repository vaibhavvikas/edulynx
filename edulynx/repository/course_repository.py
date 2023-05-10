from typing import List

import logging
import os

from bson.errors import InvalidId
from bson.objectid import ObjectId

from edulynx.database import get_collection
from edulynx.enums import ChapterRating, CourseSort, DomainFilter
from edulynx.models.course import ChapterModel, CourseModel

log = logging.getLogger(__name__)


class CourseRepository:
    def __init__(self):
        self.collection = get_collection(os.getenv("COURSES_COLLECTION"))

    def get_courses(
        self, sort: CourseSort | None = None, filter: DomainFilter | None = None
    ) -> List[CourseModel]:
        try:
            query = {}
            if filter:
                query["domain"] = filter.value

            if not sort or sort == CourseSort.alphabetical:
                courses = self.collection.find(query).sort("name", 1)
            elif sort == CourseSort.date:
                courses = self.collection.find(query).sort("date", -1)
            elif sort == CourseSort.rating:
                courses = self.collection.find(query).sort("ratings", -1)
            else:
                courses = self.collection.find(query)
        except Exception as e:
            log.error("[CourseRepository][get_courses]: " + str(e))
            raise e
        return [CourseModel(id=str(course["_id"]), **course) for course in courses]

    def get_course_by_id(self, course_id: str) -> CourseModel:
        try:
            course = self.collection.find_one({"_id": ObjectId(course_id)})
            if not course:
                log.error(
                    f"There is no course with the follwoing course_id: {course_id}"
                )
                return None
        except InvalidId as e:
            log.error(
                f"[CourseRepository][get_course_by_id]: Invalid course_id: {course_id}"
            )
            return None
        except Exception as e:
            log.error("[CourseRepository][get_course_by_id]: " + str(e))
            raise e
        return CourseModel(**course)

    def get_chapter_by_index(self, course_id: str, index: int) -> ChapterModel | None:
        try:
            course = self.get_course_by_id(course_id)
            if not course:
                log.error(
                    f"There is no course with the follwoing course_id: {course_id}"
                )
                return None

            for chapter in course.chapters:
                if chapter.chapter_no == index:
                    return chapter

            log.error(f"There is no chapter with the following index: {index}")
            return None
        except Exception as e:
            log.error("[CourseRepository][get_chapter_by_index]: " + str(e))
            raise e

    def rate_chapter_by_index(
        self, course_id: str, index: int, rating: ChapterRating
    ) -> ChapterModel | None:
        try:
            chapter = self.get_chapter_by_index(course_id, index)
            if not chapter:
                log.error("There is no chapter in the system")
                return None

            if rating == ChapterRating.positive:
                chapter.ratings_total += 1
            elif rating == ChapterRating.negative:
                pass
            else:
                log.error("[CourseRepository][rate_chapter_by_index]")
                raise Exception("Invalid rating!")
            chapter.ratings_count += 1

            result = self.collection.update_one(
                {"_id": ObjectId(course_id), "chapters.chapter_no": index},
                {
                    "$set": {
                        "chapters.$.ratings_total": chapter.ratings_total,
                        "chapters.$.ratings_count": chapter.ratings_count,
                    }
                },
            )

            if result.matched_count == 0:
                log.error("Error updating the collection")

            course = self.get_course_by_id(course_id)
            new_rating_count = course.ratings_count + 1

            add_rating = 0
            if rating == ChapterRating.positive:
                add_rating += 1

            new_rating = (
                course.ratings * course.ratings_count + add_rating
            ) / new_rating_count
            result = self.collection.update_one(
                {"_id": ObjectId(course_id)},
                {"$set": {"ratings": new_rating, "ratings_count": new_rating_count}},
            )
            if result.matched_count == 0:
                log.error("Error updating the collection")

        except Exception as e:
            log.error("[CourseRepository][rate_chapter_by_index]: " + str(e))
            raise e
        return chapter
