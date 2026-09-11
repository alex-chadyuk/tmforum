import json
from types import SimpleNamespace

import pytest
import requests
from tmforum import (
    AttachmentRef,
    BooleanCharacteristic,
    CharacteristicSpecification,
    CharacteristicSpecificationRelationship,
    CharacteristicValueSpecification,
    ConstraintRef,
    Context,
    EntityRef,
    EntityRelationship,
    EntitySpecificationRelationship,
    AssociationSpecificationRef,
    ExpressionSpecification,
    Intent,
    IntentExpression,
    IntentRef,
    IntentReport,
    IntentSpecification,
    IntentSpecificationRef,
    IntentSpecificationRelationship,
    JsonLdExpression,
    PartyRef,
    PartyRoleRef,
    ProbeIntent,
    RelatedPartyRefOrPartyRoleRef,
    TargetEntitySchema,
    TimePeriod,
    TurtleExpression,
)


@pytest.fixture
def json_ld_value():
    return {
        "@context": {
            "icm": "http://www.models.tmforum.org/tio/v1.0.0/IntentCommonModel#",
            "idan": "http://www.idan-tmforum-catalyst.org/IntentDrivenAutonomousNetworks#",
        },
        "idan:EventLiveBroadcast000001": {
            "@type": "icm:Intent",
            "icm:intentOwner": "idan:Salesforce",
            "icm:hasExpectation": {
                "idan:Delivery_service": {
                    "@type": "icm:DeliveryExpectation",
                    "icm:target": "_:service",
                    "icm:params": {"icm:targetDescription": "cat:EventWirelessAccess"},
                }
            },
        },
    }


@pytest.fixture
def intent_dict(json_ld_value):
    return {
        "@type": "Intent",
        "id": "20011",
        "href": "https://mycsp.com:8080/tmf-api/intentManagement/v5/intent/20011",
        "name": "EventLiveBroadcast",
        "description": "Intent for ordering live broadcast service for an event",
        "version": "1.0",
        "priority": "1",
        "context": "Autonomous services",
        "isBundle": False,
        "lifecycleStatus": "Created",
        "creationDate": "2023-10-23T00:30:00.00Z",
        "lastUpdate": "2023-10-23T00:30:00.00Z",
        "statusChangeDate": "2023-10-23T00:30:00.00Z",
        "validFor": {
            "startDateTime": "2023-10-23T00:30:00.00Z",
            "endDateTime": "2024-10-19T23:30:00.00Z",
        },
        "intentSpecification": {
            "@type": "IntentSpecificationRef",
            "id": "EventLiveBroadcast_IntentSpec",
            "name": "EventLiveBroadcastIntentSpec",
            "@referredType": "IntentSpecification",
        },
        "intentRelationship": [
            {
                "@type": "EntityRelationship",
                "id": "20010",
                "href": "https://mycsp.com:8080/tmf-api/intentManagement/v5/intent/20010",
                "@referredType": "Intent",
                "relationshipType": "dependency",
                "role": "prerequisite",
                "associationSpec": {
                    "@type": "EntityRef",
                    "id": "as-1",
                    "@referredType": "AssociationSpecification",
                },
            }
        ],
        "characteristic": [
            {
                "@type": "BooleanCharacteristic",
                "id": "19997-pn",
                "name": "isTimeConstrained",
                "value": True,
                "valueType": "boolean",
            }
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "role": "user",
                "partyOrPartyRole": {
                    "@type": "PartyRef",
                    "id": "19993",
                    "href": "https://mycsp.com:8080/tmf-api/partyManagement/v5/individual/456",
                    "name": "Marcus Aurelius",
                    "@referredType": "Individual",
                },
            }
        ],
        "attachment": [
            {
                "@type": "AttachmentRef",
                "id": "att-1",
                "url": "https://mycsp.com:8080/docs/broadcast.pdf",
                "@referredType": "Attachment",
            }
        ],
        "expression": {
            "@type": "JsonLdExpression",
            "iri": "https://mycsp.com:8080/tmf-api/rdfs/expression-example-1",
            "expressionValue": json_ld_value,
        },
    }


@pytest.fixture
def intent_1(intent_dict):
    return Intent.from_dict(intent_dict)


@pytest.fixture
def intent_report_dict():
    return {
        "@type": "IntentReport",
        "id": "20021",
        "href": "https://mycsp.com:8080/tmf-api/intentManagement/v5/intent/20011/intentReport/20021",
        "name": "MyIntent Report",
        "description": "An Intent report example",
        "creationDate": "2023-10-23T00:30:01.00Z",
        "validFor": {"startDateTime": "2023-10-23T00:30:01.00Z"},
        "expression": {
            "@type": "JsonLdExpression",
            "iri": "https://mycsp.com:8080/tmf-api/rdfs/expression-intentReport-1",
            "expressionValue": {
                "@context": {
                    "icm": "http://tio.models.tmforum.org/tio/v3.4.0/IntentCommonModel/"
                },
                "@graph": [
                    {
                        "@id": "_:k3",
                        "icm:target": {"@type": "Intent", "@value": "20011"},
                    }
                ],
            },
        },
        "intent": {
            "@type": "IntentRef",
            "id": "20011",
            "href": "https://mycsp.com:8080/tmf-api/intentManagement/v5/intent/20011",
            "@referredType": "Intent",
        },
    }


@pytest.fixture
def intent_specification_dict():
    return {
        "@type": "IntentSpecification",
        "@baseType": "EntitySpecification",
        "id": "65537",
        "href": "https://mycsp.com:8080/tmf-api/intentManagement/v5/intentSpecification/65537",
        "name": "EventLiveBroadcastSpec",
        "description": "Intent spec for ordering live broadcast service for an event",
        "version": "1.0",
        "isBundle": False,
        "lifecycleStatus": "ACTIVE",
        "lastUpdate": "2023-08-08T08:34:16.785Z",
        "validFor": {
            "startDateTime": "2023-04-12T23:20:50.52Z",
            "endDateTime": "2099-04-12T23:20:50.52Z",
        },
        "expressionSpecification": {
            "@type": "ExpressionSpecification",
            "expressionLanguage": "JSON-LD",
            "iri": "http://tio.models.tmforum.org/tio/v3.4.0/IntentManagmentOntology/",
        },
        "targetEntitySchema": {
            "@type": "TargetEntitySchema",
            "@schemaLocation": "https://mycsp.com:8080/tmf-api/schema/Intent.schema.json",
        },
        "specCharacteristic": [
            {
                "@type": "CharacteristicSpecification",
                "id": "cs-1",
                "name": "isTimeConstrained",
                "valueType": "boolean",
                "minCardinality": 0,
                "maxCardinality": 1,
                "charSpecRelationship": [
                    {
                        "@type": "CharacteristicSpecificationRelationship",
                        "relationshipType": "dependency",
                        "name": "eventWindow",
                        "parentSpecificationId": "65536",
                    }
                ],
                "characteristicValueSpecification": [
                    {
                        "@type": "CharacteristicValueSpecification",
                        "valueType": "boolean",
                        "isDefault": True,
                    }
                ],
            }
        ],
        "intentSpecRelationship": [
            {
                "@type": "IntentSpecificationRelationship",
                "id": "65536",
                "name": "BaseBroadcastSpec",
                "relationshipType": "substitution",
                "role": "replaces",
                "validFor": {"startDateTime": "2023-04-12T23:20:50.52Z"},
            }
        ],
        "entitySpecRelationship": [
            {
                "@type": "EntitySpecificationRelationship",
                "relationshipType": "dependency",
                "role": "requires",
                "associationSpec": {
                    "@type": "AssociationSpecificationRef",
                    "id": "as-2",
                    "@referredType": "AssociationSpecification",
                },
            }
        ],
        "constraint": [
            {
                "@type": "ConstraintRef",
                "id": "c-1",
                "version": "2",
                "@referredType": "Constraint",
            }
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "role": "Provider",
                "partyOrPartyRole": {
                    "@type": "PartyRoleRef",
                    "id": "28657",
                    "name": "TechSolutionsPro Ltd",
                    "@referredType": "Partner",
                },
            }
        ],
        "attachment": [
            {
                "@type": "AttachmentRef",
                "id": "att-2",
                "@referredType": "Attachment",
            }
        ],
    }


@pytest.fixture
def backend(monkeypatch):
    """Replaces requests.request with a stub that records calls and returns `body`."""
    stub = SimpleNamespace(calls=[], body=None)

    def request(method, url, headers=None, data=None):
        stub.calls.append((method, url))
        text = json.dumps(stub.body) if stub.body is not None else ""
        return SimpleNamespace(status_code=200, headers={}, text=text)

    monkeypatch.setattr(requests, "request", request)
    return stub


@pytest.fixture
def context():
    return Context(api_base_url="https://host:port/tmf-api", headers={})


def test_intent_instantiates_with_id(intent_1):
    assert isinstance(intent_1, Intent)
    assert intent_1.id == "20011"
    assert intent_1.name == "EventLiveBroadcast"
    assert intent_1.version == "1.0"
    assert intent_1.priority == "1"
    assert intent_1.context == "Autonomous services"
    assert intent_1.isBundle is False
    assert intent_1.lifecycleStatus == "Created"
    assert intent_1.statusChangeDate == "2023-10-23T00:30:00.00Z"


def test_intent_instantiates_classes(intent_1):
    assert isinstance(intent_1.validFor, TimePeriod)

    assert isinstance(intent_1.intentSpecification, IntentSpecificationRef)
    assert intent_1.intentSpecification._referred_type == "IntentSpecification"

    relationship = intent_1.intentRelationship[0]
    assert isinstance(relationship, EntityRelationship)
    assert relationship.relationshipType == "dependency"
    assert relationship._referred_type == "Intent"
    assert isinstance(relationship.associationSpec, EntityRef)

    characteristic = intent_1.characteristic[0]
    assert isinstance(characteristic, BooleanCharacteristic)
    assert characteristic.value is True

    related_party = intent_1.relatedParty[0]
    assert isinstance(related_party, RelatedPartyRefOrPartyRoleRef)
    assert isinstance(related_party.partyOrPartyRole, PartyRef)
    assert related_party.partyOrPartyRole._referred_type == "Individual"

    assert isinstance(intent_1.attachment[0], AttachmentRef)

    assert isinstance(intent_1.expression, JsonLdExpression)
    assert isinstance(intent_1.expression, IntentExpression)
    assert intent_1.expression.iri.endswith("expression-example-1")


def test_json_ld_expression_value_passes_through(intent_1, json_ld_value):
    assert intent_1.expression.expressionValue == json_ld_value


def test_json_ld_type_keyword_is_not_resolved_to_sdk_class():
    expression = JsonLdExpression.from_dict(
        {
            "@type": "JsonLdExpression",
            "expressionValue": {"@type": "Intent", "@id": "_:k0"},
        }
    )

    assert expression.expressionValue == {"@type": "Intent", "@id": "_:k0"}


def test_turtle_expression():
    intent = Intent.from_dict(
        {
            "@type": "Intent",
            "id": "20012",
            "expression": {
                "@type": "TurtleExpression",
                "iri": "https://mycsp.com:8080/tmf-api/rdfs/expression-example-2",
                "expressionValue": "@prefix icm: <http://tio.models.tmforum.org/> .",
            },
        }
    )

    assert isinstance(intent.expression, TurtleExpression)
    assert intent.expression.expressionValue.startswith("@prefix icm:")

    result = intent.to_dict()["expression"]
    assert result["@type"] == "TurtleExpression"
    assert result["@baseType"] == "IntentExpression"


def test_probe_intent_resolves_by_type(intent_dict, context):
    probe = Intent.from_dict({**intent_dict, "@type": "ProbeIntent"})

    assert isinstance(probe, ProbeIntent)
    assert isinstance(probe.expression, JsonLdExpression)

    result = probe.to_dict()
    assert result["@type"] == "ProbeIntent"
    assert result["@baseType"] == "Intent"
    assert ProbeIntent.get_resource_path(context) == Intent.get_resource_path(context)


def test_intent_defaults_to_empty_lists():
    intent = Intent.from_dict({"@type": "Intent", "id": "20011"})

    assert intent.expression is None
    assert intent.intentSpecification is None
    assert intent.intentRelationship == []
    assert intent.characteristic == []
    assert intent.relatedParty == []
    assert intent.attachment == []


def test_intent_rejects_non_list_characteristic():
    with pytest.raises(ValueError):
        Intent(characteristic=BooleanCharacteristic(name="isTimeConstrained"))


def test_intent_to_dict_round_trip(intent_dict):
    result = Intent.from_dict(intent_dict).to_dict()

    assert result["@type"] == "Intent"
    assert "@baseType" not in result
    assert result["id"] == "20011"
    assert result["context"] == "Autonomous services"
    assert result["isBundle"] is False
    assert result["validFor"]["endDateTime"] == "2024-10-19T23:30:00.00Z"
    assert result["intentSpecification"]["@type"] == "IntentSpecificationRef"
    assert result["intentSpecification"]["@referredType"] == "IntentSpecification"
    assert result["intentRelationship"][0]["@type"] == "EntityRelationship"
    assert result["intentRelationship"][0]["@referredType"] == "Intent"
    assert result["characteristic"][0]["@type"] == "BooleanCharacteristic"
    assert result["characteristic"][0]["@baseType"] == "Characteristic"
    assert result["relatedParty"][0]["partyOrPartyRole"]["@type"] == "PartyRef"
    assert result["attachment"][0]["@type"] == "AttachmentRef"
    assert result["expression"]["@type"] == "JsonLdExpression"
    assert result["expression"]["@baseType"] == "IntentExpression"
    assert (
        result["expression"]["expressionValue"]
        == intent_dict["expression"]["expressionValue"]
    )


def test_intent_report_instantiates_classes(intent_report_dict):
    report = IntentReport.from_dict(intent_report_dict)

    assert report.id == "20021"
    assert report.creationDate == "2023-10-23T00:30:01.00Z"
    assert isinstance(report.validFor, TimePeriod)
    assert isinstance(report.expression, JsonLdExpression)
    assert report.expression.expressionValue["@graph"][0]["icm:target"] == {
        "@type": "Intent",
        "@value": "20011",
    }
    assert isinstance(report.intent, IntentRef)
    assert report.intent._referred_type == "Intent"


def test_intent_report_carries_intent_by_value(intent_report_dict, intent_dict):
    report = IntentReport.from_dict(
        {**intent_report_dict, "intent": {**intent_dict, "@type": "ProbeIntent"}}
    )

    assert isinstance(report.intent, ProbeIntent)
    assert isinstance(report.intent.characteristic[0], BooleanCharacteristic)


def test_intent_report_untyped_intent_parses_as_first_union_member(
    intent_report_dict,
):
    report = IntentReport.from_dict(
        {**intent_report_dict, "intent": {"id": "20011", "name": "EventLiveBroadcast"}}
    )

    assert isinstance(report.intent, Intent)
    assert report.intent.id == "20011"


def test_intent_report_to_dict_round_trip(intent_report_dict):
    result = IntentReport.from_dict(intent_report_dict).to_dict()

    assert result["@type"] == "IntentReport"
    assert "@baseType" not in result
    assert result["name"] == "MyIntent Report"
    assert result["intent"]["@type"] == "IntentRef"
    assert result["intent"]["@referredType"] == "Intent"
    assert result["expression"]["@type"] == "JsonLdExpression"
    assert (
        result["expression"]["expressionValue"]
        == intent_report_dict["expression"]["expressionValue"]
    )


def test_intent_specification_instantiates_classes(intent_specification_dict):
    spec = IntentSpecification.from_dict(intent_specification_dict)

    assert spec.id == "65537"
    assert spec.lifecycleStatus == "ACTIVE"
    assert isinstance(spec.validFor, TimePeriod)

    assert isinstance(spec.expressionSpecification, ExpressionSpecification)
    assert spec.expressionSpecification.expressionLanguage == "JSON-LD"

    assert isinstance(spec.targetEntitySchema, TargetEntitySchema)

    char_spec = spec.specCharacteristic[0]
    assert isinstance(char_spec, CharacteristicSpecification)
    assert char_spec.maxCardinality == 1
    assert isinstance(
        char_spec.charSpecRelationship[0], CharacteristicSpecificationRelationship
    )
    assert isinstance(
        char_spec.characteristicValueSpecification[0], CharacteristicValueSpecification
    )

    intent_spec_relationship = spec.intentSpecRelationship[0]
    assert isinstance(intent_spec_relationship, IntentSpecificationRelationship)
    assert intent_spec_relationship.relationshipType == "substitution"
    assert intent_spec_relationship._referred_type == "IntentSpecification"
    assert isinstance(intent_spec_relationship.validFor, TimePeriod)

    entity_spec_relationship = spec.entitySpecRelationship[0]
    assert isinstance(entity_spec_relationship, EntitySpecificationRelationship)
    assert isinstance(
        entity_spec_relationship.associationSpec, AssociationSpecificationRef
    )

    assert isinstance(spec.constraint[0], ConstraintRef)
    assert spec.constraint[0].version == "2"
    assert isinstance(spec.relatedParty[0].partyOrPartyRole, PartyRoleRef)
    assert isinstance(spec.attachment[0], AttachmentRef)


def test_intent_specification_defaults_to_empty_lists():
    spec = IntentSpecification.from_dict({"@type": "IntentSpecification", "id": "1"})

    assert spec.expressionSpecification is None
    assert spec.specCharacteristic == []
    assert spec.intentSpecRelationship == []
    assert spec.entitySpecRelationship == []
    assert spec.constraint == []
    assert spec.relatedParty == []
    assert spec.attachment == []


def test_intent_specification_rejects_non_list_relationship():
    with pytest.raises(ValueError):
        IntentSpecification(
            intentSpecRelationship=IntentSpecificationRelationship(id="65536")
        )


def test_intent_specification_relationship_defaults_referred_type():
    result = IntentSpecificationRelationship(id="65536").to_dict()

    assert result["@type"] == "IntentSpecificationRelationship"
    assert "@baseType" not in result
    assert result["@referredType"] == "IntentSpecification"


def test_intent_specification_to_dict_round_trip(intent_specification_dict):
    result = IntentSpecification.from_dict(intent_specification_dict).to_dict()

    assert result["@type"] == "IntentSpecification"
    assert "@baseType" not in result
    assert result["expressionSpecification"]["@type"] == "ExpressionSpecification"
    assert result["expressionSpecification"]["iri"].endswith("IntentManagmentOntology/")
    assert result["targetEntitySchema"]["@type"] == "TargetEntitySchema"
    assert result["specCharacteristic"][0]["@type"] == "CharacteristicSpecification"
    assert (
        result["specCharacteristic"][0]["charSpecRelationship"][0]["@type"]
        == "CharacteristicSpecificationRelationship"
    )
    assert (
        result["intentSpecRelationship"][0]["@type"]
        == "IntentSpecificationRelationship"
    )
    assert result["intentSpecRelationship"][0]["@referredType"] == "IntentSpecification"
    assert (
        result["entitySpecRelationship"][0]["associationSpec"]["@referredType"]
        == "AssociationSpecification"
    )
    assert result["constraint"][0]["@referredType"] == "Constraint"
    assert result["relatedParty"][0]["partyOrPartyRole"]["@type"] == "PartyRoleRef"


def test_intent_management_resource_paths(context):
    base = "https://host:port/tmf-api/intentManagement/v5"

    assert Intent.get_resource_path(context) == f"{base}/intent"
    assert (
        IntentSpecification.get_resource_path(context) == f"{base}/intentSpecification"
    )


def test_intent_get_intent_reports(backend, context, intent_report_dict):
    backend.body = [intent_report_dict, {**intent_report_dict, "id": "20022"}]

    reports = Intent(id="20011").get_intent_reports(context, query="fields=name")

    assert backend.calls == [
        (
            "GET",
            "https://host:port/tmf-api/intentManagement/v5/intent/20011/intentReport"
            "?fields=name",
        )
    ]
    assert [r.id for r in reports] == ["20021", "20022"]
    assert all(isinstance(r, IntentReport) for r in reports)


def test_intent_get_intent_report(backend, context, intent_report_dict):
    backend.body = intent_report_dict

    report = ProbeIntent(id="20011").get_intent_report("20021", context)

    assert backend.calls == [
        (
            "GET",
            "https://host:port/tmf-api/intentManagement/v5/intent/20011/intentReport"
            "/20021",
        )
    ]
    assert isinstance(report, IntentReport)
    assert isinstance(report.intent, IntentRef)


def test_intent_get_intent_report_not_found(backend, context):
    backend.body = {"code": "404", "reason": "Not Found"}

    assert Intent(id="20011").get_intent_report("missing", context) is None


def test_intent_delete_intent_report(backend, context):
    Intent(id="20011").delete_intent_report("20021", context)

    assert backend.calls == [
        (
            "DELETE",
            "https://host:port/tmf-api/intentManagement/v5/intent/20011/intentReport"
            "/20021",
        )
    ]


def test_intent_report_helpers_require_intent_id(backend, context):
    intent = Intent(name="not created yet")

    assert intent.get_intent_reports(context) == []
    assert intent.get_intent_report("20021", context) is None
    assert intent.delete_intent_report("20021", context) is None
    assert backend.calls == []
