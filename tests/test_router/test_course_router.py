"""Tests for hello function."""
import pytest
from fastapi.testclient import TestClient

from edulynx.__main__ import app
from edulynx.repository.course_repository import CourseRepository

client = TestClient(app)


########################## Test GET /courses APIs ##########################


def test_get_courses():
    response = client.get(f"/courses")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "sort",
    [
        ("alphabetical"),
        ("date"),
        ("rating"),
    ],
)
def test_get_courses_with_sort(sort):
    response = client.get(f"/courses?sort={sort}")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "filter",
    [
        ("computer%20vision"),
        ("programming"),
        ("mathematics"),
    ],
)
def test_get_courses_with_filter(filter):
    response = client.get(f"/courses?filter={filter}")
    assert response.status_code == 200


def test_get_courses_with_invalid_sort():
    response = client.get(f"/courses?sort=invalid_str")
    assert response.status_code == 422


def test_get_courses_with_invalid_filter():
    response = client.get(f"/courses?filter=invalid_str")
    assert response.status_code == 422


############################ Test GET /courses/{course_id} API ############################

repo = CourseRepository()


def test_get_courses_by_id():
    courses = repo.get_courses()
    course_id = courses[0].id
    response = client.get(f"/courses/{course_id}")
    assert response.status_code == 200


def test_get_courses_by_id_invalid_id():
    response = client.get("/courses/invalid_id")
    assert response.status_code == 422


###################### Test GET /courses/{course_id}/chapters/index API ######################


def test_get_chapters_by_index():
    courses = repo.get_courses()
    course_id = courses[0].id
    response = client.get(f"/courses/{course_id}/chapters/1")
    assert response.status_code == 200


def test_get_chapters_by_index_invalid_index():
    courses = repo.get_courses()
    course_id = courses[0].id
    response = client.get(f"/courses/{course_id}/chapters/99")
    assert response.status_code == 422


def test_get_chapters_by_index_invalid_chapter_id():
    response = client.get(f"/courses/invalid_str/chapters/1")
    assert response.status_code == 422


def test_get_chapters_by_index_invalid_course_id_and_index():
    response = client.get(f"/courses/invalid_str/chapters/99")
    assert response.status_code == 422


##################### Test PUT /courses/{course_id}/chapters/index/rate API #####################


def test_rate_chapters_by_index_positive():
    courses = repo.get_courses()
    course_id = str(courses[0].id)
    initial_chapter = courses[0].chapters[0]
    response = client.put(f"/courses/{course_id}/chapters/1/rate?rating=positive")
    assert response.status_code == 200
    chapter = repo.get_chapter_by_index(course_id, 1)
    assert chapter.ratings_count == initial_chapter.ratings_count + 1
    assert chapter.ratings_total == initial_chapter.ratings_total + 1


def test_rate_chapters_by_index_negative():
    courses = repo.get_courses()
    course_id = str(courses[0].id)
    initial_chapter = courses[0].chapters[0]
    response = client.put(f"/courses/{course_id}/chapters/1/rate?rating=negative")
    assert response.status_code == 200
    chapter = repo.get_chapter_by_index(course_id, 1)
    assert chapter.ratings_count == initial_chapter.ratings_count + 1
    assert chapter.ratings_total == initial_chapter.ratings_total


def test_rate_chapters_by_index_invalid_rating():
    courses = repo.get_courses()
    course_id = str(courses[0].id)
    response = client.put(f"/courses/{course_id}/chapters/1/rate?rating=invalid")
    assert response.status_code == 422
