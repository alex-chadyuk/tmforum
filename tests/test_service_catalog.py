import pytest
from tmforum import (
    AssociationSpecificationRef,
    Attachment,
    AttachmentRef,
    CharacteristicSpecification,
    CharacteristicSpecificationRelationship,
    ConstraintRef,
    Context,
    EntitySpecificationRelationship,
    FeatureSpecification,
    FeatureSpecificationCharacteristic,
    FeatureSpecificationCharacteristicRelationship,
    FeatureSpecificationRelationship,
    Quantity,
    RelatedParty,
    ResourceSpecificationRef,
    ServiceCandidate,
    ServiceCandidateRef,
    ServiceCatalog,
    ServiceCategory,
    ServiceCategoryRef,
    ServiceLevelSpecificationRef,
    ServiceSpecRelationship,
    ServiceSpecification,
    ServiceSpecificationRef,
    StringCharacteristicValueSpecification,
    TargetEntitySchema,
    TimePeriod,
)


@pytest.fixture
def service_specification_dict():
    service_specification = {
        "@type": "ServiceSpecification",
        "@baseType": "Entity",
        "id": "ss-9001",
        "href": "/serviceCatalogManagement/v4/serviceSpecification/ss-9001",
        "name": "Business Internet Access",
        "description": "Specification for a managed business internet service",
        "version": "3.0",
        "isBundle": False,
        "lastUpdate": "2026-03-04T11:15:00Z",
        "lifecycleStatus": "Active",
        "validFor": {
            "startDateTime": "2026-01-01T00:00:00Z",
            "endDateTime": "2026-12-31T00:00:00Z",
        },
        "targetEntitySchema": {
            "@type": "TargetEntitySchema",
            "@schemaLocation": "https://mycsp.com/schema/Service.json",
        },
        "attachment": [
            {
                "@type": "Attachment",
                "id": "att-01",
                "name": "Service datasheet",
                "attachmentType": "document",
                "mimeType": "application/pdf",
                "url": "https://mycsp.com/docs/bia.pdf",
                "size": {"amount": 480, "units": "KB"},
            },
            {
                "@type": "AttachmentRef",
                "@referredType": "Attachment",
                "id": "att-02",
                "name": "Topology diagram",
                "url": "https://mycsp.com/docs/bia-topology.png",
            },
        ],
        "constraint": [
            {
                "@type": "ConstraintRef",
                "@referredType": "Constraint",
                "id": "cons-01",
                "name": "Maximum sites",
                "version": "1.2",
            }
        ],
        "entitySpecRelationship": [
            {
                "@type": "EntitySpecificationRelationship",
                "id": "esr-01",
                "name": "Managed CPE",
                "relationshipType": "dependency",
                "role": "supporting",
                "associationSpec": {
                    "@type": "AssociationSpecificationRef",
                    "@referredType": "AssociationSpecification",
                    "id": "as-01",
                    "name": "CPE association",
                },
                "validFor": {"startDateTime": "2026-01-01T00:00:00Z"},
            }
        ],
        "featureSpecification": [
            {
                "@type": "FeatureSpecification",
                "id": "feat-01",
                "name": "Static IP",
                "version": "1.0",
                "isBundle": False,
                "isEnabled": True,
                "constraint": [
                    {
                        "@type": "ConstraintRef",
                        "@referredType": "Constraint",
                        "id": "cons-02",
                        "name": "Address pool limit",
                    }
                ],
                "featureSpecRelationship": [
                    {
                        "@type": "FeatureSpecificationRelationship",
                        "featureId": "feat-02",
                        "name": "IPv6 addressing",
                        "relationshipType": "exclusivity",
                    }
                ],
                "featureSpecCharacteristic": [
                    {
                        "@type": "FeatureSpecificationCharacteristic",
                        "@baseType": "CharacteristicSpecification",
                        "id": "fsc-01",
                        "name": "Address count",
                        "valueType": "integer",
                        "featureSpecCharRelationship": [
                            {
                                "@type": "FeatureSpecificationCharacteristicRelationship",
                                "characteristicId": "fsc-02",
                                "featureId": "feat-02",
                                "name": "Prefix length",
                                "relationshipType": "dependency",
                            }
                        ],
                        "featureSpecCharacteristicValue": [
                            {
                                "@type": "IntegerCharacteristicValueSpecification",
                                "@baseType": "CharacteristicValueSpecification",
                                "isDefault": True,
                                "value": 5,
                            }
                        ],
                    }
                ],
            }
        ],
        "relatedParty": [
            {
                "@type": "RelatedParty",
                "id": "party-77",
                "name": "Service Design",
                "role": "owner",
            }
        ],
        "resourceSpecification": [
            {
                "@type": "ResourceSpecificationRef",
                "@referredType": "ResourceSpecification",
                "id": "rs-4501",
                "name": "Fiber Access Port",
                "version": "2.1",
            }
        ],
        "serviceLevelSpecification": [
            {
                "@type": "ServiceLevelSpecificationRef",
                "@referredType": "ServiceLevelSpecification",
                "id": "sls-01",
                "name": "Gold SLA",
            }
        ],
        "serviceSpecRelationship": [
            {
                "@type": "ServiceSpecRelationship",
                "id": "ss-9000",
                "name": "Legacy Internet Access",
                "relationshipType": "migration",
                "role": "predecessor",
                "validFor": {"startDateTime": "2026-01-01T00:00:00Z"},
            }
        ],
        "specCharacteristic": [
            {
                "@type": "CharacteristicSpecification",
                "id": "cs-01",
                "name": "Bandwidth",
                "valueType": "string",
                "minCardinality": 1,
                "maxCardinality": 1,
                "charSpecRelationship": [
                    {
                        "@type": "CharacteristicSpecificationRelationship",
                        "characteristicSpecificationId": "cs-02",
                        "name": "Burst rate",
                        "relationshipType": "dependency",
                    }
                ],
                "characteristicValueSpecification": [
                    {
                        "@type": "StringCharacteristicValueSpecification",
                        "@baseType": "CharacteristicValueSpecification",
                        "isDefault": True,
                        "value": "1G",
                    }
                ],
            }
        ],
    }
    return service_specification


@pytest.fixture
def service_specification_1(service_specification_dict):
    return ServiceSpecification.from_dict(service_specification_dict)


def test_service_specification_instantiates_with_id(service_specification_dict):
    service_specification = ServiceSpecification.from_dict(service_specification_dict)
    assert service_specification.id == "ss-9001"
    assert service_specification.name == "Business Internet Access"
    assert service_specification.version == "3.0"
    assert service_specification.isBundle is False
    assert service_specification.lifecycleStatus == "Active"


def test_service_specification_instantiates_classes(service_specification_1):
    feature_specification = service_specification_1.featureSpecification[0]
    feature_characteristic = feature_specification.featureSpecCharacteristic[0]
    entity_spec_relationship = service_specification_1.entitySpecRelationship[0]
    characteristic_specification = service_specification_1.specCharacteristic[0]
    assert isinstance(service_specification_1.validFor, TimePeriod)
    assert isinstance(service_specification_1.targetEntitySchema, TargetEntitySchema)
    assert isinstance(service_specification_1.attachment[0], Attachment)
    assert isinstance(service_specification_1.attachment[0].size, Quantity)
    assert isinstance(service_specification_1.attachment[1], AttachmentRef)
    assert isinstance(service_specification_1.constraint[0], ConstraintRef)
    assert service_specification_1.constraint[0].version == "1.2"
    assert isinstance(entity_spec_relationship, EntitySpecificationRelationship)
    assert isinstance(
        entity_spec_relationship.associationSpec, AssociationSpecificationRef
    )
    assert isinstance(entity_spec_relationship.validFor, TimePeriod)
    assert isinstance(feature_specification, FeatureSpecification)
    assert isinstance(feature_specification.constraint[0], ConstraintRef)
    assert isinstance(
        feature_specification.featureSpecRelationship[0],
        FeatureSpecificationRelationship,
    )
    # The annotation is List[CharacteristicSpecification]; the payload's '@type'
    # narrows it to the FeatureSpecification-specific subclass.
    assert isinstance(feature_characteristic, FeatureSpecificationCharacteristic)
    assert isinstance(feature_characteristic, CharacteristicSpecification)
    assert isinstance(
        feature_characteristic.featureSpecCharRelationship[0],
        FeatureSpecificationCharacteristicRelationship,
    )
    assert feature_characteristic.featureSpecCharacteristicValue[0].value == 5
    assert isinstance(service_specification_1.relatedParty[0], RelatedParty)
    assert service_specification_1.relatedParty[0].role == "owner"
    assert isinstance(
        service_specification_1.resourceSpecification[0], ResourceSpecificationRef
    )
    assert isinstance(
        service_specification_1.serviceLevelSpecification[0],
        ServiceLevelSpecificationRef,
    )
    assert isinstance(
        service_specification_1.serviceSpecRelationship[0], ServiceSpecRelationship
    )
    assert isinstance(characteristic_specification, CharacteristicSpecification)
    assert isinstance(
        characteristic_specification.charSpecRelationship[0],
        CharacteristicSpecificationRelationship,
    )
    assert isinstance(
        characteristic_specification.characteristicValueSpecification[0],
        StringCharacteristicValueSpecification,
    )


def test_service_specification_to_dict_round_trip(service_specification_1):
    service_specification_dict = service_specification_1.to_dict()
    assert service_specification_dict["@type"] == "ServiceSpecification"
    # ServiceSpecification derives directly from Entity, so no @baseType is emitted.
    assert "@baseType" not in service_specification_dict
    assert service_specification_dict["attachment"][0]["@type"] == "Attachment"
    assert service_specification_dict["attachment"][1]["@type"] == "AttachmentRef"
    assert service_specification_dict["attachment"][1]["@referredType"] == "Attachment"
    assert service_specification_dict["constraint"][0]["@referredType"] == "Constraint"
    entity_spec_relationship_dict = service_specification_dict[
        "entitySpecRelationship"
    ][0]
    assert (
        entity_spec_relationship_dict["associationSpec"]["@type"]
        == "AssociationSpecificationRef"
    )
    feature_characteristic_dict = service_specification_dict["featureSpecification"][0][
        "featureSpecCharacteristic"
    ][0]
    assert feature_characteristic_dict["@type"] == "FeatureSpecificationCharacteristic"
    assert feature_characteristic_dict["@baseType"] == "CharacteristicSpecification"
    assert (
        feature_characteristic_dict["featureSpecCharRelationship"][0]["@type"]
        == "FeatureSpecificationCharacteristicRelationship"
    )
    char_spec_dict = service_specification_dict["specCharacteristic"][0]
    assert char_spec_dict["@type"] == "CharacteristicSpecification"
    value_spec_dict = char_spec_dict["characteristicValueSpecification"][0]
    assert value_spec_dict["@type"] == "StringCharacteristicValueSpecification"
    assert value_spec_dict["@baseType"] == "CharacteristicValueSpecification"
    assert value_spec_dict["value"] == "1G"


def test_target_entity_schema_serializes_schema_location():
    # Entity.from_dict only reverse-maps '@referredType', so '@schemaLocation' has to
    # be set through the '_schema_location' field to be emitted by to_dict().
    target_entity_schema = TargetEntitySchema(
        _schema_location="https://mycsp.com/schema/Service.json"
    )
    target_entity_schema_dict = target_entity_schema.to_dict()
    assert target_entity_schema_dict["@type"] == "TargetEntitySchema"
    assert (
        target_entity_schema_dict["@schemaLocation"]
        == "https://mycsp.com/schema/Service.json"
    )


def test_service_specification_raises_when_characteristic_not_a_list():
    with pytest.raises(ValueError):
        ServiceSpecification(
            name="Bad specification",
            specCharacteristic=CharacteristicSpecification(id="cs-01"),
        )


def test_service_specification_resource_path_is_v4():
    context = Context(api_base_url="https://mycsp.com/tmf-api")
    assert (
        ServiceSpecification.get_resource_path(context)
        == "https://mycsp.com/tmf-api/serviceCatalogManagement/v4/serviceSpecification"
    )


@pytest.fixture
def service_candidate_dict():
    service_candidate = {
        "@type": "ServiceCandidate",
        "@baseType": "Entity",
        "id": "sc-201",
        "href": "/serviceCatalogManagement/v4/serviceCandidate/sc-201",
        "name": "Business Internet Access - Retail",
        "description": "Retail offering of the business internet service",
        "version": "1.4",
        "lastUpdate": "2026-03-05T08:00:00Z",
        "lifecycleStatus": "Active",
        "validFor": {"startDateTime": "2026-01-01T00:00:00Z"},
        "category": [
            {
                "@type": "ServiceCategoryRef",
                "@referredType": "ServiceCategory",
                "id": "scat-10",
                "name": "Connectivity",
                "version": "2.0",
            }
        ],
        "serviceSpecification": {
            "@type": "ServiceSpecificationRef",
            "@referredType": "ServiceSpecification",
            "id": "ss-9001",
            "name": "Business Internet Access",
            "version": "3.0",
        },
    }
    return service_candidate


@pytest.fixture
def service_candidate_1(service_candidate_dict):
    return ServiceCandidate.from_dict(service_candidate_dict)


def test_service_candidate_instantiates_classes(service_candidate_1):
    assert service_candidate_1.id == "sc-201"
    assert service_candidate_1.version == "1.4"
    assert isinstance(service_candidate_1.validFor, TimePeriod)
    assert isinstance(service_candidate_1.category[0], ServiceCategoryRef)
    assert service_candidate_1.category[0].version == "2.0"
    assert isinstance(service_candidate_1.serviceSpecification, ServiceSpecificationRef)


def test_service_candidate_to_dict_round_trip(service_candidate_1):
    service_candidate_dict = service_candidate_1.to_dict()
    assert service_candidate_dict["@type"] == "ServiceCandidate"
    assert "@baseType" not in service_candidate_dict
    assert service_candidate_dict["category"][0]["@type"] == "ServiceCategoryRef"
    assert service_candidate_dict["category"][0]["@referredType"] == "ServiceCategory"
    assert (
        service_candidate_dict["serviceSpecification"]["@referredType"]
        == "ServiceSpecification"
    )


def test_service_candidate_resource_path():
    context = Context(api_base_url="https://mycsp.com/tmf-api")
    assert (
        ServiceCandidate.get_resource_path(context)
        == "https://mycsp.com/tmf-api/serviceCatalogManagement/v4/serviceCandidate"
    )


@pytest.fixture
def service_category_dict():
    service_category = {
        "@type": "ServiceCategory",
        "@baseType": "Entity",
        "id": "scat-10",
        "href": "/serviceCatalogManagement/v4/serviceCategory/scat-10",
        "name": "Connectivity",
        "description": "Connectivity services",
        "version": "2.0",
        "isRoot": True,
        "parentId": None,
        "lastUpdate": "2026-03-05T08:00:00Z",
        "lifecycleStatus": "Active",
        "validFor": {"startDateTime": "2026-01-01T00:00:00Z"},
        "category": [
            {
                "@type": "ServiceCategoryRef",
                "@referredType": "ServiceCategory",
                "id": "scat-11",
                "name": "Fixed access",
                "version": "1.0",
            }
        ],
        "serviceCandidate": [
            {
                "@type": "ServiceCandidateRef",
                "@referredType": "ServiceCandidate",
                "id": "sc-201",
                "name": "Business Internet Access - Retail",
                "version": "1.4",
            }
        ],
    }
    return service_category


@pytest.fixture
def service_category_1(service_category_dict):
    return ServiceCategory.from_dict(service_category_dict)


def test_service_category_instantiates_classes(service_category_1):
    assert service_category_1.id == "scat-10"
    assert service_category_1.isRoot is True
    assert isinstance(service_category_1.validFor, TimePeriod)
    assert isinstance(service_category_1.category[0], ServiceCategoryRef)
    assert isinstance(service_category_1.serviceCandidate[0], ServiceCandidateRef)
    assert service_category_1.serviceCandidate[0].version == "1.4"


def test_service_category_to_dict_round_trip(service_category_1):
    service_category_dict = service_category_1.to_dict()
    assert service_category_dict["@type"] == "ServiceCategory"
    assert "@baseType" not in service_category_dict
    assert service_category_dict["isRoot"] is True
    assert (
        service_category_dict["serviceCandidate"][0]["@referredType"]
        == "ServiceCandidate"
    )


def test_service_category_raises_when_service_candidate_not_a_list():
    with pytest.raises(ValueError):
        ServiceCategory(
            name="Bad category",
            serviceCandidate=ServiceCandidateRef(id="sc-201"),
        )


def test_service_category_resource_path():
    context = Context(api_base_url="https://mycsp.com/tmf-api")
    assert (
        ServiceCategory.get_resource_path(context)
        == "https://mycsp.com/tmf-api/serviceCatalogManagement/v4/serviceCategory"
    )


@pytest.fixture
def service_catalog_dict():
    service_catalog = {
        "@type": "ServiceCatalog",
        "@baseType": "Entity",
        "id": "scl-1",
        "href": "/serviceCatalogManagement/v4/serviceCatalog/scl-1",
        "name": "Enterprise Service Catalog",
        "description": "Services offered to enterprise customers",
        "version": "5.2",
        "lastUpdate": "2026-03-05T08:00:00Z",
        "lifecycleStatus": "Active",
        "validFor": {
            "startDateTime": "2026-01-01T00:00:00Z",
            "endDateTime": "2026-12-31T00:00:00Z",
        },
        "category": [
            {
                "@type": "ServiceCategoryRef",
                "@referredType": "ServiceCategory",
                "id": "scat-10",
                "name": "Connectivity",
                "version": "2.0",
            }
        ],
        "relatedParty": [
            {
                "@type": "RelatedParty",
                "id": "party-77",
                "name": "Service Design",
                "role": "owner",
            }
        ],
    }
    return service_catalog


@pytest.fixture
def service_catalog_1(service_catalog_dict):
    return ServiceCatalog.from_dict(service_catalog_dict)


def test_service_catalog_instantiates_classes(service_catalog_1):
    assert service_catalog_1.id == "scl-1"
    assert service_catalog_1.version == "5.2"
    assert isinstance(service_catalog_1.validFor, TimePeriod)
    assert service_catalog_1.validFor._length_ms() > 0
    assert isinstance(service_catalog_1.category[0], ServiceCategoryRef)
    assert isinstance(service_catalog_1.relatedParty[0], RelatedParty)


def test_service_catalog_to_dict_round_trip(service_catalog_1):
    service_catalog_dict = service_catalog_1.to_dict()
    assert service_catalog_dict["@type"] == "ServiceCatalog"
    assert "@baseType" not in service_catalog_dict
    assert service_catalog_dict["category"][0]["@type"] == "ServiceCategoryRef"
    assert service_catalog_dict["relatedParty"][0]["@type"] == "RelatedParty"


def test_service_catalog_raises_when_category_not_a_list():
    with pytest.raises(ValueError):
        ServiceCatalog(
            name="Bad catalog",
            category=ServiceCategoryRef(id="scat-10"),
        )


def test_service_catalog_resource_path():
    context = Context(api_base_url="https://mycsp.com/tmf-api")
    assert (
        ServiceCatalog.get_resource_path(context)
        == "https://mycsp.com/tmf-api/serviceCatalogManagement/v4/serviceCatalog"
    )
