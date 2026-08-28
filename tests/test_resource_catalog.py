import pytest
from tmforum import (
    Attachment,
    AttachmentRef,
    CharacteristicSpecification,
    CharacteristicSpecificationRelationship,
    ConnectionAssociationType,
    ConnectionPointSpecificationRef,
    ConnectionSpecification,
    Context,
    EndpointSpecificationRef,
    ExternalIdentifier,
    FeatureSpecification,
    FeatureSpecificationRelationship,
    IntentSpecificationRef,
    LogicalResourceSpecification,
    PartyRoleRef,
    PhysicalResourceSpecification,
    PolicyRef,
    Quantity,
    RelatedPartyRefOrPartyRoleRef,
    ResourceFunctionSpecification,
    ResourceGraphSpecification,
    ResourceGraphSpecificationRef,
    ResourceGraphSpecificationRelationship,
    ResourceGraphSpecificationRelationshipType,
    ResourceSpecification,
    ResourceSpecificationRelationship,
    StringCharacteristicValueSpecification,
    TargetResourceSchema,
    TimePeriod,
)


@pytest.fixture
def resource_specification_dict():
    resource_specification = {
        "@type": "ResourceSpecification",
        "@baseType": "Entity",
        "id": "rs-4501",
        "href": "/resourceCatalog/v5/resourceSpecification/rs-4501",
        "name": "Fiber Access Port",
        "description": "Specification for an optical access port",
        "version": "2.1",
        "category": "NetworkConnectivity",
        "isBundle": False,
        "lastUpdate": "2026-02-11T09:30:00Z",
        "lifecycleStatus": "Active",
        "validFor": {
            "startDateTime": "2026-01-01T00:00:00Z",
            "endDateTime": "2026-12-31T00:00:00Z",
        },
        "targetResourceSchema": {
            "@type": "TargetResourceSchema",
            "@schemaLocation": "https://mycsp.com/schema/LogicalResource.json",
        },
        "featureSpecification": [
            {
                "@type": "FeatureSpecification",
                "id": "feat-01",
                "name": "Bandwidth Profile",
                "version": "1.0",
                "isBundle": False,
                "isEnabled": True,
                "validFor": {"startDateTime": "2026-01-01T00:00:00Z"},
                "featureSpecRelationship": [
                    {
                        "@type": "FeatureSpecificationRelationship",
                        "relationshipType": "requires",
                        "featureId": "feat-02",
                        "name": "QoS Profile",
                        "parentSpecificationId": "rs-4501",
                        "parentSpecificationHref": (
                            "/resourceCatalog/v5/resourceSpecification/rs-4501"
                        ),
                    }
                ],
                "policyConstraint": [
                    {
                        "@type": "PolicyRef",
                        "@referredType": "Policy",
                        "id": "pol-01",
                        "name": "Fair Use Policy",
                        "version": "3.0",
                    }
                ],
                "featureSpecCharacteristic": [
                    {
                        "@type": "CharacteristicSpecification",
                        "id": "cs-99",
                        "name": "downstreamRate",
                        "valueType": "integer",
                    }
                ],
            }
        ],
        "attachment": [
            {
                "@type": "Attachment",
                "id": "att-01",
                "name": "Datasheet",
                "attachmentType": "document",
                "mimeType": "application/pdf",
                "url": "https://mycsp.com/docs/port.pdf",
                "size": {"@type": "Quantity", "amount": 412, "units": "KB"},
            },
            {
                "@type": "AttachmentRef",
                "@referredType": "Attachment",
                "id": "att-02",
                "name": "Wiring diagram",
                "url": "https://mycsp.com/docs/wiring.png",
            },
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "role": "specificationOwner",
                "partyOrPartyRole": {
                    "@type": "PartyRoleRef",
                    "@referredType": "PartyRole",
                    "id": "pr-01",
                    "name": "Network Planning",
                    "partyId": "party-07",
                    "partyName": "ACME Networks",
                },
            }
        ],
        "resourceSpecCharacteristic": [
            {
                "@type": "CharacteristicSpecification",
                "id": "cs-01",
                "name": "portSpeed",
                "valueType": "string",
                "description": "Nominal speed of the port",
                "configurable": True,
                "minCardinality": 1,
                "maxCardinality": 1,
                "isUnique": False,
                "extensible": False,
                "regex": "^[0-9]+G$",
                "validFor": {"startDateTime": "2026-01-01T00:00:00Z"},
                "charSpecRelationship": [
                    {
                        "@type": "CharacteristicSpecificationRelationship",
                        "relationshipType": "dependency",
                        "name": "portType",
                        "characteristicSpecificationId": "cs-02",
                        "parentSpecificationId": "rs-4501",
                        "parentSpecificationHref": (
                            "/resourceCatalog/v5/resourceSpecification/rs-4501"
                        ),
                    }
                ],
                "characteristicValueSpecification": [
                    {
                        "@type": "StringCharacteristicValueSpecification",
                        "@baseType": "CharacteristicValueSpecification",
                        "valueType": "string",
                        "isDefault": True,
                        "unitOfMeasure": "Gbps",
                        "value": "10G",
                    }
                ],
            }
        ],
        "resourceSpecRelationship": [
            {
                "@type": "ResourceSpecificationRelationship",
                "id": "rs-4502",
                "href": "/resourceCatalog/v5/resourceSpecification/rs-4502",
                "name": "Optical Line Terminal",
                "relationshipType": "dependency",
                "role": "parent",
                "defaultQuantity": 1,
                "minimumQuantity": 1,
                "maximumQuantity": 4,
                "characteristic": [
                    {
                        "@type": "CharacteristicSpecification",
                        "id": "cs-03",
                        "name": "slotNumber",
                        "valueType": "integer",
                    }
                ],
            }
        ],
        "intentSpecification": {
            "@type": "IntentSpecificationRef",
            "@referredType": "IntentSpecification",
            "id": "int-01",
            "name": "Latency intent",
        },
        "externalIdentifier": [
            {
                "@type": "ExternalIdentifier",
                "id": "ext-01",
                "owner": "LegacyInventory",
                "externalIdentifierType": "inventoryId",
            }
        ],
    }
    return resource_specification


@pytest.fixture
def resource_specification_1(resource_specification_dict):
    return ResourceSpecification.from_dict(resource_specification_dict)


def test_resource_specification_instantiates_with_id(resource_specification_dict):
    resource_specification = ResourceSpecification.from_dict(
        resource_specification_dict
    )
    assert resource_specification.id == "rs-4501"
    assert resource_specification.version == "2.1"
    assert resource_specification.isBundle is False
    assert resource_specification.category == "NetworkConnectivity"


def test_resource_specification_instantiates_classes(resource_specification_1):
    feature_specification = resource_specification_1.featureSpecification[0]
    characteristic_specification = resource_specification_1.resourceSpecCharacteristic[
        0
    ]
    related_party = resource_specification_1.relatedParty[0]
    assert isinstance(resource_specification_1.validFor, TimePeriod)
    assert isinstance(
        resource_specification_1.targetResourceSchema, TargetResourceSchema
    )
    assert isinstance(feature_specification, FeatureSpecification)
    assert isinstance(
        feature_specification.featureSpecRelationship[0],
        FeatureSpecificationRelationship,
    )
    assert isinstance(feature_specification.policyConstraint[0], PolicyRef)
    assert isinstance(
        feature_specification.featureSpecCharacteristic[0], CharacteristicSpecification
    )
    assert isinstance(resource_specification_1.attachment[0], Attachment)
    assert isinstance(resource_specification_1.attachment[0].size, Quantity)
    assert isinstance(resource_specification_1.attachment[1], AttachmentRef)
    assert isinstance(related_party, RelatedPartyRefOrPartyRoleRef)
    assert isinstance(related_party.partyOrPartyRole, PartyRoleRef)
    assert isinstance(characteristic_specification, CharacteristicSpecification)
    assert isinstance(
        characteristic_specification.charSpecRelationship[0],
        CharacteristicSpecificationRelationship,
    )
    assert isinstance(
        characteristic_specification.characteristicValueSpecification[0],
        StringCharacteristicValueSpecification,
    )
    assert isinstance(
        resource_specification_1.resourceSpecRelationship[0],
        ResourceSpecificationRelationship,
    )
    assert isinstance(
        resource_specification_1.intentSpecification, IntentSpecificationRef
    )
    assert isinstance(
        resource_specification_1.externalIdentifier[0], ExternalIdentifier
    )


def test_resource_specification_to_dict_round_trip(resource_specification_1):
    resource_specification_dict = resource_specification_1.to_dict()
    assert resource_specification_dict["@type"] == "ResourceSpecification"
    # ResourceSpecification derives directly from Entity, so no @baseType is emitted.
    assert "@baseType" not in resource_specification_dict
    assert (
        resource_specification_dict["targetResourceSchema"]["@type"]
        == "TargetResourceSchema"
    )
    assert resource_specification_dict["attachment"][0]["@type"] == "Attachment"
    assert resource_specification_dict["attachment"][1]["@type"] == "AttachmentRef"
    assert resource_specification_dict["attachment"][1]["@referredType"] == "Attachment"
    char_spec_dict = resource_specification_dict["resourceSpecCharacteristic"][0]
    assert char_spec_dict["@type"] == "CharacteristicSpecification"
    value_spec_dict = char_spec_dict["characteristicValueSpecification"][0]
    assert value_spec_dict["@type"] == "StringCharacteristicValueSpecification"
    assert value_spec_dict["@baseType"] == "CharacteristicValueSpecification"
    assert value_spec_dict["value"] == "10G"


def test_target_resource_schema_serializes_schema_location():
    # Entity.from_dict only reverse-maps '@referredType', so '@schemaLocation' has to
    # be set through the '_schema_location' field to be emitted by to_dict().
    target_resource_schema = TargetResourceSchema(
        _schema_location="https://mycsp.com/schema/LogicalResource.json"
    )
    target_resource_schema_dict = target_resource_schema.to_dict()
    assert target_resource_schema_dict["@type"] == "TargetResourceSchema"
    assert (
        target_resource_schema_dict["@schemaLocation"]
        == "https://mycsp.com/schema/LogicalResource.json"
    )


def test_resource_specification_raises_when_feature_not_a_list():
    with pytest.raises(ValueError):
        ResourceSpecification(
            name="Bad specification",
            featureSpecification=FeatureSpecification(id="feat-01"),
        )


def test_resource_specification_resource_path_is_v5():
    context = Context(api_base_url="https://mycsp.com/tmf-api")
    assert (
        ResourceSpecification.get_resource_path(context)
        == "https://mycsp.com/tmf-api/resourceCatalog/v5/resourceSpecification"
    )


@pytest.fixture
def physical_resource_specification_dict():
    physical_resource_specification = {
        "@type": "PhysicalResourceSpecification",
        "@baseType": "ResourceSpecification",
        "id": "prs-01",
        "href": "/resourceCatalog/v5/resourceSpecification/prs-01",
        "name": "SFP+ Transceiver",
        "category": "PhysicalLinks",
        "model": "SFP-10G-LR",
        "part": "PN-889201",
        "sku": "SKU-77123",
        "vendor": "ACME Optics",
    }
    return physical_resource_specification


def test_physical_resource_specification_from_dict(
    physical_resource_specification_dict,
):
    physical_resource_specification = ResourceSpecification.from_dict(
        physical_resource_specification_dict
    )
    assert isinstance(physical_resource_specification, PhysicalResourceSpecification)
    assert physical_resource_specification.model == "SFP-10G-LR"
    assert physical_resource_specification.part == "PN-889201"
    assert physical_resource_specification.sku == "SKU-77123"
    assert physical_resource_specification.vendor == "ACME Optics"
    assert physical_resource_specification.category == "PhysicalLinks"


def test_physical_resource_specification_to_dict_round_trip(
    physical_resource_specification_dict,
):
    physical_resource_specification = ResourceSpecification.from_dict(
        physical_resource_specification_dict
    ).to_dict()
    assert physical_resource_specification["@type"] == "PhysicalResourceSpecification"
    assert physical_resource_specification["@baseType"] == "ResourceSpecification"
    assert physical_resource_specification["vendor"] == "ACME Optics"


def test_physical_resource_specification_shares_the_specification_path():
    context = Context(api_base_url="https://mycsp.com/tmf-api")
    assert (
        PhysicalResourceSpecification.get_resource_path(context)
        == "https://mycsp.com/tmf-api/resourceCatalog/v5/resourceSpecification"
    )


@pytest.fixture
def resource_function_specification_dict():
    resource_function_specification = {
        "@type": "ResourceFunctionSpecification",
        "@baseType": "LogicalResourceSpecification",
        "id": "rfs-01",
        "href": "/resourceCatalog/v5/resourceSpecification/rfs-01",
        "name": "Medium Enterprise Firewall",
        "category": "Generic",
        "connectionPointSpecification": [
            {
                "@type": "ConnectionPointSpecificationRef",
                "@referredType": "ConnectionPointSpecification",
                "id": "cps-01",
                "name": "WAN SAP",
                "version": "1.2",
            }
        ],
        "connectivitySpecification": [
            {
                "@type": "ResourceGraphSpecification",
                "id": "rgs-01",
                "href": "/resourceCatalog/v5/resourceGraphSpecification/rgs-01",
                "name": "Internal connectivity",
                "description": "Potential internal connectivity of the firewall",
                "graphSpecificationRelationship": [
                    {
                        "@type": "ResourceGraphSpecificationRelationship",
                        "relationshipType": "connectivity",
                        "resourceGraph": {
                            "@type": "ResourceGraphSpecificationRef",
                            "@referredType": "ResourceGraphSpecification",
                            "id": "rgs-02",
                            "name": "Management plane graph",
                        },
                    }
                ],
                "connectionSpecification": [
                    {
                        "@type": "ConnectionSpecification",
                        "id": "cs-edge-01",
                        "name": "WAN to LAN",
                        "associationType": "pointtoPoint",
                        "endpointSpecification": [
                            {
                                "@type": "EndpointSpecificationRef",
                                "@referredType": "EndpointSpecification",
                                "id": "es-01",
                                "name": "WAN endpoint",
                                "role": "source",
                                "isRoot": True,
                                "connectionPointSpecification": {
                                    "@type": "ConnectionPointSpecificationRef",
                                    "@referredType": "ConnectionPointSpecification",
                                    "id": "cps-01",
                                    "version": "1.2",
                                },
                            }
                        ],
                    }
                ],
            }
        ],
    }
    return resource_function_specification


@pytest.fixture
def resource_function_specification_1(resource_function_specification_dict):
    return ResourceSpecification.from_dict(resource_function_specification_dict)


def test_resource_function_specification_instantiates_classes(
    resource_function_specification_1,
):
    assert isinstance(resource_function_specification_1, ResourceFunctionSpecification)
    assert isinstance(resource_function_specification_1, LogicalResourceSpecification)
    assert isinstance(
        resource_function_specification_1.connectionPointSpecification[0],
        ConnectionPointSpecificationRef,
    )
    graph = resource_function_specification_1.connectivitySpecification[0]
    assert isinstance(graph, ResourceGraphSpecification)
    relationship = graph.graphSpecificationRelationship[0]
    assert isinstance(relationship, ResourceGraphSpecificationRelationship)
    assert (
        relationship.relationshipType
        is ResourceGraphSpecificationRelationshipType.CONNECTIVITY
    )
    assert isinstance(relationship.resourceGraph, ResourceGraphSpecificationRef)
    connection = graph.connectionSpecification[0]
    assert isinstance(connection, ConnectionSpecification)
    assert connection.associationType is ConnectionAssociationType.POINT_TO_POINT
    endpoint = connection.endpointSpecification[0]
    assert isinstance(endpoint, EndpointSpecificationRef)
    assert endpoint.isRoot is True
    assert endpoint.role == "source"
    assert isinstance(
        endpoint.connectionPointSpecification, ConnectionPointSpecificationRef
    )


def test_resource_function_specification_to_dict_round_trip(
    resource_function_specification_1,
):
    resource_function_specification_dict = resource_function_specification_1.to_dict()
    assert (
        resource_function_specification_dict["@type"] == "ResourceFunctionSpecification"
    )
    assert (
        resource_function_specification_dict["@baseType"]
        == "LogicalResourceSpecification"
    )
    graph_dict = resource_function_specification_dict["connectivitySpecification"][0]
    assert graph_dict["@type"] == "ResourceGraphSpecification"
    relationship_dict = graph_dict["graphSpecificationRelationship"][0]
    assert relationship_dict["relationshipType"] == "connectivity"
    assert (
        relationship_dict["resourceGraph"]["@type"] == "ResourceGraphSpecificationRef"
    )
    connection_dict = graph_dict["connectionSpecification"][0]
    assert connection_dict["associationType"] == "pointtoPoint"
    endpoint_dict = connection_dict["endpointSpecification"][0]
    assert endpoint_dict["@type"] == "EndpointSpecificationRef"
    assert endpoint_dict["@referredType"] == "EndpointSpecification"
    assert (
        endpoint_dict["connectionPointSpecification"]["@type"]
        == "ConnectionPointSpecificationRef"
    )


def test_resource_graph_specification_raises_when_connection_not_a_list():
    with pytest.raises(ValueError):
        ResourceGraphSpecification(
            name="Bad graph",
            connectionSpecification=ConnectionSpecification(id="cs-edge-01"),
        )


def test_connection_specification_raises_when_endpoint_not_a_list():
    with pytest.raises(ValueError):
        ConnectionSpecification(
            name="Bad connection",
            endpointSpecification=EndpointSpecificationRef(id="es-01"),
        )
