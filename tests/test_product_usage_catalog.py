import pytest
from tmforum import (
    AttachmentRefOrValue,
    CharacteristicSpecification,
    Context,
    ProductSpecificationRef,
    ProductUsageSpecification,
    ProductUsageSpecificationLifecycleStatusType,
    ServiceUsageSpecificationRef,
    StringCharacteristicValueSpecification,
    TargetProductSchema,
    TargetProductUsageSchema,
    TimePeriod,
)


@pytest.fixture
def product_usage_specification_dict():
    return {
        "@type": "ProductUsageSpecification",
        "@baseType": "Entity",
        "id": "pus-8801",
        "href": (
            "https://mycsp.com/tmf-api/productUsageCatalogManagement/v5"
            "/productUsageSpecification/pus-8801"
        ),
        "name": "Mobile data usage",
        "description": "Metered mobile data consumption used to rate broadband products",
        "lastUpdate": "2026-05-14T08:30:00.000Z",
        "lifecycleStatus": "active",
        "version": "2.1",
        "productSpecification": [
            {
                "@type": "ProductSpecificationRef",
                "id": "ps-101",
                "href": (
                    "https://mycsp.com/tmf-api/productCatalogManagement/v5"
                    "/productSpecification/ps-101"
                ),
                "name": "Mobile broadband",
                "version": "1.4",
                "@referredType": "ProductSpecification",
                "targetProductSchema": {
                    "@type": "TargetProductSchema",
                    "id": "tps-1",
                },
            }
        ],
        "serviceUsageSpecification": [
            {
                "@type": "ServiceUsageSpecificationRef",
                "id": "sus-55",
                "href": (
                    "https://mycsp.com/tmf-api/usageManagement/v5"
                    "/usageSpecification/sus-55"
                ),
                "name": "Data session record",
                "@referredType": "ServiceUsageSpecification",
            }
        ],
        "specCharacteristic": [
            {
                "@type": "CharacteristicSpecification",
                "id": "spec-char-1",
                "name": "volumeUnit",
                "valueType": "string",
                "description": "Unit the metered volume is expressed in",
                "minCardinality": 1,
                "maxCardinality": 1,
                "characteristicValueSpecification": [
                    {
                        "@type": "StringCharacteristicValueSpecification",
                        "isDefault": True,
                        "value": "MB",
                    }
                ],
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
        "validFor": {
            "startDateTime": "2026-01-01T00:00:00.000Z",
            "endDateTime": "2027-01-01T00:00:00.000Z",
        },
        "targetProductUsageSchema": {
            "@type": "TargetProductUsageSchema",
        },
    }


@pytest.fixture
def product_usage_specification_1(product_usage_specification_dict):
    return ProductUsageSpecification.from_dict(product_usage_specification_dict)


def test_product_usage_specification_instantiates_with_id(
    product_usage_specification_dict,
):
    pus = ProductUsageSpecification.from_dict(product_usage_specification_dict)
    assert pus.id == "pus-8801"
    assert pus.name == "Mobile data usage"
    assert pus.version == "2.1"
    assert pus.lastUpdate == "2026-05-14T08:30:00.000Z"
    assert pus.href.endswith("/productUsageSpecification/pus-8801")


def test_product_usage_specification_instantiates_classes(
    product_usage_specification_1,
):
    pus = product_usage_specification_1

    assert isinstance(pus, ProductUsageSpecification)
    assert pus.lifecycleStatus is ProductUsageSpecificationLifecycleStatusType.ACTIVE

    assert isinstance(pus.productSpecification[0], ProductSpecificationRef)
    assert pus.productSpecification[0].id == "ps-101"
    assert pus.productSpecification[0].version == "1.4"
    assert pus.productSpecification[0]._referred_type == "ProductSpecification"
    assert isinstance(
        pus.productSpecification[0].targetProductSchema, TargetProductSchema
    )

    assert isinstance(pus.serviceUsageSpecification[0], ServiceUsageSpecificationRef)
    assert pus.serviceUsageSpecification[0].id == "sus-55"
    assert (
        pus.serviceUsageSpecification[0]._referred_type == "ServiceUsageSpecification"
    )

    assert isinstance(pus.specCharacteristic[0], CharacteristicSpecification)
    assert pus.specCharacteristic[0].name == "volumeUnit"
    assert pus.specCharacteristic[0].minCardinality == 1
    assert isinstance(
        pus.specCharacteristic[0].characteristicValueSpecification[0],
        StringCharacteristicValueSpecification,
    )
    assert pus.specCharacteristic[0].characteristicValueSpecification[0].value == "MB"
    assert isinstance(pus.specCharacteristic[0].validFor, TimePeriod)

    assert isinstance(pus.attachment[0], AttachmentRefOrValue)
    assert pus.attachment[0].mimeType == "application/pdf"
    assert pus.attachment[0].isRef is False

    assert isinstance(pus.validFor, TimePeriod)
    assert pus.validFor.startDateTime == "2026-01-01T00:00:00.000Z"
    assert isinstance(pus.targetProductUsageSchema, TargetProductUsageSchema)


def test_product_usage_specification_defaults_to_empty_lists():
    pus = ProductUsageSpecification.from_dict(
        {"@type": "ProductUsageSpecification", "id": "pus-1", "name": "Voice usage"}
    )

    assert pus.productSpecification == []
    assert pus.serviceUsageSpecification == []
    assert pus.specCharacteristic == []
    assert pus.attachment == []
    assert pus.lifecycleStatus is None


def test_product_usage_specification_unknown_lifecycle_status_passes_through(
    product_usage_specification_dict,
):
    product_usage_specification_dict = dict(
        product_usage_specification_dict, lifecycleStatus="launched"
    )
    pus = ProductUsageSpecification.from_dict(product_usage_specification_dict)

    assert pus.lifecycleStatus == "launched"
    assert pus.to_dict()["lifecycleStatus"] == "launched"


def test_product_usage_specification_resource_path():
    context = Context(api_base_url="https://mycsp.com:8080/tmf-api")
    assert ProductUsageSpecification.get_resource_path(context) == (
        "https://mycsp.com:8080/tmf-api/productUsageCatalogManagement/v5"
        "/productUsageSpecification"
    )


def test_product_usage_specification_to_dict_round_trip(
    product_usage_specification_dict,
):
    result = ProductUsageSpecification.from_dict(
        product_usage_specification_dict
    ).to_dict()

    assert result["@type"] == "ProductUsageSpecification"
    assert "@baseType" not in result
    assert result["lifecycleStatus"] == "active"
    assert result["productSpecification"][0]["@referredType"] == "ProductSpecification"
    assert (
        result["serviceUsageSpecification"][0]["@referredType"]
        == "ServiceUsageSpecification"
    )
    assert (
        result["specCharacteristic"][0]["characteristicValueSpecification"][0]["@type"]
        == "StringCharacteristicValueSpecification"
    )
    assert result["validFor"]["endDateTime"] == "2027-01-01T00:00:00.000Z"


def test_target_product_usage_schema_serializes_schema_location():
    # Entity.from_dict only reverse-maps '@referredType', so '@schemaLocation' has to
    # be set through the '_schema_location' field to be emitted by to_dict().
    target_schema_dict = TargetProductUsageSchema(
        _schema_location="https://mycsp.com/schema/MobileDataUsage.json"
    ).to_dict()

    assert target_schema_dict["@type"] == "TargetProductUsageSchema"
    assert (
        target_schema_dict["@schemaLocation"]
        == "https://mycsp.com/schema/MobileDataUsage.json"
    )
