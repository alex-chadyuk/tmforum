import pytest
from tmforum import (
    Attachment,
    AttachmentRef,
    BooleanArrayCharacteristicValueSpecification,
    BooleanCharacteristicValueSpecification,
    ChannelRef,
    CharacteristicSpecification,
    CharacteristicValueSpecification,
    EntityRef,
    ExternalIdentifier,
    FlowCharacteristic,
    FlowCharacteristicSpecification,
    FlowStateType,
    ObjectCharacteristic,
    PartyRef,
    PolicyRef,
    Process,
    ProcessRef,
    ProcessRelationship,
    ProcessSpecification,
    ProcessSpecificationRef,
    ProcessSpecificationRelationship,
    RelatedEntity,
    RelatedPartyRefOrPartyRoleRef,
    RelatedProcess,
    RelatedProcessSpecification,
    StringCharacteristic,
    Task,
    TaskRef,
    TaskRelationship,
    TaskSpecification,
    TaskSpecificationRef,
    TaskSpecificationRelationship,
    TimePeriod,
)

BASE = "https://www.mycsp.com/tmfapis/processManagement/v5"


@pytest.fixture
def related_party_dict():
    return {
        "@type": "RelatedPartyRefOrPartyRoleRef",
        "role": "Customer",
        "partyOrPartyRole": {
            "@type": "PartyRef",
            "id": "456-f69",
            "href": "https://www.mycsp.com/tmfapis/partyManagement/v5/individual/456-f69",
            "name": "Jean Pontus",
            "@referredType": "Individual",
        },
    }


@pytest.fixture
def process_dict(related_party_dict):
    return {
        "@type": "Process",
        "id": "4fd-ty56-gg55",
        "href": f"{BASE}/process/4fd-ty56-gg55",
        "name": "Order capture for Jean Pontus",
        "description": "Order capture through the web store",
        "creationDate": "2024-04-11T14:52:21.823Z",
        "requestedStartDate": "2024-04-11T15:00:00.000Z",
        "startDate": "2024-04-11T15:00:02.000Z",
        "requestedCompletionDate": "2024-04-12T15:00:00.000Z",
        "completionDate": "2024-04-11T16:10:00.000Z",
        "state": "completed",
        "channel": {
            "@type": "ChannelRef",
            "id": "1",
            "href": "https://www.mycsp.com/tmfapis/channel/1",
            "name": "TMFWebStore",
            "@referredType": "Channel",
        },
        "processSpecification": {
            "@type": "ProcessSpecificationRef",
            "id": "OC54",
            "href": f"{BASE}/processSpecification/OC54",
            "name": "orderCapture",
            "version": "1",
            "@referredType": "ProcessSpecification",
        },
        "externalIdentifier": {
            "@type": "ExternalIdentifier",
            "id": "BPM-7781",
            "owner": "Camunda",
            "externalIdentifierType": "processInstanceId",
        },
        "relatedParty": [related_party_dict],
        "processCharacteristic": [
            {
                "@type": "FlowCharacteristic",
                "modality": "input",
                "isPopulated": True,
                "characteristic": {
                    "@type": "ObjectCharacteristic",
                    "valueType": "object",
                    "name": "Offer name",
                    "value": {"name": "productOfferingRef", "id": "TMFMobile20"},
                },
            }
        ],
        "processRelationship": [
            {
                "@type": "ProcessRelationship",
                "relationshipType": "triggeredBy",
                "process": {
                    "@type": "ProcessRef",
                    "id": "4fd-ty56-gg50",
                    "href": f"{BASE}/process/4fd-ty56-gg50",
                    "@referredType": "Process",
                },
            }
        ],
        "task": [
            {
                "@type": "TaskRef",
                "id": "4fd-ty56-gg55-2",
                "href": f"{BASE}/task/4fd-ty56-gg55-2",
                "@referredType": "Task",
            },
            {
                "@type": "Task",
                "id": "4fd-ty56-gg55-3",
                "name": "Initialize ShoppingCart",
                "state": "active",
                "taskCharacteristic": [
                    {
                        "@type": "FlowCharacteristic",
                        "modality": "output",
                        "characteristic": {
                            "@type": "StringCharacteristic",
                            "name": "Eligibility result",
                            "value": "Qualified",
                        },
                    }
                ],
            },
        ],
        "relatedEntity": [
            {
                "@type": "RelatedEntity",
                "role": "created shopping Cart",
                "entity": {
                    "@type": "EntityRef",
                    "id": "1203",
                    "href": "https://www.mycsp.com/tmfapis/shoppingCartManagement/v5/shoppingCart/1203",
                    "@referredType": "ShoppingCart",
                },
            }
        ],
    }


@pytest.fixture
def process_1(process_dict):
    return Process.from_dict(process_dict)


@pytest.fixture
def task_dict(related_party_dict):
    return {
        "@type": "Task",
        "@schemaLocation": "https://www.mycsp.com/tmfapis/schemas/task.json",
        "id": "4fd-ty56-gg55-3",
        "href": f"{BASE}/task/4fd-ty56-gg55-3",
        "name": "Initialize ShoppingCart",
        "description": "Create the shopping cart for the captured offer",
        "isMandatory": True,
        "priority": 2,
        "state": "active",
        "taskType": "businessRuleTask",
        "startDate": "2024-04-11T15:01:00.000Z",
        "completionDate": "2024-04-11T15:02:00.000Z",
        "channel": {"@type": "ChannelRef", "id": "1", "@referredType": "Channel"},
        "taskSpecification": {
            "@type": "TaskSpecificationRef",
            "id": "tfs1",
            "href": f"{BASE}/taskSpecification/tfs1",
            "name": "Initialize ShoppingCart",
            "version": "1",
            "@referredType": "TaskSpecification",
        },
        "parentProcess": {
            "@type": "ProcessRef",
            "id": "4fd-ty56-gg55",
            "href": f"{BASE}/process/4fd-ty56-gg55",
            "@referredType": "Process",
        },
        "taskRelationship": [
            {
                "@type": "TaskRelationship",
                "id": "4fd-ty56-gg55-4",
                "href": f"{BASE}/task/4fd-ty56-gg55-4",
                "relationshipType": "triggers",
                "@referredType": "Task",
            }
        ],
        "relatedProcess": [
            {
                "@type": "RelatedProcess",
                "role": "compensation",
                "process": {
                    "@type": "ProcessRef",
                    "id": "4fd-ty56-gg60",
                    "@referredType": "Process",
                },
            }
        ],
        "relatedEntity": [
            {
                "@type": "RelatedEntity",
                "role": "shopping cart",
                "entity": {
                    "@type": "EntityRef",
                    "id": "1203",
                    "@referredType": "ShoppingCart",
                },
            }
        ],
        "relatedParty": [related_party_dict],
        "taskCharacteristic": [
            {
                "@type": "FlowCharacteristic",
                "modality": "input",
                "characteristic": {
                    "@type": "StringCharacteristic",
                    "valueType": "string",
                    "name": "Eligibility result",
                    "value": "Qualified",
                },
            }
        ],
    }


@pytest.fixture
def process_specification_dict():
    return {
        "@type": "ProcessSpecification",
        "id": "OC54",
        "href": f"{BASE}/processSpecification/OC54",
        "lifecycleStatus": "onDesign",
        "version": "1",
        "lastUpdate": "2023-12-30T09:42:25.747Z",
        "name": "orderCapture",
        "description": "Description of the order capture process for all channels",
        "validFor": {"startDateTime": "2024-01-01T00:00:00.000Z"},
        "channel": [{"@type": "ChannelRef", "id": "1", "@referredType": "Channel"}],
        "attachment": [
            {
                "@type": "Attachment",
                "attachmentType": "TaskDocumentation",
                "mimeType": "application/pdf",
                "name": "pfs-1-doc",
                "url": "https://mycsp.com/content/4aafacbd-11ff-4dc8-b445-305f2215715f",
                "size": {"amount": 2423, "units": "Mb"},
            },
            {"@type": "AttachmentRef", "id": "att-2", "@referredType": "Attachment"},
        ],
        "processSpecificationCharacteristic": [
            {
                "@type": "FlowCharacteristicSpecification",
                "modality": "input",
                "characteristicSpecification": {
                    "@type": "CharacteristicSpecification",
                    "configurable": True,
                    "maxCardinality": 1,
                    "minCardinality": 0,
                    "valueType": "boolean",
                    "name": "expressDelivery",
                    "characteristicValueSpecification": [
                        {
                            "@type": "BooleanCharacteristicValueSpecification",
                            "valueType": "boolean",
                            "isDefault": True,
                            "value": False,
                        }
                    ],
                },
            }
        ],
        "processSpecificationPolicy": [
            {
                "@type": "PolicyRef",
                "id": "pol-7",
                "version": "2",
                "@referredType": "Policy",
            }
        ],
        "processSpecificationRelationship": [
            {
                "@type": "ProcessSpecificationRelationship",
                "relationshipType": "dependsOn",
                "processSpecification": {
                    "@type": "ProcessSpecificationRef",
                    "id": "CR01",
                    "version": "3",
                    "@referredType": "ProcessSpecification",
                },
            }
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "role": "designer",
                "partyOrPartyRole": {
                    "@type": "PartyRef",
                    "id": "4cf-mg1",
                    "name": "Simon Clement",
                    "@referredType": "Individual",
                },
            }
        ],
        "taskSpecification": [
            {
                "@type": "TaskSpecificationRef",
                "id": "tfs0",
                "href": f"{BASE}/taskSpecification/tfs0",
                "@referredType": "TaskSpecification",
            },
            {
                "@type": "TaskSpecificationRef",
                "id": "tfs1",
                "href": f"{BASE}/taskSpecification/tfs1",
                "@referredType": "TaskSpecification",
            },
        ],
    }


@pytest.fixture
def task_specification_dict():
    return {
        "@type": "TaskSpecification",
        "@schemaLocation": "https://www.mycsp.com/tmfapis/schemas/taskSpecification.json",
        "id": "tfs0",
        "href": f"{BASE}/taskSpecification/tfs0",
        "description": "Check Offer Eligibility",
        "lastUpdate": "2024-04-30T13:03:57.839Z",
        "lifecycleStatus": "active",
        "name": "Eligibility Check",
        "taskType": "businessRuleTask",
        "version": "1",
        "validFor": {"startDateTime": "2024-12-30T13:03:57.839Z"},
        "channel": [{"@type": "ChannelRef", "id": "1", "@referredType": "Channel"}],
        "attachment": [
            {
                "@type": "Attachment",
                "attachmentType": "TaskDocumentation",
                "mimeType": "application/pdf",
                "name": "tfs-2-doc",
                "size": {"amount": 2105, "units": "Mb"},
            }
        ],
        "taskSpecificationCharacteristic": [
            {
                "@type": "FlowCharacteristicSpecification",
                "modality": "output",
                "characteristicSpecification": {
                    "@type": "CharacteristicSpecification",
                    "configurable": True,
                    "maxCardinality": 1,
                    "minCardinality": 1,
                    "name": "qualification result",
                    "valueType": "string",
                },
            }
        ],
        "taskSpecificationRelationship": [
            {
                "@type": "TaskSpecificationRelationship",
                "relationshipType": "nextTask",
                "taskSpecification": {
                    "@type": "TaskSpecificationRef",
                    "id": "tfs1",
                    "href": f"{BASE}/taskSpecification/tfs1",
                    "name": "Initialize ShoppingCart",
                    "@referredType": "TaskSpecification",
                },
            }
        ],
        "relatedProcessSpecification": [
            {
                "@type": "RelatedProcessSpecification",
                "role": "usedBy",
                "processSpecification": {
                    "@type": "ProcessSpecificationRef",
                    "id": "OC54",
                    "version": "1",
                    "@referredType": "ProcessSpecification",
                },
            }
        ],
        "taskSpecificationPolicy": [
            {"@type": "PolicyRef", "id": "pol-9", "@referredType": "Policy"}
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "role": "approver",
                "partyOrPartyRole": {
                    "@type": "PartyRef",
                    "id": "fp5-559",
                    "name": "Kate Noman",
                    "@referredType": "Individual",
                },
            }
        ],
    }


def test_process_instantiates_with_id(process_1):
    assert isinstance(process_1, Process)
    assert process_1.id == "4fd-ty56-gg55"
    assert process_1.name == "Order capture for Jean Pontus"
    assert process_1.state is FlowStateType.COMPLETED
    assert process_1.creationDate == "2024-04-11T14:52:21.823Z"
    assert process_1.requestedStartDate == "2024-04-11T15:00:00.000Z"
    assert process_1.requestedCompletionDate == "2024-04-12T15:00:00.000Z"


def test_process_instantiates_classes(process_1):
    assert isinstance(process_1.channel, ChannelRef)
    assert process_1.channel._referred_type == "Channel"

    assert isinstance(process_1.processSpecification, ProcessSpecificationRef)
    assert process_1.processSpecification.version == "1"
    assert process_1.processSpecification._referred_type == "ProcessSpecification"

    related_party = process_1.relatedParty[0]
    assert isinstance(related_party, RelatedPartyRefOrPartyRoleRef)
    assert isinstance(related_party.partyOrPartyRole, PartyRef)

    process_characteristic = process_1.processCharacteristic[0]
    assert isinstance(process_characteristic, FlowCharacteristic)
    assert process_characteristic.modality == "input"
    assert process_characteristic.isPopulated is True
    assert isinstance(process_characteristic.characteristic, ObjectCharacteristic)
    assert process_characteristic.characteristic.name == "Offer name"

    relationship = process_1.processRelationship[0]
    assert isinstance(relationship, ProcessRelationship)
    assert relationship.relationshipType == "triggeredBy"
    assert isinstance(relationship.process, ProcessRef)
    assert relationship.process._referred_type == "Process"

    related_entity = process_1.relatedEntity[0]
    assert isinstance(related_entity, RelatedEntity)
    assert isinstance(related_entity.entity, EntityRef)
    assert related_entity.entity._referred_type == "ShoppingCart"


def test_process_task_resolves_ref_or_value(process_1):
    task_ref, task = process_1.task

    assert isinstance(task_ref, TaskRef)
    assert task_ref._referred_type == "Task"

    assert isinstance(task, Task)
    assert task.state is FlowStateType.ACTIVE
    assert isinstance(task.taskCharacteristic[0], FlowCharacteristic)
    assert isinstance(task.taskCharacteristic[0].characteristic, StringCharacteristic)


def test_process_external_identifier_is_single_object(process_1):
    assert isinstance(process_1.externalIdentifier, ExternalIdentifier)
    assert process_1.externalIdentifier.owner == "Camunda"

    result = process_1.to_dict()["externalIdentifier"]
    assert result["@type"] == "ExternalIdentifier"
    assert result["externalIdentifierType"] == "processInstanceId"


def test_process_defaults_to_empty_lists():
    process = Process.from_dict({"@type": "Process", "id": "4fd-ty56-gg55"})

    assert process.state is None
    assert process.externalIdentifier is None
    assert process.processCharacteristic == []
    assert process.processRelationship == []
    assert process.task == []
    assert process.relatedEntity == []
    assert process.relatedParty == []


def test_process_rejects_non_list_task():
    with pytest.raises(ValueError):
        Process(task=TaskRef(id="4fd-ty56-gg55-2"))


def test_process_to_dict_round_trip(process_dict):
    result = Process.from_dict(process_dict).to_dict()

    assert result["@type"] == "Process"
    assert "@baseType" not in result
    assert result["state"] == "completed"
    assert result["completionDate"] == "2024-04-11T16:10:00.000Z"
    assert result["channel"]["@referredType"] == "Channel"
    assert result["processSpecification"]["@type"] == "ProcessSpecificationRef"
    assert result["processSpecification"]["version"] == "1"
    assert result["processCharacteristic"][0]["@type"] == "FlowCharacteristic"
    assert (
        result["processCharacteristic"][0]["characteristic"]["@baseType"]
        == "Characteristic"
    )
    assert result["processRelationship"][0]["process"]["@referredType"] == "Process"
    assert result["task"][0]["@type"] == "TaskRef"
    assert result["task"][0]["@referredType"] == "Task"
    assert result["task"][1]["@type"] == "Task"
    assert result["task"][1]["state"] == "active"
    assert result["relatedEntity"][0]["entity"]["@referredType"] == "ShoppingCart"
    assert result["relatedParty"][0]["partyOrPartyRole"]["@type"] == "PartyRef"


def test_task_instantiates_classes(task_dict):
    task = Task.from_dict(task_dict)

    assert task.id == "4fd-ty56-gg55-3"
    assert task.isMandatory is True
    assert task.priority == 2
    assert task.taskType == "businessRuleTask"
    assert task.state is FlowStateType.ACTIVE
    assert isinstance(task.channel, ChannelRef)

    assert isinstance(task.taskSpecification, TaskSpecificationRef)
    assert task.taskSpecification.version == "1"
    assert task.taskSpecification._referred_type == "TaskSpecification"

    assert isinstance(task.parentProcess, ProcessRef)
    assert task.parentProcess.id == "4fd-ty56-gg55"

    relationship = task.taskRelationship[0]
    assert isinstance(relationship, TaskRelationship)
    assert relationship.relationshipType == "triggers"
    assert relationship._referred_type == "Task"

    related_process = task.relatedProcess[0]
    assert isinstance(related_process, RelatedProcess)
    assert related_process.role == "compensation"
    assert isinstance(related_process.process, ProcessRef)

    assert isinstance(task.relatedEntity[0], RelatedEntity)
    assert isinstance(task.relatedParty[0].partyOrPartyRole, PartyRef)

    characteristic = task.taskCharacteristic[0]
    assert isinstance(characteristic, FlowCharacteristic)
    assert isinstance(characteristic.characteristic, StringCharacteristic)
    assert characteristic.characteristic.value == "Qualified"


def test_task_relationship_defaults_referred_type():
    result = TaskRelationship(
        id="4fd-ty56-gg55-4", relationshipType="requires"
    ).to_dict()

    assert result["@type"] == "TaskRelationship"
    assert "@baseType" not in result
    assert result["@referredType"] == "Task"
    assert result["relationshipType"] == "requires"


def test_task_to_dict_round_trip(task_dict):
    result = Task.from_dict(task_dict).to_dict()

    assert result["@type"] == "Task"
    assert "@baseType" not in result
    assert result["state"] == "active"
    assert result["priority"] == 2
    assert result["isMandatory"] is True
    assert result["taskSpecification"]["@referredType"] == "TaskSpecification"
    assert result["parentProcess"]["@type"] == "ProcessRef"
    assert result["taskRelationship"][0]["@type"] == "TaskRelationship"
    assert result["taskRelationship"][0]["@referredType"] == "Task"
    assert result["relatedProcess"][0]["@type"] == "RelatedProcess"
    assert result["relatedProcess"][0]["process"]["@referredType"] == "Process"
    assert (
        result["taskCharacteristic"][0]["characteristic"]["@type"]
        == "StringCharacteristic"
    )


def test_process_specification_instantiates_classes(process_specification_dict):
    spec = ProcessSpecification.from_dict(process_specification_dict)

    assert spec.id == "OC54"
    assert spec.lifecycleStatus == "onDesign"
    assert spec.version == "1"
    assert isinstance(spec.validFor, TimePeriod)
    assert isinstance(spec.channel[0], ChannelRef)

    attachment, attachment_ref = spec.attachment
    assert isinstance(attachment, Attachment)
    assert attachment.mimeType == "application/pdf"
    assert isinstance(attachment_ref, AttachmentRef)

    flow_char_spec = spec.processSpecificationCharacteristic[0]
    assert isinstance(flow_char_spec, FlowCharacteristicSpecification)
    assert flow_char_spec.modality == "input"
    char_spec = flow_char_spec.characteristicSpecification
    assert isinstance(char_spec, CharacteristicSpecification)
    assert char_spec.name == "expressDelivery"
    value_spec = char_spec.characteristicValueSpecification[0]
    assert isinstance(value_spec, BooleanCharacteristicValueSpecification)
    assert value_spec.value is False

    assert isinstance(spec.processSpecificationPolicy[0], PolicyRef)
    assert spec.processSpecificationPolicy[0].version == "2"

    relationship = spec.processSpecificationRelationship[0]
    assert isinstance(relationship, ProcessSpecificationRelationship)
    assert relationship.relationshipType == "dependsOn"
    assert isinstance(relationship.processSpecification, ProcessSpecificationRef)
    assert relationship.processSpecification.version == "3"

    assert isinstance(spec.relatedParty[0].partyOrPartyRole, PartyRef)
    assert [t.id for t in spec.taskSpecification] == ["tfs0", "tfs1"]
    assert all(isinstance(t, TaskSpecificationRef) for t in spec.taskSpecification)


def test_process_specification_defaults_to_empty_lists():
    spec = ProcessSpecification.from_dict({"@type": "ProcessSpecification", "id": "1"})

    assert spec.validFor is None
    assert spec.processSpecificationCharacteristic == []
    assert spec.processSpecificationRelationship == []
    assert spec.processSpecificationPolicy == []
    assert spec.taskSpecification == []
    assert spec.channel == []
    assert spec.relatedParty == []
    assert spec.attachment == []


def test_process_specification_to_dict_round_trip(process_specification_dict):
    result = ProcessSpecification.from_dict(process_specification_dict).to_dict()

    assert result["@type"] == "ProcessSpecification"
    assert "@baseType" not in result
    assert result["lifecycleStatus"] == "onDesign"
    assert result["validFor"]["startDateTime"] == "2024-01-01T00:00:00.000Z"
    assert result["attachment"][0]["@type"] == "Attachment"
    assert result["attachment"][0]["size"]["amount"] == 2423
    assert result["attachment"][1]["@type"] == "AttachmentRef"
    value_spec = result["processSpecificationCharacteristic"][0][
        "characteristicSpecification"
    ]["characteristicValueSpecification"][0]
    assert value_spec["@type"] == "BooleanCharacteristicValueSpecification"
    assert value_spec["@baseType"] == "CharacteristicValueSpecification"
    assert value_spec["value"] is False
    assert result["processSpecificationPolicy"][0]["@referredType"] == "Policy"
    assert (
        result["processSpecificationRelationship"][0]["processSpecification"]["version"]
        == "3"
    )
    assert result["taskSpecification"][1]["@referredType"] == "TaskSpecification"


def test_task_specification_instantiates_classes(task_specification_dict):
    spec = TaskSpecification.from_dict(task_specification_dict)

    assert spec.id == "tfs0"
    assert spec.taskType == "businessRuleTask"
    assert spec.lifecycleStatus == "active"
    assert isinstance(spec.validFor, TimePeriod)
    assert isinstance(spec.channel[0], ChannelRef)
    assert isinstance(spec.attachment[0], Attachment)

    flow_char_spec = spec.taskSpecificationCharacteristic[0]
    assert isinstance(flow_char_spec, FlowCharacteristicSpecification)
    assert flow_char_spec.modality == "output"
    assert isinstance(
        flow_char_spec.characteristicSpecification, CharacteristicSpecification
    )

    relationship = spec.taskSpecificationRelationship[0]
    assert isinstance(relationship, TaskSpecificationRelationship)
    assert relationship.relationshipType == "nextTask"
    assert isinstance(relationship.taskSpecification, TaskSpecificationRef)

    related = spec.relatedProcessSpecification[0]
    assert isinstance(related, RelatedProcessSpecification)
    assert related.role == "usedBy"
    assert isinstance(related.processSpecification, ProcessSpecificationRef)

    assert isinstance(spec.taskSpecificationPolicy[0], PolicyRef)
    assert isinstance(spec.relatedParty[0].partyOrPartyRole, PartyRef)


def test_task_specification_rejects_non_list_characteristic():
    with pytest.raises(ValueError):
        TaskSpecification(
            taskSpecificationCharacteristic=FlowCharacteristicSpecification(
                modality="input"
            )
        )


def test_task_specification_to_dict_round_trip(task_specification_dict):
    result = TaskSpecification.from_dict(task_specification_dict).to_dict()

    assert result["@type"] == "TaskSpecification"
    assert "@baseType" not in result
    assert result["taskType"] == "businessRuleTask"
    assert (
        result["taskSpecificationCharacteristic"][0]["@type"]
        == "FlowCharacteristicSpecification"
    )
    assert (
        result["taskSpecificationRelationship"][0]["taskSpecification"]["@type"]
        == "TaskSpecificationRef"
    )
    assert (
        result["relatedProcessSpecification"][0]["processSpecification"][
            "@referredType"
        ]
        == "ProcessSpecification"
    )
    assert result["taskSpecificationPolicy"][0]["@type"] == "PolicyRef"


def test_boolean_array_characteristic_value_specification_resolves_by_type():
    char_spec = CharacteristicSpecification.from_dict(
        {
            "@type": "CharacteristicSpecification",
            "name": "enabledFeatures",
            "characteristicValueSpecification": [
                {
                    "@type": "BooleanArrayCharacteristicValueSpecification",
                    "value": [True, False],
                }
            ],
        }
    )

    value_spec = char_spec.characteristicValueSpecification[0]
    assert isinstance(value_spec, BooleanArrayCharacteristicValueSpecification)
    assert isinstance(value_spec, CharacteristicValueSpecification)
    assert value_spec.value == [True, False]

    result = value_spec.to_dict()
    assert result["@baseType"] == "CharacteristicValueSpecification"
    assert result["value"] == [True, False]


def test_flow_state_type_values():
    assert [s.value for s in FlowStateType] == [
        "ready",
        "planned",
        "active",
        "withdrawn",
        "terminated",
        "failed",
        "completed",
        "other",
    ]


def test_process_management_resource_paths(context):
    base = "https://host:port/tmf-api/processManagement/v5"

    assert Process.get_resource_path(context) == f"{base}/process"
    assert Task.get_resource_path(context) == f"{base}/task"
    assert (
        ProcessSpecification.get_resource_path(context)
        == f"{base}/processSpecification"
    )
    assert TaskSpecification.get_resource_path(context) == f"{base}/taskSpecification"
