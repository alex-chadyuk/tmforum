import pytest
from tmforum import (
    CharacteristicSpecification,
    Process,
    StringCharacteristicValueSpecification,
    TaskRef,
)


def string_value_spec(value):
    return {"@type": "StringCharacteristicValueSpecification", "value": value}


def parse_value_specs(items):
    spec = CharacteristicSpecification.from_dict(
        {
            "@type": "CharacteristicSpecification",
            "characteristicValueSpecification": items,
        }
    )
    return spec.characteristicValueSpecification


@pytest.mark.parametrize(
    "type_name",
    [
        "NoSuchCharacteristicValueSpecification",
        "Context",  # a class of the module, but not an Entity
    ],
)
def test_list_item_of_unknown_type_after_known_item_is_dropped(type_name, capsys):
    result = parse_value_specs([string_value_spec("a"), {"@type": type_name}])

    assert len(result) == 1
    assert isinstance(result[0], StringCharacteristicValueSpecification)
    assert result[0].value == "a"
    assert f"Unknown entity type {type_name}" in capsys.readouterr().out


def test_list_item_of_unknown_type_first_is_dropped(capsys):
    result = parse_value_specs(
        [{"@type": "NoSuchCharacteristicValueSpecification"}, string_value_spec("b")]
    )

    assert [v.value for v in result] == ["b"]
    assert (
        "Unknown entity type NoSuchCharacteristicValueSpecification"
        in capsys.readouterr().out
    )


def test_list_item_of_unknown_type_does_not_duplicate_its_neighbours():
    result = parse_value_specs(
        [
            string_value_spec("a"),
            {"@type": "NoSuchCharacteristicValueSpecification", "value": True},
            string_value_spec("b"),
            {"@type": "NoSuchCharacteristicValueSpecification", "value": False},
        ]
    )

    assert [v.value for v in result] == ["a", "b"]


def test_every_dropped_list_item_is_reported(capsys):
    parse_value_specs(
        [
            {"@type": "NoSuchFirst"},
            string_value_spec("a"),
            {"@type": "NoSuchSecond"},
        ]
    )

    out = capsys.readouterr().out
    assert "Unknown entity type NoSuchFirst" in out
    assert "Unknown entity type NoSuchSecond" in out


def test_untyped_union_list_item_that_no_member_parses_is_dropped():
    # A list where a string belongs makes both Task.from_dict and TaskRef.from_dict raise.
    process = Process.from_dict(
        {
            "@type": "Process",
            "task": [
                {"@type": "TaskRef", "id": "4fd-ty56-gg55-2"},
                {"id": "4fd-ty56-gg55-3", "name": ["not", "a", "string"]},
            ],
        }
    )

    assert len(process.task) == 1
    assert isinstance(process.task[0], TaskRef)
    assert process.task[0].id == "4fd-ty56-gg55-2"
