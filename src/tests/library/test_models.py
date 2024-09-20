import pytest
from django.core.exceptions import ValidationError
from model_bakery import baker

from library.models import Author


@pytest.mark.django_db
class TestAuthor:
    def test_mandatory_fields(self):
        with pytest.raises(ValidationError) as error:
            Author.objects.create()
        assert list(error.value.error_dict.keys()) == ["name"]

    def test_valid(self):
        author = baker.make(Author)
        expected = {
            "id": author.id,
            "created": author.created,
            "modified": author.modified,
            "name": author.name,
        }
        for field in [field.name for field in Author._meta.get_fields()]:
            assert getattr(author, field) == expected[field]
