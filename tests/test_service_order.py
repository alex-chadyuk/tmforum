import pytest
from tmforum import (
    AppointmentRef,
    AttachmentRefOrValue,
    CancelServiceOrder,
    Characteristic,
    CharacteristicSpecification,
    ConstraintRef,
    Context,
    ContextUpdate,
    EntityRef,
    EntitySpecificationRef,
    EntitySpecificationRelationship,
    ExternalIdentifier,
    ExternalReference,
    Feature,
    JsonPatch,
    Note,
    OrderFailurePolicy,
    OrderItemSpecRelationship,
    OrderItemSpecification,
    OrderSequencingPolicy,
    OrderSpecification,
    ProcessFlowSpecificationRef,
    RelatedEntityRefOrValue,
    RelatedParty,
    RelatedPlaceRefOrValue,
    RelatedServiceOrderItem,
    ResourceRef,
    ServiceCategoryRef,
    ServiceOperatingStatusType,
    ServiceOrder,
    ServiceOrderErrorMessage,
    ServiceOrderItem,
    ServiceOrderItemActionType,
    ServiceOrderItemErrorMessage,
    ServiceOrderItemRef,
    ServiceOrderItemRelationship,
    ServiceOrderItemSpecification,
    ServiceOrderItemStateType,
    ServiceOrderJeopardyAlert,
    ServiceOrderMilestone,
    ServiceOrderRef,
    ServiceOrderRelationship,
    ServiceOrderSpecification,
    ServiceOrderStateType,
    ServiceRefOrValue,
    ServiceRelationship,
    ServiceSpecificationRef,
    ServiceStateType,
    TargetEntitySchema,
    TaskStateType,
    TimePeriod,
)


@pytest.fixture
def service_order_dict():
    return {
        "@type": "ServiceOrder",
        "id": "so-4411",
        "href": "https://mycsp.com/tmf-api/serviceOrdering/v4/serviceOrder/so-4411",
        "category": "Broadband",
        "description": "Activate fibre access for new subscriber",
        "externalId": "CRM-90218",
        "notificationContact": "noc@mycsp.com",
        "priority": "1",
        "state": "inProgress",
        "orderDate": "2026-04-02T08:00:00.000Z",
        "lastUpdate": "2026-04-02T11:45:00.000Z",
        "expectedCompletionDate": "2026-04-09T17:00:00.000Z",
        "requestedCompletionDate": "2026-04-10T17:00:00.000Z",
        "requestedStartDate": "2026-04-03T08:00:00.000Z",
        "startDate": "2026-04-03T08:30:00.000Z",
        "orderSpecification": {
            "@type": "EntitySpecificationRef",
            "id": "sos-77",
            "href": "https://mycsp.com/tmf-api/serviceOrdering/v4/serviceOrderSpecification/sos-77",
            "name": "Fibre activation order",
            "version": "3.0",
            "@referredType": "ServiceOrderSpecification",
        },
        "externalReference": [
            {
                "@type": "ExternalReference",
                "id": "WFM-3321",
                "href": "https://wfm.mycsp.com/tasks/WFM-3321",
                "externalReferenceType": "workOrder",
                "name": "Field dispatch",
            }
        ],
        "note": [
            {
                "@type": "Note",
                "id": "n-1",
                "author": "planner",
                "date": "2026-04-02T08:05:00.000Z",
                "text": "Duct survey already completed.",
            }
        ],
        "orderCharacteristic": [
            {
                "@type": "Characteristic",
                "id": "oc-1",
                "name": "salesChannel",
                "valueType": "String",
            }
        ],
        "orderRelationship": [
            {
                "@type": "ServiceOrderRelationship",
                "id": "so-4410",
                "href": "https://mycsp.com/tmf-api/serviceOrdering/v4/serviceOrder/so-4410",
                "relationshipType": "dependency",
            }
        ],
        "relatedParty": [
            {
                "@type": "RelatedParty",
                "id": "party-501",
                "name": "Aurora Media",
                "role": "customer",
            }
        ],
        "relatedEntity": [
            {
                "@type": "RelatedEntityRefOrValue",
                "role": "billingAccount",
                "entity": {"@type": "EntityRef", "id": "ba-77", "name": "Main account"},
            }
        ],
        "milestone": [
            {
                "@type": "ServiceOrderMilestone",
                "id": "ms-1",
                "name": "Design complete",
                "description": "Network design signed off",
                "message": "Design approved by planning",
                "milestoneDate": "2026-04-04T12:00:00.000Z",
                "status": "completed",
                "serviceOrderItem": [
                    {
                        "@type": "ServiceOrderItemRef",
                        "itemId": "item-1",
                        "serviceOrderId": "so-4411",
                        "@referredType": "ServiceOrderItem",
                    }
                ],
            }
        ],
        "jeopardyAlert": [
            {
                "@type": "ServiceOrderJeopardyAlert",
                "id": "ja-1",
                "name": "Civils delay",
                "alertDate": "2026-04-06T09:00:00.000Z",
                "exception": "PermitNotGranted",
                "jeopardyType": "Critical",
                "message": "Street works permit still pending",
                "serviceOrderItem": [
                    {
                        "@type": "ServiceOrderItemRef",
                        "itemId": "item-1",
                        "serviceOrderId": "so-4411",
                        "@referredType": "ServiceOrderItem",
                    }
                ],
            }
        ],
        "errorMessage": [
            {
                "@type": "ServiceOrderErrorMessage",
                "code": "503",
                "message": "Downstream inventory unavailable",
                "reason": "InventoryTimeout",
                "referenceError": "https://mycsp.com/errors/503",
                "status": "failed",
                "timestamp": "2026-04-05T14:20:00.000Z",
                "serviceOrderItem": [
                    {
                        "@type": "ServiceOrderItemRef",
                        "itemId": "item-1",
                        "serviceOrderId": "so-4411",
                        "@referredType": "ServiceOrderItem",
                    }
                ],
            }
        ],
        "serviceOrderItem": [
            {
                "@type": "ServiceOrderItem",
                "id": "item-1",
                "name": "Fibre access",
                "action": "add",
                "quantity": 1,
                "state": "inProgress",
                "appointment": {
                    "@type": "AppointmentRef",
                    "id": "appt-31",
                    "href": "https://mycsp.com/tmf-api/appointment/v4/appointment/appt-31",
                    "description": "Install window",
                },
                "orderItemCharacteristic": [
                    {
                        "@type": "Characteristic",
                        "id": "oic-1",
                        "name": "installType",
                        "valueType": "String",
                    }
                ],
                "relatedParty": [
                    {"@type": "RelatedParty", "id": "party-88", "role": "installer"}
                ],
                "modifyPath": [
                    {
                        "@type": "JsonPatch",
                        "op": "replace",
                        "path": "/serviceCharacteristic/0/value",
                        "value": 1000,
                    }
                ],
                "errorMessage": [
                    {
                        "@type": "ServiceOrderItemErrorMessage",
                        "code": "409",
                        "message": "Port already reserved",
                        "reason": "PortConflict",
                        "status": "held",
                        "timestamp": "2026-04-05T14:22:00.000Z",
                    }
                ],
                "serviceOrderItemRelationship": [
                    {
                        "@type": "ServiceOrderItemRelationship",
                        "relationshipType": "dependency",
                        "orderItem": {
                            "@type": "ServiceOrderItemRef",
                            "itemId": "item-2",
                            "serviceOrderId": "so-4412",
                            "serviceOrderHref": "https://mycsp.com/tmf-api/serviceOrdering/v4/serviceOrder/so-4412",
                            "@referredType": "ServiceOrderItem",
                        },
                    }
                ],
                "serviceOrderItem": [
                    {
                        "@type": "ServiceOrderItem",
                        "id": "item-1-a",
                        "action": "noChange",
                        "state": "acknowledged",
                    }
                ],
                "service": {
                    "@type": "ServiceRefOrValue",
                    "id": "svc-2201",
                    "href": "https://mycsp.com/tmf-api/serviceInventory/v5/service/svc-2201",
                    "name": "Fibre broadband 1G",
                    "category": "CFS",
                    "description": "Residential fibre access service",
                    "serviceType": "broadband",
                    "startMode": "automatic",
                    "serviceDate": "2026-04-09T00:00:00.000Z",
                    "startDate": "2026-04-09T09:00:00.000Z",
                    "endDate": "2027-04-09T09:00:00.000Z",
                    "hasStarted": False,
                    "isBundle": False,
                    "isServiceEnabled": True,
                    "isStateful": True,
                    "state": "designed",
                    "operatingStatus": "pending",
                    "@referredType": "CustomerFacingService",
                    "operatingStatusContextUpdate": {
                        "@type": "ContextUpdate",
                        "id": "ctx-1",
                        "lastUpdate": "2026-04-05T10:00:00.000Z",
                        "reason": "Awaiting field activation",
                        "relatedEntity": [
                            {"@type": "EntityRef", "id": "wo-9", "name": "Work order 9"}
                        ],
                        "relatedParty": [
                            {
                                "@type": "RelatedParty",
                                "id": "party-88",
                                "role": "installer",
                            }
                        ],
                    },
                    "serviceSpecification": {
                        "@type": "ServiceSpecificationRef",
                        "id": "ss-12",
                        "version": "2.0",
                    },
                    "externalIdentifier": [
                        {
                            "@type": "ExternalIdentifier",
                            "id": "ext-1",
                            "href": "https://legacy.mycsp.com/services/ext-1",
                            "externalIdentifierType": "legacyId",
                            "owner": "LegacyOSS",
                            "value": "L-88213",
                        }
                    ],
                    "feature": [
                        {
                            "@type": "Feature",
                            "id": "f-1",
                            "name": "staticIp",
                            "isEnabled": True,
                            "constraint": [
                                {
                                    "@type": "ConstraintRef",
                                    "id": "con-1",
                                    "name": "Max 4 addresses",
                                }
                            ],
                        }
                    ],
                    "note": [{"@type": "Note", "id": "n-2", "text": "Ported number."}],
                    "place": [
                        {
                            "@type": "RelatedPlaceRefOrValue",
                            "id": "place-9",
                            "name": "12 Harbour Lane",
                            "role": "installationSite",
                        }
                    ],
                    "relatedEntity": [
                        {
                            "@type": "RelatedEntityRefOrValue",
                            "role": "agreement",
                            "entity": {"@type": "EntityRef", "id": "agr-3"},
                        }
                    ],
                    "relatedParty": [
                        {"@type": "RelatedParty", "id": "party-501", "role": "customer"}
                    ],
                    "serviceCharacteristic": [
                        {
                            "@type": "Characteristic",
                            "id": "sc-1",
                            "name": "downstreamSpeed",
                            "valueType": "Integer",
                        }
                    ],
                    "serviceOrderItem": [
                        {
                            "@type": "RelatedServiceOrderItem",
                            "itemId": "item-1",
                            "serviceOrderId": "so-4411",
                            "role": "orderedBy",
                        }
                    ],
                    "serviceRelationship": [
                        {
                            "@type": "ServiceRelationship",
                            "relationshipType": "dependsOn",
                            "service": {"@type": "ServiceRef", "id": "svc-1000"},
                        }
                    ],
                    "supportingResource": [
                        {"@type": "ResourceRef", "id": "res-77", "name": "ONT"}
                    ],
                    "supportingService": [
                        {
                            "@type": "ServiceRefOrValue",
                            "id": "svc-2202",
                            "name": "Access RFS",
                            "category": "RFS",
                        }
                    ],
                },
            }
        ],
    }


@pytest.fixture
def service_order_1(service_order_dict):
    return ServiceOrder.from_dict(service_order_dict)


@pytest.fixture
def cancel_service_order_dict():
    return {
        "@type": "CancelServiceOrder",
        "id": "cso-77",
        "href": "https://mycsp.com/tmf-api/serviceOrdering/v4/cancelServiceOrder/cso-77",
        "cancellationReason": "Subscriber moved out of footprint",
        "completionMessage": "Cancelled before point of no return",
        "requestedCancellationDate": "2026-04-04T09:00:00.000Z",
        "effectiveCancellationDate": "2026-04-04T09:40:00.000Z",
        "state": "accepted",
        "errorMessage": {
            "@type": "ErrorMessage",
            "code": "200",
            "message": "Cancellation accepted",
            "reason": "CustomerRequest",
        },
        "serviceOrder": {
            "@type": "ServiceOrderRef",
            "id": "so-4411",
            "href": "https://mycsp.com/tmf-api/serviceOrdering/v4/serviceOrder/so-4411",
            "@referredType": "ServiceOrder",
        },
    }


@pytest.fixture
def service_order_specification_dict():
    return {
        "@type": "ServiceOrderSpecification",
        "id": "sos-77",
        "href": "https://mycsp.com/tmf-api/serviceOrdering/v4/serviceOrderSpecification/sos-77",
        "name": "Fibre activation order",
        "description": "Template for residential fibre activation orders",
        "version": "3.0",
        "lastUpdate": "2026-03-30T12:00:00.000Z",
        "lifecycleStatus": "Active",
        "isAutoResumeAllowed": True,
        "isAutoUnlockAllowed": False,
        "isBundle": False,
        "isSyncModeEnabled": True,
        "failurePolicy": "HaltAndRollback",
        "sequencingPolicy": "Sequential",
        "validFor": {
            "@type": "TimePeriod",
            "startDateTime": "2026-01-01T00:00:00.000Z",
            "endDateTime": "2027-01-01T00:00:00.000Z",
        },
        "targetEntitySchema": {
            "@type": "TargetEntitySchema",
            "@schemaLocation": "https://mycsp.com/schemas/ServiceOrder.json",
        },
        "workflow": {
            "@type": "ProcessFlowSpecificationRef",
            "id": "pfs-5",
            "name": "Fibre activation flow",
            "@referredType": "ProcessFlowSpecification",
        },
        "attachment": [
            {
                "@type": "AttachmentRefOrValue",
                "id": "att-2",
                "name": "runbook.pdf",
                "mimeType": "application/pdf",
                "url": "https://mycsp.com/files/runbook.pdf",
            }
        ],
        "constraint": [
            {"@type": "ConstraintRef", "id": "con-9", "name": "Footprint check"}
        ],
        "entitySpecRelationship": [
            {
                "@type": "EntitySpecificationRelationship",
                "id": "sos-76",
                "relationshipType": "substitution",
                "role": "predecessor",
            }
        ],
        "externalIdentifier": [
            {
                "@type": "ExternalIdentifier",
                "id": "ext-9",
                "externalIdentifierType": "catalogueId",
                "value": "CAT-3311",
            }
        ],
        "relatedParty": [
            {"@type": "RelatedParty", "id": "party-2", "role": "productManager"}
        ],
        "specCharacteristic": [
            {
                "@type": "CharacteristicSpecification",
                "id": "cs-1",
                "name": "installType",
                "valueType": "String",
            }
        ],
        "serviceOrderItemSpecification": [
            {
                "@type": "ServiceOrderItemSpecification",
                "id": "sois-1",
                "name": "Fibre access item",
                "description": "Access leg of the activation",
                "actionType": "add",
                "otherAction": "reactivate",
                "serviceCategory": {"@type": "ServiceCategoryRef", "id": "scat-1"},
                "serviceSpecification": {
                    "@type": "ServiceSpecificationRef",
                    "id": "ss-12",
                },
                "attachment": [
                    {"@type": "AttachmentRefOrValue", "id": "att-3", "name": "spec.pdf"}
                ],
                "constraint": [{"@type": "ConstraintRef", "id": "con-10"}],
                "specCharacteristic": [
                    {
                        "@type": "CharacteristicSpecification",
                        "id": "cs-2",
                        "name": "bandwidth",
                    }
                ],
                "orderItemSpecRelationship": [
                    {
                        "@type": "OrderItemSpecRelationship",
                        "orderItemSpecificationId": "sois-2",
                        "parentOrderSpecificationId": "sos-77",
                        "parentOrderSpecificationHref": "https://mycsp.com/tmf-api/serviceOrdering/v4/serviceOrderSpecification/sos-77",
                        "relationshipType": "dependency",
                    }
                ],
            }
        ],
    }


def test_service_order_instantiates_with_scalars(service_order_1):
    assert service_order_1.id == "so-4411"
    assert service_order_1.externalId == "CRM-90218"
    assert service_order_1.category == "Broadband"
    assert service_order_1.notificationContact == "noc@mycsp.com"
    assert service_order_1.priority == "1"
    assert service_order_1.state is ServiceOrderStateType.IN_PROGRESS
    assert service_order_1.completionDate is None
    assert service_order_1.cancellationReason is None


def test_service_order_instantiates_classes(service_order_1):
    assert isinstance(service_order_1.orderSpecification, EntitySpecificationRef)
    assert service_order_1.orderSpecification.version == "3.0"
    assert (
        service_order_1.orderSpecification._referred_type == "ServiceOrderSpecification"
    )
    assert isinstance(service_order_1.externalReference[0], ExternalReference)
    assert service_order_1.externalReference[0].externalReferenceType == "workOrder"
    assert isinstance(service_order_1.note[0], Note)
    assert isinstance(service_order_1.orderCharacteristic[0], Characteristic)
    assert isinstance(service_order_1.orderRelationship[0], ServiceOrderRelationship)
    assert service_order_1.orderRelationship[0].relationshipType == "dependency"
    assert isinstance(service_order_1.relatedParty[0], RelatedParty)
    assert isinstance(service_order_1.relatedEntity[0], RelatedEntityRefOrValue)
    assert isinstance(service_order_1.relatedEntity[0].entity, EntityRef)


def test_service_order_milestone_jeopardy_and_error(service_order_1):
    milestone = service_order_1.milestone[0]
    assert isinstance(milestone, ServiceOrderMilestone)
    assert milestone.name == "Design complete"
    assert milestone.status == "completed"
    assert isinstance(milestone.serviceOrderItem[0], ServiceOrderItemRef)
    assert milestone.serviceOrderItem[0].itemId == "item-1"

    alert = service_order_1.jeopardyAlert[0]
    assert isinstance(alert, ServiceOrderJeopardyAlert)
    assert alert.jeopardyType == "Critical"
    assert isinstance(alert.serviceOrderItem[0], ServiceOrderItemRef)

    error = service_order_1.errorMessage[0]
    assert isinstance(error, ServiceOrderErrorMessage)
    assert error.code == "503"
    assert error.status == "failed"
    assert error.timestamp == "2026-04-05T14:20:00.000Z"
    assert isinstance(error.serviceOrderItem[0], ServiceOrderItemRef)


def test_service_order_item_nested_classes(service_order_1):
    item = service_order_1.serviceOrderItem[0]
    assert isinstance(item, ServiceOrderItem)
    assert item.action is ServiceOrderItemActionType.ADD
    assert item.state is ServiceOrderItemStateType.IN_PROGRESS
    assert item.quantity == 1
    assert isinstance(item.appointment, AppointmentRef)
    assert isinstance(item.orderItemCharacteristic[0], Characteristic)
    assert isinstance(item.relatedParty[0], RelatedParty)
    assert isinstance(item.modifyPath[0], JsonPatch)
    assert item.modifyPath[0].op == "replace"
    assert item.modifyPath[0].value == 1000
    assert isinstance(item.errorMessage[0], ServiceOrderItemErrorMessage)
    assert item.errorMessage[0].timestamp == "2026-04-05T14:22:00.000Z"

    relationship = item.serviceOrderItemRelationship[0]
    assert isinstance(relationship, ServiceOrderItemRelationship)
    assert isinstance(relationship.orderItem, ServiceOrderItemRef)
    assert relationship.orderItem.serviceOrderId == "so-4412"

    nested = item.serviceOrderItem[0]
    assert isinstance(nested, ServiceOrderItem)
    assert nested.action is ServiceOrderItemActionType.NO_CHANGE


def test_service_ref_or_value_nested_classes(service_order_1):
    service = service_order_1.serviceOrderItem[0].service
    assert isinstance(service, ServiceRefOrValue)
    assert service.id == "svc-2201"
    assert service.isServiceEnabled is True
    assert service.hasStarted is False
    assert service.state is ServiceStateType.DESIGNED
    assert service.operatingStatus is ServiceOperatingStatusType.PENDING
    assert service._referred_type == "CustomerFacingService"

    context_update = service.operatingStatusContextUpdate
    assert isinstance(context_update, ContextUpdate)
    assert context_update.reason == "Awaiting field activation"
    assert isinstance(context_update.relatedEntity[0], EntityRef)
    assert isinstance(context_update.relatedParty[0], RelatedParty)

    assert isinstance(service.serviceSpecification, ServiceSpecificationRef)
    assert isinstance(service.externalIdentifier[0], ExternalIdentifier)
    assert (
        service.externalIdentifier[0].href == "https://legacy.mycsp.com/services/ext-1"
    )
    assert isinstance(service.feature[0], Feature)
    assert isinstance(service.feature[0].constraint[0], ConstraintRef)
    assert isinstance(service.note[0], Note)
    assert isinstance(service.place[0], RelatedPlaceRefOrValue)
    assert isinstance(service.relatedEntity[0], RelatedEntityRefOrValue)
    assert isinstance(service.relatedParty[0], RelatedParty)
    assert isinstance(service.serviceCharacteristic[0], Characteristic)
    assert isinstance(service.serviceOrderItem[0], RelatedServiceOrderItem)
    assert isinstance(service.serviceRelationship[0], ServiceRelationship)
    assert isinstance(service.supportingResource[0], ResourceRef)
    assert isinstance(service.supportingService[0], ServiceRefOrValue)
    assert service.supportingService[0].category == "RFS"


def test_service_ref_or_value_without_type_discriminator():
    item = ServiceOrderItem.from_dict(
        {"id": "item-9", "service": {"id": "svc-1", "name": "bare value"}}
    )
    assert isinstance(item.service, ServiceRefOrValue)
    assert item.service.name == "bare value"


def test_service_order_specification(service_order_specification_dict):
    spec = ServiceOrderSpecification.from_dict(service_order_specification_dict)
    assert isinstance(spec, OrderSpecification)
    assert spec.id == "sos-77"
    assert spec.version == "3.0"
    assert spec.lifecycleStatus == "Active"
    assert spec.isAutoResumeAllowed is True
    assert spec.isAutoUnlockAllowed is False
    assert spec.isSyncModeEnabled is True
    assert spec.failurePolicy is OrderFailurePolicy.HALT_AND_ROLLBACK
    assert spec.sequencingPolicy is OrderSequencingPolicy.SEQUENTIAL
    assert isinstance(spec.validFor, TimePeriod)
    assert isinstance(spec.targetEntitySchema, TargetEntitySchema)
    assert isinstance(spec.workflow, ProcessFlowSpecificationRef)
    assert isinstance(spec.attachment[0], AttachmentRefOrValue)
    assert isinstance(spec.constraint[0], ConstraintRef)
    assert isinstance(spec.entitySpecRelationship[0], EntitySpecificationRelationship)
    assert isinstance(spec.externalIdentifier[0], ExternalIdentifier)
    assert isinstance(spec.relatedParty[0], RelatedParty)
    assert isinstance(spec.specCharacteristic[0], CharacteristicSpecification)

    item_spec = spec.serviceOrderItemSpecification[0]
    assert isinstance(item_spec, ServiceOrderItemSpecification)
    assert isinstance(item_spec, OrderItemSpecification)
    assert item_spec.actionType is ServiceOrderItemActionType.ADD
    assert item_spec.otherAction == "reactivate"
    assert isinstance(item_spec.serviceCategory, ServiceCategoryRef)
    assert isinstance(item_spec.serviceSpecification, ServiceSpecificationRef)
    assert isinstance(item_spec.attachment[0], AttachmentRefOrValue)
    assert isinstance(item_spec.constraint[0], ConstraintRef)
    assert isinstance(item_spec.specCharacteristic[0], CharacteristicSpecification)
    assert isinstance(item_spec.orderItemSpecRelationship[0], OrderItemSpecRelationship)
    assert item_spec.orderItemSpecRelationship[0].parentOrderSpecificationId == "sos-77"


def test_cancel_service_order(cancel_service_order_dict):
    cancel = CancelServiceOrder.from_dict(cancel_service_order_dict)
    assert cancel.id == "cso-77"
    assert cancel.state is TaskStateType.ACCEPTED
    assert cancel.completionMessage == "Cancelled before point of no return"
    assert cancel.errorMessage.code == "200"
    assert isinstance(cancel.serviceOrder, ServiceOrderRef)
    assert cancel.serviceOrder.id == "so-4411"
    assert cancel.serviceOrder._referred_type == "ServiceOrder"


def test_service_order_list_fields_default_to_lists():
    order = ServiceOrder()
    assert order.serviceOrderItem == []
    assert order.note == []
    assert order.milestone == []
    assert order.jeopardyAlert == []
    assert order.errorMessage == []
    assert order.externalReference == []
    assert order.relatedParty == []


def test_service_order_post_init_rejects_non_list():
    with pytest.raises(ValueError):
        ServiceOrder(serviceOrderItem=ServiceOrderItem(id="item-1"))


def test_service_order_item_post_init_rejects_non_list():
    with pytest.raises(ValueError):
        ServiceOrderItem(modifyPath=JsonPatch(op="add"))


def test_service_order_resource_path():
    context = Context(api_base_url="https://mycsp.com:8080/tmf-api")
    assert (
        ServiceOrder.get_resource_path(context)
        == "https://mycsp.com:8080/tmf-api/serviceOrdering/v4/serviceOrder"
    )


def test_cancel_service_order_resource_path():
    context = Context(api_base_url="https://mycsp.com:8080/tmf-api")
    assert (
        CancelServiceOrder.get_resource_path(context)
        == "https://mycsp.com:8080/tmf-api/serviceOrdering/v4/cancelServiceOrder"
    )


def test_service_order_specification_resource_path():
    context = Context(api_base_url="https://mycsp.com:8080/tmf-api")
    assert (
        ServiceOrderSpecification.get_resource_path(context)
        == "https://mycsp.com:8080/tmf-api/serviceOrdering/v4/serviceOrderSpecification"
    )


def test_service_order_to_dict_round_trip(service_order_1):
    order_dict = service_order_1.to_dict()
    assert order_dict["@type"] == "ServiceOrder"
    assert "@baseType" not in order_dict
    assert order_dict["state"] == "inProgress"
    assert (
        order_dict["orderSpecification"]["@referredType"] == "ServiceOrderSpecification"
    )

    milestone_dict = order_dict["milestone"][0]
    assert milestone_dict["@type"] == "ServiceOrderMilestone"
    assert milestone_dict["@baseType"] == "Milestone"

    alert_dict = order_dict["jeopardyAlert"][0]
    assert alert_dict["@type"] == "ServiceOrderJeopardyAlert"
    assert alert_dict["@baseType"] == "JeopardyAlert"

    error_dict = order_dict["errorMessage"][0]
    assert error_dict["@type"] == "ServiceOrderErrorMessage"
    assert error_dict["@baseType"] == "ErrorMessage"

    item_dict = order_dict["serviceOrderItem"][0]
    assert item_dict["@type"] == "ServiceOrderItem"
    assert item_dict["action"] == "add"
    assert item_dict["modifyPath"][0]["value"] == 1000
    assert item_dict["errorMessage"][0]["@baseType"] == "ErrorMessage"
    assert (
        item_dict["serviceOrderItemRelationship"][0]["orderItem"]["@referredType"]
        == "ServiceOrderItem"
    )

    service_dict = item_dict["service"]
    assert service_dict["@type"] == "ServiceRefOrValue"
    assert service_dict["@referredType"] == "CustomerFacingService"
    assert service_dict["operatingStatus"] == "pending"
    assert service_dict["operatingStatusContextUpdate"]["@type"] == "ContextUpdate"
    assert service_dict["externalIdentifier"][0]["href"] == (
        "https://legacy.mycsp.com/services/ext-1"
    )
    assert service_dict["feature"][0]["constraint"][0]["@type"] == "ConstraintRef"
    assert service_dict["supportingService"][0]["@type"] == "ServiceRefOrValue"

    assert ServiceOrder.from_dict(order_dict).to_dict() == order_dict


def test_service_order_specification_to_dict_round_trip(
    service_order_specification_dict,
):
    spec_dict = ServiceOrderSpecification.from_dict(
        service_order_specification_dict
    ).to_dict()
    assert spec_dict["@type"] == "ServiceOrderSpecification"
    assert spec_dict["@baseType"] == "OrderSpecification"
    assert spec_dict["failurePolicy"] == "HaltAndRollback"
    assert spec_dict["sequencingPolicy"] == "Sequential"
    assert spec_dict["workflow"]["@referredType"] == "ProcessFlowSpecification"

    item_spec_dict = spec_dict["serviceOrderItemSpecification"][0]
    assert item_spec_dict["@type"] == "ServiceOrderItemSpecification"
    assert item_spec_dict["@baseType"] == "OrderItemSpecification"
    assert item_spec_dict["actionType"] == "add"

    assert ServiceOrderSpecification.from_dict(spec_dict).to_dict() == spec_dict


def test_cancel_service_order_to_dict_round_trip(cancel_service_order_dict):
    cancel_dict = CancelServiceOrder.from_dict(cancel_service_order_dict).to_dict()
    assert cancel_dict["@type"] == "CancelServiceOrder"
    assert "@baseType" not in cancel_dict
    assert cancel_dict["state"] == "accepted"
    assert cancel_dict["errorMessage"]["@type"] == "ErrorMessage"
    assert cancel_dict["serviceOrder"]["@referredType"] == "ServiceOrder"

    assert CancelServiceOrder.from_dict(cancel_dict).to_dict() == cancel_dict
