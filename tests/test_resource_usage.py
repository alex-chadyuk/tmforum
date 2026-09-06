import pytest
from tmforum import (
    AttachmentRefOrValue,
    Characteristic,
    CharacteristicSpecification,
    Context,
    ExternalIdentifier,
    PartyRoleRef,
    RelatedPartyRefOrPartyRoleRef,
    ResourceRef,
    ResourceSpecificationRef,
    ResourceUsage,
    ResourceUsageRef,
    ResourceUsageSpecRelationship,
    ResourceUsageSpecification,
    ResourceUsageSpecificationRef,
    StringCharacteristic,
    TimePeriod,
)


@pytest.fixture
def resource_usage_dict():
    return {
        "@type": "ResourceUsage",
        "@baseType": "Entity",
        "id": "ru-4412",
        "href": (
            "https://mycsp.com/tmf-api/resourceUsageManagement/v5"
            "/resourceUsage/ru-4412"
        ),
        "usageDate": "2026-05-14T09:13:16.000Z",
        "description": "Voicemail Retrieval",
        "usageType": "voicemailAccess",
        "isBundle": False,
        "usageCharacteristic": [
            {
                "@type": "StringCharacteristic",
                "id": "uc-1",
                "name": "originatingNumber",
                "valueType": "string",
                "value": "+441234567890",
            },
            {
                "@type": "Characteristic",
                "id": "uc-2",
                "name": "duration",
                "valueType": "integer",
                "characteristicRelationship": [
                    {
                        "@type": "CharacteristicRelationship",
                        "id": "uc-1",
                        "relationshipType": "dependency",
                    }
                ],
            },
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "role": "usageOwner",
                "partyOrPartyRole": {
                    "@type": "PartyRoleRef",
                    "@referredType": "PartyRole",
                    "id": "pr-07",
                    "name": "Network Operations",
                    "partyId": "party-07",
                    "partyName": "ACME Networks",
                },
            }
        ],
        "resource": {
            "@type": "ResourceRef",
            "@referredType": "Resource",
            "id": "res-900",
            "href": "https://mycsp.com/tmf-api/resourceInventory/v5/resource/res-900",
            "name": "Voicemail platform",
        },
        "usageSpecification": {
            "@type": "ResourceUsageSpecificationRef",
            "@referredType": "ResourceUsageSpecification",
            "id": "rus-8801",
            "name": "Voicemail usage",
        },
        "bundledResourceUsage": [
            {
                "@type": "ResourceUsageRef",
                "@referredType": "ResourceUsage",
                "id": "ru-4413",
                "name": "Voicemail leg",
            }
        ],
        "externalIdentifier": [
            {
                "@type": "ExternalIdentifier",
                "owner": "MediationPlatform",
                "externalIdentifierType": "CDR",
                "id": "cdr-99182",
            }
        ],
    }


@pytest.fixture
def resource_usage_1(resource_usage_dict):
    return ResourceUsage.from_dict(resource_usage_dict)


@pytest.fixture
def resource_usage_specification_dict():
    return {
        "@type": "ResourceUsageSpecification",
        "@baseType": "Entity",
        "id": "rus-8801",
        "href": (
            "https://mycsp.com/tmf-api/resourceUsageManagement/v5"
            "/resourceUsageSpecification/rus-8801"
        ),
        "name": "Voicemail usage",
        "description": "Metered voicemail platform usage",
        "isBundle": False,
        "lastUpdate": "2026-05-14T08:30:00.000Z",
        "lifecycleStatus": "active",
        "version": "2.1",
        "resourceSpecification": [
            {
                "@type": "ResourceSpecificationRef",
                "@referredType": "ResourceSpecification",
                "id": "rs-101",
                "href": (
                    "https://mycsp.com/tmf-api/resourceCatalog/v5"
                    "/resourceSpecification/rs-101"
                ),
                "name": "Voicemail platform",
                "version": "1.4",
            }
        ],
        "specCharacteristic": [
            {
                "@type": "CharacteristicSpecification",
                "id": "spec-char-1",
                "name": "durationUnit",
                "valueType": "string",
                "description": "Unit the metered duration is expressed in",
                "minCardinality": 1,
                "maxCardinality": 1,
                "validFor": {
                    "startDateTime": "2026-01-01T00:00:00.000Z",
                    "endDateTime": "2027-01-01T00:00:00.000Z",
                },
            }
        ],
        "attachment": [
            {
                "@type": "AttachmentRefOrValue",
                "id": "att-9",
                "name": "Usage metering guide",
                "mimeType": "application/pdf",
                "url": "https://mycsp.com/docs/usage-metering.pdf",
                "isRef": False,
            }
        ],
        "bundledResourceUsageSpecification": [
            {
                "@type": "ResourceUsageSpecificationRef",
                "@referredType": "ResourceUsageSpecification",
                "id": "rus-8802",
                "name": "Voicemail storage usage",
            }
        ],
        "resourceUsageSpecRelationship": [
            {
                "@type": "ResourceUsageSpecRelationship",
                "id": "rus-8803",
                "name": "Legacy voicemail usage",
                "relationshipType": "substitution",
                "role": "predecessor",
                "validFor": {
                    "startDateTime": "2026-01-01T00:00:00.000Z",
                },
            }
        ],
        "validFor": {
            "startDateTime": "2026-01-01T00:00:00.000Z",
            "endDateTime": "2027-01-01T00:00:00.000Z",
        },
    }


@pytest.fixture
def resource_usage_specification_1(resource_usage_specification_dict):
    return ResourceUsageSpecification.from_dict(resource_usage_specification_dict)


def test_resource_usage_instantiates_with_id(resource_usage_dict):
    ru = ResourceUsage.from_dict(resource_usage_dict)

    assert ru.id == "ru-4412"
    assert ru.description == "Voicemail Retrieval"
    assert ru.usageType == "voicemailAccess"
    assert ru.usageDate == "2026-05-14T09:13:16.000Z"
    assert ru.isBundle is False
    assert ru.href.endswith("/resourceUsage/ru-4412")


def test_resource_usage_instantiates_classes(resource_usage_1):
    ru = resource_usage_1

    assert isinstance(ru, ResourceUsage)

    assert isinstance(ru.usageCharacteristic[0], StringCharacteristic)
    assert ru.usageCharacteristic[0].value == "+441234567890"
    assert isinstance(ru.usageCharacteristic[1], Characteristic)
    assert ru.usageCharacteristic[1].characteristicRelationship[0].id == "uc-1"

    assert isinstance(ru.relatedParty[0], RelatedPartyRefOrPartyRoleRef)
    assert isinstance(ru.relatedParty[0].partyOrPartyRole, PartyRoleRef)
    assert ru.relatedParty[0].partyOrPartyRole.partyId == "party-07"

    assert isinstance(ru.resource, ResourceRef)
    assert ru.resource._referred_type == "Resource"

    assert isinstance(ru.usageSpecification, ResourceUsageSpecificationRef)
    assert ru.usageSpecification.id == "rus-8801"

    assert isinstance(ru.bundledResourceUsage[0], ResourceUsageRef)
    assert ru.bundledResourceUsage[0]._referred_type == "ResourceUsage"

    assert isinstance(ru.externalIdentifier[0], ExternalIdentifier)
    assert ru.externalIdentifier[0].owner == "MediationPlatform"


def test_resource_usage_defaults_to_empty_lists():
    ru = ResourceUsage.from_dict(
        {"@type": "ResourceUsage", "id": "ru-1", "usageType": "dataSession"}
    )

    assert ru.usageCharacteristic == []
    assert ru.relatedParty == []
    assert ru.bundledResourceUsage == []
    assert ru.externalIdentifier == []
    assert ru.resource is None
    assert ru.usageSpecification is None


def test_resource_usage_resource_path():
    context = Context(api_base_url="https://mycsp.com:8080/tmf-api")

    assert ResourceUsage.get_resource_path(context) == (
        "https://mycsp.com:8080/tmf-api/resourceUsageManagement/v5/resourceUsage"
    )


def test_resource_usage_to_dict_round_trip(resource_usage_dict):
    result = ResourceUsage.from_dict(resource_usage_dict).to_dict()

    assert result["@type"] == "ResourceUsage"
    assert "@baseType" not in result
    assert result["usageCharacteristic"][0]["@type"] == "StringCharacteristic"
    assert result["resource"]["@referredType"] == "Resource"
    assert result["usageSpecification"]["@referredType"] == "ResourceUsageSpecification"
    assert result["bundledResourceUsage"][0]["@referredType"] == "ResourceUsage"
    assert result["externalIdentifier"][0]["owner"] == "MediationPlatform"


def test_resource_usage_specification_instantiates_with_id(
    resource_usage_specification_dict,
):
    rus = ResourceUsageSpecification.from_dict(resource_usage_specification_dict)

    assert rus.id == "rus-8801"
    assert rus.name == "Voicemail usage"
    assert rus.version == "2.1"
    assert rus.lifecycleStatus == "active"
    assert rus.lastUpdate == "2026-05-14T08:30:00.000Z"
    assert rus.href.endswith("/resourceUsageSpecification/rus-8801")


def test_resource_usage_specification_instantiates_classes(
    resource_usage_specification_1,
):
    rus = resource_usage_specification_1

    assert isinstance(rus, ResourceUsageSpecification)

    assert isinstance(rus.resourceSpecification[0], ResourceSpecificationRef)
    assert rus.resourceSpecification[0].version == "1.4"
    assert rus.resourceSpecification[0]._referred_type == "ResourceSpecification"

    assert isinstance(rus.specCharacteristic[0], CharacteristicSpecification)
    assert rus.specCharacteristic[0].name == "durationUnit"
    assert isinstance(rus.specCharacteristic[0].validFor, TimePeriod)

    assert isinstance(rus.attachment[0], AttachmentRefOrValue)
    assert rus.attachment[0].isRef is False

    assert isinstance(
        rus.bundledResourceUsageSpecification[0], ResourceUsageSpecificationRef
    )
    assert rus.bundledResourceUsageSpecification[0].id == "rus-8802"

    assert isinstance(
        rus.resourceUsageSpecRelationship[0], ResourceUsageSpecRelationship
    )
    assert rus.resourceUsageSpecRelationship[0].relationshipType == "substitution"
    assert rus.resourceUsageSpecRelationship[0].role == "predecessor"
    assert isinstance(rus.resourceUsageSpecRelationship[0].validFor, TimePeriod)

    assert isinstance(rus.validFor, TimePeriod)
    assert rus.validFor.endDateTime == "2027-01-01T00:00:00.000Z"


def test_resource_usage_specification_defaults_to_empty_lists():
    rus = ResourceUsageSpecification.from_dict(
        {
            "@type": "ResourceUsageSpecification",
            "id": "rus-1",
            "name": "Data session usage",
        }
    )

    assert rus.resourceSpecification == []
    assert rus.specCharacteristic == []
    assert rus.attachment == []
    assert rus.bundledResourceUsageSpecification == []
    assert rus.resourceUsageSpecRelationship == []
    assert rus.lifecycleStatus is None
    assert rus.validFor is None


def test_resource_usage_specification_resource_path():
    context = Context(api_base_url="https://mycsp.com:8080/tmf-api")

    assert ResourceUsageSpecification.get_resource_path(context) == (
        "https://mycsp.com:8080/tmf-api/resourceUsageManagement/v5"
        "/resourceUsageSpecification"
    )


def test_resource_usage_specification_to_dict_round_trip(
    resource_usage_specification_dict,
):
    result = ResourceUsageSpecification.from_dict(
        resource_usage_specification_dict
    ).to_dict()

    assert result["@type"] == "ResourceUsageSpecification"
    assert "@baseType" not in result
    assert result["lifecycleStatus"] == "active"
    assert (
        result["resourceSpecification"][0]["@referredType"] == "ResourceSpecification"
    )
    assert (
        result["bundledResourceUsageSpecification"][0]["@referredType"]
        == "ResourceUsageSpecification"
    )
    assert (
        result["resourceUsageSpecRelationship"][0]["@type"]
        == "ResourceUsageSpecRelationship"
    )
    assert result["validFor"]["endDateTime"] == "2027-01-01T00:00:00.000Z"


def test_resource_usage_ref_from_entity(resource_usage_1):
    ref = ResourceUsageRef.from_entity(resource_usage_1)

    assert isinstance(ref, ResourceUsageRef)
    assert ref.id == "ru-4412"
    assert ref._referred_type == "ResourceUsage"
