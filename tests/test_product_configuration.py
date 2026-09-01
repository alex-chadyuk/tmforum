import pytest
from tmforum import (
    BundledProductOffering,
    ChannelRef,
    Characteristic,
    ConfigurationAction,
    ConfigurationCharacteristic,
    Context,
    EntityRef,
    ItemRef,
    ProductConfiguration,
    ProductConfigurationItemRelationship,
    ProductOfferingRef,
    QueryProductConfiguration,
    QueryProductConfigurationItem,
    RelatedPartyRefOrPartyRoleRef,
    PartyRoleRef,
    StateReason,
    TaskStateType,
)


@pytest.fixture
def qpc_payload():
    return {
        "@type": "QueryProductConfiguration",
        "@baseType": "Entity",
        "id": "qpc-001",
        "href": "/queryProductConfiguration/qpc-001",
        "instantSync": True,
        "state": "done",
        "channel": {
            "@type": "ChannelRef",
            "@referredType": "Channel",
            "id": "web",
            "name": "Web Store",
        },
        "contextEntity": {
            "@type": "EntityRef",
            "@referredType": "ProductOrder",
            "id": "order-42",
            "href": "/productOrder/order-42",
        },
        "contextCharacteristic": [
            {
                "@type": "Characteristic",
                "@baseType": "Entity",
                "name": "salesChannel",
                "value": "retail",
            }
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "@baseType": "Entity",
                "role": "customer",
                "partyOrPartyRole": {
                    "@type": "PartyRoleRef",
                    "@referredType": "Customer",
                    "id": "cust-7",
                },
            }
        ],
        "requestProductConfigurationItem": [
            {
                "@type": "QueryProductConfigurationItem",
                "@baseType": "Entity",
                "id": "001",
                "stateReason": [],
                "contextItem": {
                    "@type": "ItemRef",
                    "@referredType": "ProductOrderItem",
                    "id": "order-42",
                    "entityId": "order-42",
                    "itemId": "1",
                },
                "productConfiguration": {
                    "@type": "ProductConfiguration",
                    "@baseType": "Entity",
                    "isSelectable": True,
                    "isSelected": True,
                    "isVisible": True,
                    "configurationAction": [
                        {
                            "@type": "ConfigurationAction",
                            "@baseType": "Entity",
                            "action": "add",
                            "isSelected": True,
                        }
                    ],
                    "productOffering": {
                        "@type": "ProductOfferingRef",
                        "@referredType": "ProductOffering",
                        "id": "08b88d3a-80d5-4da2-a8d9-a0dadddb06f6",
                        "href": "/ProductOffering/08b88d3a-80d5-4da2-a8d9-a0dadddb06f6",
                    },
                    "configurationPrice": [],
                    "configurationTerm": [],
                    "configurationCharacteristic": [],
                    "policy": [],
                    "productConfiguration": [],
                },
                "productConfigurationItemRelationship": [],
                "queryProductConfigurationItem": [],
            }
        ],
        "computedProductConfigurationItem": [
            {
                "@type": "QueryProductConfigurationItem",
                "@baseType": "Entity",
                "id": "001",
                "state": "accepted",
                "stateReason": [
                    {
                        "@type": "StateReason",
                        "@baseType": "Entity",
                        "code": "OK",
                        "label": "Configuration is valid",
                    }
                ],
                "productConfiguration": {
                    "@type": "ProductConfiguration",
                    "@baseType": "Entity",
                    "isSelectable": True,
                    "isSelected": True,
                    "isVisible": True,
                    "configurationAction": [
                        {
                            "@type": "ConfigurationAction",
                            "@baseType": "Entity",
                            "action": "add",
                            "isSelected": True,
                        }
                    ],
                    "configurationCharacteristic": [
                        {
                            "@type": "ConfigurationCharacteristic",
                            "@baseType": "Entity",
                            "id": "bandwidth",
                            "name": "Bandwidth",
                            "isConfigurable": True,
                            "isVisible": True,
                            "minCardinality": 1,
                            "maxCardinality": 1,
                        }
                    ],
                    "productOffering": {
                        "@type": "BundledProductOffering",
                        "@baseType": "ProductOfferingRef",
                        "@referredType": "ProductOffering",
                        "id": "5f9d2b1e-1c4a-4f0b-9a3e-1d2c3b4a5f6e",
                        "name": "Fibre 500 Bundle",
                    },
                    "configurationPrice": [],
                    "configurationTerm": [],
                    "policy": [],
                    "productConfiguration": [],
                },
                "productConfigurationItemRelationship": [
                    {
                        "@type": "ProductConfigurationItemRelationship",
                        "@baseType": "Entity",
                        "id": "002",
                        "relationshipType": "bundled",
                    }
                ],
                "queryProductConfigurationItem": [
                    {
                        "@type": "QueryProductConfigurationItem",
                        "@baseType": "Entity",
                        "id": "002",
                        "state": "accepted",
                        "stateReason": [],
                        "productConfigurationItemRelationship": [],
                        "queryProductConfigurationItem": [],
                    }
                ],
            }
        ],
    }


@pytest.fixture
def qpc_1(qpc_payload):
    return QueryProductConfiguration.from_dict(qpc_payload)


def test_qpc_instantiates_classes(qpc_1):
    request_item = qpc_1.requestProductConfigurationItem[0]
    computed_item = qpc_1.computedProductConfigurationItem[0]
    prod_config = computed_item.productConfiguration

    assert isinstance(qpc_1, QueryProductConfiguration)
    assert isinstance(qpc_1.state, TaskStateType)
    assert isinstance(qpc_1.channel, ChannelRef)
    assert isinstance(qpc_1.contextEntity, EntityRef)
    assert isinstance(qpc_1.contextCharacteristic[0], Characteristic)
    assert isinstance(qpc_1.relatedParty[0], RelatedPartyRefOrPartyRoleRef)
    assert isinstance(qpc_1.relatedParty[0].partyOrPartyRole, PartyRoleRef)

    assert isinstance(request_item, QueryProductConfigurationItem)
    assert isinstance(request_item.contextItem, ItemRef)
    assert isinstance(request_item.productConfiguration, ProductConfiguration)
    assert isinstance(
        request_item.productConfiguration.productOffering, ProductOfferingRef
    )

    assert isinstance(computed_item, QueryProductConfigurationItem)
    assert isinstance(computed_item.stateReason[0], StateReason)
    assert isinstance(
        computed_item.productConfigurationItemRelationship[0],
        ProductConfigurationItemRelationship,
    )
    assert isinstance(prod_config, ProductConfiguration)
    assert isinstance(prod_config.configurationAction[0], ConfigurationAction)
    assert isinstance(
        prod_config.configurationCharacteristic[0], ConfigurationCharacteristic
    )
    assert isinstance(prod_config.productOffering, BundledProductOffering)


def test_qpc_nested_items_are_recursive(qpc_1):
    nested = qpc_1.computedProductConfigurationItem[0].queryProductConfigurationItem[0]
    assert isinstance(nested, QueryProductConfigurationItem)
    assert nested.id == "002"
    assert nested.state == "accepted"


def test_item_ref_carries_entity_id(qpc_1):
    context_item = qpc_1.requestProductConfigurationItem[0].contextItem
    assert context_item.entityId == "order-42"
    assert context_item.itemId == "1"
    assert context_item.to_dict()["entityId"] == "order-42"


def test_qpc_item_throws_exception_when_id_missing():
    with pytest.raises(ValueError):
        QueryProductConfigurationItem.from_dict(
            {
                "@type": "QueryProductConfigurationItem",
                "@baseType": "Entity",
                "state": "accepted",
            }
        )


def test_qpc_round_trips_to_dict(qpc_1):
    qpc_dict = qpc_1.to_dict()

    assert qpc_dict["@type"] == "QueryProductConfiguration"
    assert qpc_dict["id"] == "qpc-001"
    assert qpc_dict["state"] == "done"
    assert qpc_dict["instantSync"] is True

    computed = qpc_dict["computedProductConfigurationItem"][0]
    assert computed["@type"] == "QueryProductConfigurationItem"
    assert computed["productConfiguration"]["@type"] == "ProductConfiguration"
    assert computed["queryProductConfigurationItem"][0]["id"] == "002"

    # direct Entity subclasses carry no @baseType; deeper subclasses do
    assert "@baseType" not in qpc_dict
    assert "@baseType" not in computed
    product_offering = computed["productConfiguration"]["productOffering"]
    assert product_offering["@type"] == "BundledProductOffering"
    assert product_offering["@baseType"] == "ProductOfferingRef"

    reparsed = QueryProductConfiguration.from_dict(qpc_dict)
    assert reparsed.to_dict() == qpc_dict


def test_query_product_configuration_resource_path():
    context = Context(api_base_url="https://mycsp.com/tmf-api")
    assert QueryProductConfiguration.get_resource_path(context) == (
        "https://mycsp.com/tmf-api/productConfiguration/v5/queryProductConfiguration"
    )
