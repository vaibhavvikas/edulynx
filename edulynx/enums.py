from enum import Enum


class CourseSort(str, Enum):
    alphabetical = "alphabetical"
    date = "date"
    rating = "rating"


class DomainFilter(str, Enum):
    computer_vision = "computer vision"
    artificial_intelligence = "artificial intelligence"
    programming = "programming"
    mathematics = "mathematics"


class ChapterRating(str, Enum):
    positive = "positive"
    negative = "negative"
