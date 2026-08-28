import pytest
from tmforum import (
    AppointmentRef,
    AttachmentRefOrValue,
    CancelResourceOrder,
    Characteristic,
    Context,
    ExternalId,
    Note,
    OrderItemActionType,
    Quantity,
    RelatedParty,
    RelatedPlaceRefOrValue,
    ResourceOrder,
    ResourceOrderItem,
    ResourceOrderItemRef,
    ResourceOrderItemRelationship,
    ResourceOrderRef,
    ResourceRef,
    ResourceRefOrValue,
    ResourceRelationship,
    ResourceSpecificationRef,
    ResourceStatusType,
    TaskStateType,
    TimePeriod,
)


@pytest.fixture
def resource_order_dict():
    return {
        "@type": "ResourceOrder",
        "id": "ro-8801",
        "href": "https://mycsp.com/tmf-api/resourceOrderingManagement/v4/resourceOrder/ro-8801",
        "category": "NetworkProvisioning",
        "description": "Provision access circuit for site relocation",
        "name": "Site relocation order",
        "externalId": "CRM-55231",
        "orderType": "provision",
        "priority": 2,
        "state": "inProgress",
        "orderDate": "2026-03-04T09:15:00.000Z",
        "expectedCompletionDate": "2026-03-18T17:00:00.000Z",
        "requestedCompletionDate": "2026-03-20T17:00:00.000Z",
        "requestedStartDate": "2026-03-05T08:00:00.000Z",
        "startDate": "2026-03-05T08:12:00.000Z",
        "externalReference": [
            {
                "@type": "ExternalId",
                "id": "WO-44120",
                "entityType": "WorkOrder",
                "owner": "FieldOpsSystem",
            }
        ],
        "note": [
            {
                "@type": "Note",
                "id": "n-1",
                "author": "dispatcher",
                "date": "2026-03-04T09:20:00.000Z",
                "text": "Customer requires weekend cutover.",
            }
        ],
        "relatedParty": [
            {
                "@type": "RelatedParty",
                "id": "party-77",
                "name": "Northwind Logistics",
                "role": "customer",
            }
        ],
        "orderItem": [
            {
                "@type": "ResourceOrderItem",
                "id": "item-1",
                "action": "add",
                "quantity": 2,
                "state": "acknowledged",
                "appointment": {
                    "@type": "AppointmentRef",
                    "id": "appt-9",
                    "href": "https://mycsp.com/tmf-api/appointment/v4/appointment/appt-9",
                    "description": "Field engineer install slot",
                },
                "resourceSpecification": {
                    "@type": "ResourceSpecificationRef",
                    "id": "rs-4501",
                    "version": "2.1",
                },
                "resource": {
                    "@type": "ResourceRefOrValue",
                    "id": "res-3312",
                    "href": "https://mycsp.com/tmf-api/resourceInventory/v5/resource/res-3312",
                    "name": "Access circuit",
                    "category": "Gold",
                    "description": "10G access circuit",
                    "resourceVersion": "1.0",
                    "startOperatingDate": "2026-03-06T00:00:00.000Z",
                    "endOperatingDate": "2027-03-06T00:00:00.000Z",
                    "administrativeState": "unlocked",
                    "operationalState": "enable",
                    "resourceStatus": "reserved",
                    "usageState": "idle",
                    "@referredType": "LogicalResource",
                    "place": {
                        "@type": "RelatedPlaceRefOrValue",
                        "id": "place-12",
                        "href": "https://mycsp.com/tmf-api/geographicSite/v4/place-12",
                        "name": "Rotterdam DC",
                        "role": "installationSite",
                    },
                    "note": [
                        {
                            "@type": "Note",
                            "id": "n-2",
                            "text": "Pre-staged in warehouse.",
                        }
                    ],
                    "attachment": [
                        {
                            "@type": "AttachmentRefOrValue",
                            "id": "att-5",
                            "name": "site-survey.pdf",
                            "attachmentType": "document",
                            "mimeType": "application/pdf",
                            "url": "https://mycsp.com/files/site-survey.pdf",
                            "isRef": False,
                            "size": {"@type": "Quantity", "amount": 210, "units": "KB"},
                            "validFor": {
                                "@type": "TimePeriod",
                                "startDateTime": "2026-03-01T00:00:00.000Z",
                                "endDateTime": "2026-06-01T00:00:00.000Z",
                            },
                        }
                    ],
                    "relatedParty": [
                        {
                            "@type": "RelatedParty",
                            "id": "party-88",
                            "role": "installer",
                        }
                    ],
                    "resourceCharacteristic": [
                        {
                            "@type": "Characteristic",
                            "id": "c-1",
                            "name": "bandwidth",
                            "valueType": "String",
                        }
                    ],
                    "resourceRelationship": [
                        {
                            "@type": "ResourceRelationship",
                            "relationshipType": "dependsOn",
                            "resource": {"@type": "ResourceRef", "id": "res-9000"},
                        }
                    ],
                    "resourceSpecification": {
                        "@type": "ResourceSpecificationRef",
                        "id": "rs-4501",
                    },
                },
                "orderItemRelationship": [
                    {
                        "@type": "ResourceOrderItemRelationship",
                        "relationshipType": "dependency",
                        "orderItem": {
                            "@type": "ResourceOrderItemRef",
                            "itemId": "item-2",
                            "resourceOrderId": "ro-8802",
                            "resourceOrderHref": "https://mycsp.com/tmf-api/resourceOrderingManagement/v4/resourceOrder/ro-8802",
                            "@referredType": "ResourceOrderItem",
                        },
                    }
                ],
            }
        ],
    }


@pytest.fixture
def resource_order_1(resource_order_dict):
    return ResourceOrder.from_dict(resource_order_dict)


@pytest.fixture
def cancel_resource_order_dict():
    return {
        "@type": "CancelResourceOrder",
        "id": "cro-101",
        "href": "https://mycsp.com/tmf-api/resourceOrderingManagement/v4/cancelResourceOrder/cro-101",
        "cancellationReason": "Customer withdrew the relocation request",
        "requestedCancellationDate": "2026-03-06T10:00:00.000Z",
        "effectiveCancellationDate": "2026-03-06T11:30:00.000Z",
        "state": "done",
        "resourceOrder": {
            "@type": "ResourceOrderRef",
            "id": "ro-8801",
            "href": "https://mycsp.com/tmf-api/resourceOrderingManagement/v4/resourceOrder/ro-8801",
            "@referredType": "ResourceOrder",
        },
    }


def test_resource_order_instantiates_with_scalars(resource_order_1):
    assert resource_order_1.id == "ro-8801"
    assert resource_order_1.externalId == "CRM-55231"
    assert resource_order_1.orderType == "provision"
    assert resource_order_1.priority == 2
    assert resource_order_1.state == "inProgress"
    assert resource_order_1.completionDate is None


def test_resource_order_instantiates_classes(resource_order_1):
    order_item = resource_order_1.orderItem[0]
    resource = order_item.resource
    assert isinstance(resource_order_1.externalReference[0], ExternalId)
    assert resource_order_1.externalReference[0].entityType == "WorkOrder"
    assert isinstance(resource_order_1.note[0], Note)
    assert isinstance(resource_order_1.relatedParty[0], RelatedParty)
    assert isinstance(order_item, ResourceOrderItem)
    assert order_item.action is OrderItemActionType.ADD
    assert order_item.quantity == 2
    assert isinstance(order_item.appointment, AppointmentRef)
    assert isinstance(order_item.resourceSpecification, ResourceSpecificationRef)
    assert isinstance(
        order_item.orderItemRelationship[0], ResourceOrderItemRelationship
    )
    assert isinstance(
        order_item.orderItemRelationship[0].orderItem, ResourceOrderItemRef
    )
    assert order_item.orderItemRelationship[0].orderItem.itemId == "item-2"
    assert isinstance(resource, ResourceRefOrValue)


def test_resource_ref_or_value_nested_classes(resource_order_1):
    resource = resource_order_1.orderItem[0].resource
    assert resource.resourceStatus is ResourceStatusType.RESERVED
    assert resource._referred_type == "LogicalResource"
    assert isinstance(resource.place, RelatedPlaceRefOrValue)
    assert resource.place.id == "place-12"
    assert resource.place.name == "Rotterdam DC"
    assert isinstance(resource.note[0], Note)
    assert isinstance(resource.attachment[0], AttachmentRefOrValue)
    assert resource.attachment[0].isRef is False
    assert isinstance(resource.attachment[0].size, Quantity)
    assert isinstance(resource.attachment[0].validFor, TimePeriod)
    assert isinstance(resource.relatedParty[0], RelatedParty)
    assert isinstance(resource.resourceCharacteristic[0], Characteristic)
    assert isinstance(resource.resourceRelationship[0], ResourceRelationship)
    assert isinstance(resource.resourceRelationship[0].resource, ResourceRef)
    assert isinstance(resource.resourceSpecification, ResourceSpecificationRef)


def test_resource_ref_or_value_without_type_discriminator():
    order_item = ResourceOrderItem.from_dict(
        {"id": "item-9", "resource": {"id": "res-1", "name": "bare value"}}
    )
    assert isinstance(order_item.resource, ResourceRefOrValue)
    assert order_item.resource.name == "bare value"


def test_cancel_resource_order(cancel_resource_order_dict):
    cancel = CancelResourceOrder.from_dict(cancel_resource_order_dict)
    assert cancel.id == "cro-101"
    assert cancel.state is TaskStateType.DONE
    assert cancel.cancellationReason == "Customer withdrew the relocation request"
    assert isinstance(cancel.resourceOrder, ResourceOrderRef)
    assert cancel.resourceOrder.id == "ro-8801"
    assert cancel.resourceOrder._referred_type == "ResourceOrder"


def test_resource_order_list_fields_default_to_lists():
    order = ResourceOrder()
    assert order.orderItem == []
    assert order.note == []
    assert order.externalReference == []
    assert order.relatedParty == []


def test_resource_order_post_init_rejects_non_list():
    with pytest.raises(ValueError):
        ResourceOrder(orderItem=ResourceOrderItem(id="item-1"))


def test_resource_order_resource_path():
    context = Context(api_base_url="https://mycsp.com:8080/tmf-api")
    assert (
        ResourceOrder.get_resource_path(context)
        == "https://mycsp.com:8080/tmf-api/resourceOrderingManagement/v4/resourceOrder"
    )


def test_cancel_resource_order_resource_path():
    context = Context(api_base_url="https://mycsp.com:8080/tmf-api")
    assert (
        CancelResourceOrder.get_resource_path(context)
        == "https://mycsp.com:8080/tmf-api/resourceOrderingManagement/v4/cancelResourceOrder"
    )


def test_resource_order_to_dict_round_trip(resource_order_1):
    order_dict = resource_order_1.to_dict()
    assert order_dict["@type"] == "ResourceOrder"
    assert "@baseType" not in order_dict
    assert order_dict["priority"] == 2
    assert order_dict["externalReference"][0]["@type"] == "ExternalId"

    item_dict = order_dict["orderItem"][0]
    assert item_dict["@type"] == "ResourceOrderItem"
    assert item_dict["action"] == "add"

    resource_dict = item_dict["resource"]
    assert resource_dict["@type"] == "ResourceRefOrValue"
    assert resource_dict["@referredType"] == "LogicalResource"
    assert resource_dict["resourceStatus"] == "reserved"

    attachment_dict = resource_dict["attachment"][0]
    assert attachment_dict["@type"] == "AttachmentRefOrValue"
    assert attachment_dict["@baseType"] == "Attachment"
    assert attachment_dict["isRef"] is False

    relationship_dict = item_dict["orderItemRelationship"][0]
    assert relationship_dict["orderItem"]["@referredType"] == "ResourceOrderItem"

    assert ResourceOrder.from_dict(order_dict).to_dict() == order_dict


def test_cancel_resource_order_to_dict_round_trip(cancel_resource_order_dict):
    cancel = CancelResourceOrder.from_dict(cancel_resource_order_dict)
    cancel_dict = cancel.to_dict()
    assert cancel_dict["@type"] == "CancelResourceOrder"
    assert "@baseType" not in cancel_dict
    assert cancel_dict["state"] == "done"
    assert cancel_dict["resourceOrder"]["@type"] == "ResourceOrderRef"
    assert cancel_dict["resourceOrder"]["@referredType"] == "ResourceOrder"
