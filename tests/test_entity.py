"""Behaviour of Entity.from_dict / to_dict itself, rather than of one TMF API."""

import dataclasses
import json
import logging
from typing import Optional, Union

import pytest
import tmforum
from tmforum import (
    Attachment,
    AttachmentRef,
    CharacteristicSpecification,
    Entity,
    FromDictError,
    Intent,
    IntentRef,
    IntentReport,
    ObjectCharacteristic,
    Process,
    Product,
    ProductOfferingPrice,
    ProductOfferingPriceTable,
    ProductOrderItem,
    ProductRef,
    ResourceRefOrValue,
    StringCharacteristicValueSpecification,
    Task,
    TaskRef,
    TaskSpecification,
    TargetResourceSchema,
)


@dataclasses.dataclass(repr=False)
class _Picky(Entity):
    """Test-only entity that refuses to be built without an id."""

    id: Optional[str] = None
    picky: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        if not self.id:
            raise ValueError("_Picky requires an id")


@dataclasses.dataclass(repr=False)
class _AlsoPicky(Entity):
    id: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        if not self.id:
            raise ValueError("_AlsoPicky requires an id")


@dataclasses.dataclass(repr=False)
class _Holder(Entity):
    """Declares a union whose members both reject an object without an id."""

    either: Optional[Union[_Picky, _AlsoPicky]] = None


@pytest.fixture(autouse=True)
def parse_log(caplog):
    caplog.set_level(logging.DEBUG, logger="tmforum")
    return caplog


def warnings_of(caplog):
    return [r.getMessage() for r in caplog.records if r.levelno == logging.WARNING]


def value_spec_payload(value):
    return {"@type": "StringCharacteristicValueSpecification", "value": value}


def char_spec(items):
    return {
        "@type": "CharacteristicSpecification",
        "characteristicValueSpecification": items,
    }


# (id, class, payload, getter for the value that must stay raw, reported path)
UNMAPPABLE = [
    (
        "unknown-type-list-item",
        CharacteristicSpecification,
        char_spec([value_spec_payload("a"), {"@type": "NoSuchSpec", "value": True}]),
        lambda o: o.characteristicValueSpecification[1],
        "CharacteristicSpecification.characteristicValueSpecification[1]",
    ),
    (
        "non-entity-class-as-type",
        CharacteristicSpecification,
        char_spec([{"@type": "Context"}]),
        lambda o: o.characteristicValueSpecification[0],
        "CharacteristicSpecification.characteristicValueSpecification[0]",
    ),
    (
        "unhashable-type",
        CharacteristicSpecification,
        char_spec([{"@type": ["NoSuchSpec"]}]),
        lambda o: o.characteristicValueSpecification[0],
        "CharacteristicSpecification.characteristicValueSpecification[0]",
    ),
    (
        "unknown-type-single-field",
        IntentReport,
        {"@type": "IntentReport", "intent": {"@type": "AcmeIntent", "id": "1"}},
        lambda o: o.intent,
        "IntentReport.intent",
    ),
    (
        "list-for-str",
        Task,
        {"@type": "Task", "name": ["not", "a", "string"]},
        lambda o: o.name,
        "Task.name",
    ),
    (
        "list-for-entity",
        IntentReport,
        {"@type": "IntentReport", "intent": [{"@type": "IntentRef", "id": "1"}]},
        lambda o: o.intent,
        "IntentReport.intent",
    ),
    (
        "list-for-enum",
        Task,
        {"@type": "Task", "state": ["active"]},
        lambda o: o.state,
        "Task.state",
    ),
    (
        "list-for-bool",
        Task,
        {"@type": "Task", "isMandatory": [True]},
        lambda o: o.isMandatory,
        "Task.isMandatory",
    ),
    (
        "object-for-list",
        Process,
        {"@type": "Process", "task": {"@type": "TaskRef", "id": "t1"}},
        lambda o: o.task,
        "Process.task",
    ),
    (
        "scalar-for-list",
        Process,
        {"@type": "Process", "task": "abc"},
        lambda o: o.task,
        "Process.task",
    ),
    (
        "empty-object-for-list",
        Process,
        {"@type": "Process", "task": {}},
        lambda o: o.task,
        "Process.task",
    ),
    (
        "false-for-list",
        Process,
        {"@type": "Process", "task": False},
        lambda o: o.task,
        "Process.task",
    ),
    (
        "scalar-for-entity",
        Attachment,
        {"@type": "Attachment", "size": "2 Mb"},
        lambda o: o.size,
        "Attachment.size",
    ),
    (
        "null-in-entity-list",
        Process,
        {"@type": "Process", "task": [None]},
        lambda o: o.task[0],
        "Process.task[0]",
    ),
    (
        "object-for-str",
        Task,
        {"@type": "Task", "name": {"value": "x"}},
        lambda o: o.name,
        "Task.name",
    ),
    (
        "object-for-enum",
        Task,
        {"@type": "Task", "state": {"value": "active"}},
        lambda o: o.state,
        "Task.state",
    ),
    (
        "nested-validator-rejects",
        ProductOrderItem,
        {"@type": "ProductOrderItem", "product": {"@type": "Product", "id": "p"}},
        lambda o: o.product,
        "ProductOrderItem.product",
    ),
    (
        "no-union-member-accepts",
        _Holder,
        {"either": {"picky": "yes"}},  # no "@type": the class is local to this module
        lambda o: o.either,
        "_Holder.either",
    ),
]


@pytest.mark.parametrize(
    "cls, payload, getter, path",
    [case[1:] for case in UNMAPPABLE],
    ids=[case[0] for case in UNMAPPABLE],
)
def test_unmappable_value_is_kept_raw_and_reported(
    cls, payload, getter, path, parse_log
):
    entity = cls.from_dict(payload)

    raw = getter(entity)
    expected = payload
    for step in path.split(".")[1:]:
        name, _, index = step.partition("[")
        expected = expected[name]
        if index:
            expected = expected[int(index.rstrip("]"))]
    assert raw == expected

    messages = warnings_of(parse_log)
    assert len(messages) == 1
    assert messages[0].startswith(f"{path}: ")


@pytest.mark.parametrize(
    "cls, payload, getter, path",
    [case[1:] for case in UNMAPPABLE],
    ids=[case[0] for case in UNMAPPABLE],
)
def test_unmappable_value_raises_in_strict_mode(cls, payload, getter, path):
    with pytest.raises(FromDictError) as error:
        cls.from_dict(payload, strict=True)

    assert error.value.path == path
    assert str(error.value).startswith(f"{path}: ")


def test_unknown_list_item_does_not_duplicate_its_neighbours(parse_log):
    spec = CharacteristicSpecification.from_dict(
        char_spec(
            [
                value_spec_payload("a"),
                {"@type": "NoSuchSpec", "value": True},
                value_spec_payload("b"),
                {"@type": "NoSuchSpec", "value": False},
            ]
        )
    )

    parsed = spec.characteristicValueSpecification
    assert [v.value for v in parsed if isinstance(v, Entity)] == ["a", "b"]
    assert parsed[1] == {"@type": "NoSuchSpec", "value": True}
    assert parsed[3] == {"@type": "NoSuchSpec", "value": False}
    assert len(warnings_of(parse_log)) == 2


def test_each_unmappable_list_item_is_reported_once(parse_log):
    CharacteristicSpecification.from_dict(
        char_spec(
            [
                {"@type": "NoSuchFirst"},
                value_spec_payload("a"),
                {"@type": "NoSuchSecond"},
            ]
        )
    )

    messages = warnings_of(parse_log)
    assert len(messages) == 2
    assert "NoSuchFirst" in messages[0]
    assert "NoSuchSecond" in messages[1]


def test_top_level_unknown_type_parses_as_the_called_class(parse_log):
    task = Task.from_dict({"@type": "AcmeTask", "id": "t1", "acmeField": 7})

    assert isinstance(task, Task)
    assert task.id == "t1"
    assert len(warnings_of(parse_log)) == 1
    assert task.to_dict() == {"@type": "AcmeTask", "id": "t1", "acmeField": 7}


def test_exact_type_outside_the_declared_type_is_honoured(parse_log):
    resource = ResourceRefOrValue.from_dict(
        {
            "@type": "ResourceRefOrValue",
            "attachment": [{"@type": "AttachmentRef", "id": "a1"}],
        }
    )

    assert isinstance(resource.attachment[0], AttachmentRef)
    assert warnings_of(parse_log) == []


@pytest.mark.parametrize("strict", [False, True])
def test_base_type_fallback_in_a_list_item(strict, parse_log):
    payload = {
        "@type": "Process",
        "relatedEntity": [
            {
                "@type": "AcmeRelatedEntity",
                "@baseType": "RelatedEntity",
                "role": "cart",
                "acmeField": 1,
            }
        ],
    }

    process = Process.from_dict(payload, strict=strict)

    related = process.relatedEntity[0]
    assert isinstance(related, tmforum.RelatedEntity)
    assert related.role == "cart"
    assert related.extra_attributes == {"acmeField": 1}
    assert warnings_of(parse_log) == []
    assert process.to_dict() == payload


def test_base_type_fallback_at_top_level(parse_log):
    payload = {"@type": "AcmeTask", "@baseType": "Task", "id": "t1", "acmeField": 1}

    task = Task.from_dict(payload, strict=True)

    assert isinstance(task, Task)
    assert warnings_of(parse_log) == []
    assert task.to_dict() == payload


def test_top_level_known_type_that_is_not_a_subclass_is_converted(parse_log):
    product = Product.from_dict({"@type": "ProductRef", "name": "Internet"})

    assert isinstance(product, Product)
    assert product.to_dict()["@type"] == "Product"
    assert warnings_of(parse_log) == []


def test_untyped_union_member_chosen_by_key_coverage():
    process = Process.from_dict(
        {
            "@type": "Process",
            "task": [{"id": "t1", "name": "n", "isMandatory": True, "priority": 2}],
        }
    )

    task = process.task[0]
    assert isinstance(task, Task)
    assert task.isMandatory is True
    assert task.priority == 2


def test_untyped_union_member_chosen_by_referred_type():
    report = IntentReport.from_dict(
        {"@type": "IntentReport", "intent": {"id": "1", "@referredType": "Intent"}}
    )

    assert isinstance(report.intent, IntentRef)
    assert report.intent._referred_type == "Intent"
    assert report.to_dict()["intent"]["@referredType"] == "Intent"


def test_untyped_union_tie_keeps_declared_order():
    report = IntentReport.from_dict(
        {"@type": "IntentReport", "intent": {"id": "1", "name": "EventLiveBroadcast"}}
    )

    assert isinstance(report.intent, Intent)


def test_untyped_union_falls_back_when_a_member_rejects_the_object(parse_log):
    item = ProductOrderItem.from_dict(
        {"@type": "ProductOrderItem", "product": {"id": "p", "isBundle": False}}
    )

    assert isinstance(item.product, ProductRef)
    assert item.product.extra_attributes == {"isBundle": False}
    assert warnings_of(parse_log) == []


@pytest.mark.parametrize(
    "cls, field_name, payload_value",
    [
        (ObjectCharacteristic, "value", {"@type": "ProductRef", "id": "p"}),
        (ProductOfferingPriceTable, "tableConfig", {"@type": "ProductRef", "id": "p"}),
        (ProductOfferingPriceTable, "tableData", [[{"@type": "ProductRef"}]]),
    ],
)
def test_free_form_values_are_left_untouched(cls, field_name, payload_value, parse_log):
    entity = cls.from_dict(
        {"@type": cls.__name__, field_name: payload_value}, strict=True
    )

    assert getattr(entity, field_name) == payload_value
    assert warnings_of(parse_log) == []


def test_unknown_enum_value_is_kept_as_a_string(parse_log):
    task = TaskSpecification.from_dict(
        {"@type": "TaskSpecification", "lifecycleStatus": "onDesign"}, strict=True
    )
    process = Process.from_dict({"@type": "Process", "state": "Completed"}, strict=True)

    assert task.lifecycleStatus == "onDesign"
    assert process.state == "Completed"
    assert warnings_of(parse_log) == []
    assert any("is not a value of" in r.getMessage() for r in parse_log.records)


def test_list_of_enums_is_converted():
    price = ProductOfferingPrice.from_dict(
        {"@type": "ProductOfferingPrice", "priceAlterationType": ["percentage"]}
    )

    assert price.priceAlterationType == [
        tmforum.ProductOfferingPriceAlterationTypeEnum("percentage")
    ]
    assert price.to_dict()["priceAlterationType"] == ["percentage"]


def test_null_list_takes_the_field_default():
    process = Process.from_dict({"@type": "Process", "task": None})
    spec = StringCharacteristicValueSpecification.from_dict(
        {"@type": "StringCharacteristicValueSpecification", "value": None}
    )

    assert process.task == []
    assert spec.value is None


def test_list_values_are_copied():
    payload = {"@type": "StringArrayCharacteristic", "value": ["a"]}

    characteristic = tmforum.StringArrayCharacteristic.from_dict(payload)

    assert characteristic.value == ["a"]
    assert characteristic.value is not payload["value"]


def test_schema_location_is_read_back():
    payload = {
        "@type": "TargetResourceSchema",
        "@schemaLocation": "https://host/schema.json",
    }

    schema = TargetResourceSchema.from_dict(payload, strict=True)

    assert schema._schema_location == "https://host/schema.json"
    assert schema.to_dict() == payload


def test_unknown_keys_are_preserved_and_never_override_fields():
    payload = {
        "@type": "Task",
        "id": "t1",
        "acmeField": {"nested": [1, 2]},
        "@acmeKey": "x",
    }

    task = Task.from_dict(payload, strict=True)

    assert task.extra_attributes == {"acmeField": {"nested": [1, 2]}, "@acmeKey": "x"}
    assert task.to_dict() == payload

    task.extra_attributes["id"] = "ignored"
    task.extra_attributes["added"] = 1
    result = task.to_dict()
    assert result["id"] == "t1"
    assert result["added"] == 1


def test_framework_keys_are_not_kept_as_unknown_keys():
    task = Task.from_dict({"@type": "Task", "@baseType": "Entity", "id": "t1"})

    assert task.extra_attributes == {}
    assert "@baseType" not in task.to_dict()


def test_extras_are_ignored_by_equality_and_replace():
    payload = {"@type": "Task", "id": "t1", "acmeField": 1}

    task = Task.from_dict(payload)

    assert task == Task(id="t1")
    assert dataclasses.replace(task).extra_attributes == {}
    assert json.loads(repr(task))["acmeField"] == 1


@pytest.mark.parametrize("data", [None, "x", [], 1])
@pytest.mark.parametrize("strict", [False, True])
def test_non_dict_payload_raises_type_error(data, strict):
    with pytest.raises(TypeError):
        Task.from_dict(data, strict=strict)


def test_entity_base_needs_a_resolvable_type():
    with pytest.raises(TypeError):
        Entity.from_dict({"@type": "NoSuchEntity"})

    assert isinstance(Entity.from_dict({"@type": "TaskRef"}), TaskRef)


@pytest.mark.parametrize("strict", [False, True])
def test_top_level_validator_still_raises(strict):
    with pytest.raises(ValueError) as error:
        Product.from_dict({"@type": "Product", "id": "p"}, strict=strict)

    assert not isinstance(error.value, FromDictError)


def test_list_check_applies_again_after_a_failed_parse():
    with pytest.raises(ValueError):
        Product.from_dict({"@type": "Product", "id": "p"})

    with pytest.raises(ValueError):
        Task(taskCharacteristic=tmforum.FlowCharacteristic(modality="input"))


def test_every_entity_field_is_classified():
    kinds = set()
    for obj in vars(tmforum).values():
        if isinstance(obj, type) and dataclasses.is_dataclass(obj):
            for plan in tmforum._class_plan(obj).fields:
                kinds.add(plan.kind)
                if plan.kind in ("entity", "enum"):
                    assert plan.members, f"{obj.__name__}.{plan.name}"

    assert kinds == {"any", "dict", "entity", "enum", "scalar"}


@pytest.mark.parametrize("body", [{"code": "404", "reason": "Not Found"}, [], None])
def test_from_id_returns_none_without_an_entity(backend, context, body):
    backend.body = body

    assert Task.from_id("t1", context) is None


def test_read_and_update_keep_the_entity_on_an_error_body(backend, context):
    backend.body = {"code": "404", "reason": "Not Found"}
    task = Task(id="t1", name="local")

    assert task.read(context) is task
    assert task.update({"name": "x"}, context) is task


def test_create_returns_the_raw_body_when_it_carries_no_entity(backend, context):
    backend.body = {"code": "422", "reason": "Unprocessable"}

    assert Task(name="new").create(context) == backend.body


def test_query_get_returns_a_non_list_response_unchanged(backend, context):
    backend.body = {"code": "404", "reason": "Not Found"}

    assert Task.query_get("", context) == backend.body


def test_query_get_keeps_an_unparsable_item_in_place(backend, context):
    backend.body = [
        {"@type": "Product", "id": "p1"},
        {"@type": "Product", "name": "ok"},
    ]

    items = Product.query_get("", context)

    assert items[0] == backend.body[0]
    assert isinstance(items[1], Product)

    context.strict_parsing = True
    with pytest.raises(ValueError):
        Product.query_get("", context)


def test_check_availability_returns_a_non_list_response_unchanged(backend, context):
    backend.body = {"code": "500"}

    assert tmforum.ResourcePool(id="rp1").check_availability(context) == backend.body


def test_intent_reports_use_the_context_strict_flag(backend, context):
    backend.body = [{"@type": "IntentReport", "id": "r1", "intent": {"@type": "Acme"}}]

    reports = Intent(id="i1").get_intent_reports(context)
    assert reports[0].intent == {"@type": "Acme"}

    context.strict_parsing = True
    with pytest.raises(FromDictError):
        Intent(id="i1").get_intent_reports(context)
