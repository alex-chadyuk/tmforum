import pytest
from tmforum import (
    Attachment,
    AttachmentRef,
    ChannelRef,
    CharacteristicRelationship,
    CharacteristicSpecification,
    CharacteristicSpecificationRelationship,
    EntityRef,
    ExternalIdentifier,
    Note,
    NumberCharacteristic,
    PartyRef,
    PartyRoleRef,
    RelatedEntity,
    RelatedPartyRefOrPartyRoleRef,
    StatusChange,
    StringCharacteristic,
    TimePeriod,
    TroubleTicket,
    TroubleTicketRelationship,
    TroubleTicketSpecification,
    TroubleTicketSpecificationRef,
    TroubleTicketStatusType,
)

BASE = "https://mycsp.com:8080/tmf-api/troubleTicket/v5"


@pytest.fixture
def trouble_ticket_dict():
    return {
        "@type": "TroubleTicket",
        "id": "3180",
        "href": f"{BASE}/troubleTicket/3180",
        "@schemaLocation": "https://mycsp.com:8080/tmf-api/troubleTicket/5/schema/troubleTicket.yaml",
        "name": "complaint over last bill",
        "description": "I do not accept the last VOD charge",
        "creationDate": "2022-05-31T07:34:45.968Z",
        "lastUpdate": "2022-05-31T07:34:45.968Z",
        "requestedResolutionDate": "2022-05-31T07:34:45.968Z",
        "expectedResolutionDate": "2019-06-10T07:34:45.968Z",
        "resolutionDate": "2022-05-31T07:34:45.968Z",
        "priority": "High",
        "severity": "Minor",
        "ticketType": "Bill Dispute",
        "status": "resolved",
        "statusChangeDate": "2022-05-31T07:34:45.968Z",
        "statusChangeReason": "Apply full credit",
        "troubleTicketSpecification": {
            "@type": "TroubleTicketSpecificationRef",
            "id": "25632415",
            "href": f"{BASE}/troubleTicketSpecification/25632415",
            "name": "Bill Dispute",
            "version": "1",
        },
        "troubleTicketCharacteristic": [
            {
                "@type": "NumberCharacteristic",
                "id": "2",
                "name": "creditAmount",
                "valueType": "number",
                "value": 40,
                "characteristicRelationship": [
                    {
                        "@type": "CharacteristicRelationship",
                        "id": "4",
                        "relationshipType": "dependency",
                    }
                ],
            },
            {
                "@type": "StringCharacteristic",
                "id": "3",
                "name": "currency",
                "valueType": "string",
                "value": "USD",
            },
        ],
        "attachment": [
            {
                "@type": "Attachment",
                "description": "Scanned disputed bill",
                "attachmentType": "billCopy",
                "mimeType": "image/png",
                "name": "March Bill",
                "url": "https://mycsp.com:7070/docloader?docnum=3534555",
            },
            {
                "@type": "AttachmentRef",
                "@referredType": "Attachment",
                "id": "4455",
                "href": "https://mycsp.com:8080/tmf-api/document/v5/attachment/4455",
            },
        ],
        "channel": {"@type": "ChannelRef", "id": "8774", "name": "self service"},
        "note": [
            {
                "@type": "Note",
                "id": "77456",
                "author": "Jack Smith",
                "date": "2019-05-31T07:34:45.968Z",
                "text": "This is quite important",
            }
        ],
        "relatedEntity": [
            {
                "@type": "RelatedEntity",
                "role": "disputedBill",
                "entity": {
                    "@type": "EntityRef",
                    "@referredType": "CustomerBill",
                    "id": "3472",
                    "href": "https://mycsp.com:8080/tmf-api/customerBillManagement/v5/customerBill/8297",
                    "name": "March 2019 Bill",
                },
            }
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "role": "reporter",
                "partyOrPartyRole": {
                    "@type": "PartyRef",
                    "@referredType": "Individual",
                    "id": "9877",
                    "name": "Jacob Jac Miller",
                },
            },
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "role": "customer",
                "partyOrPartyRole": {
                    "@type": "PartyRoleRef",
                    "@referredType": "Customer",
                    "id": "9176",
                    "href": "https://mycsp.com:8080/tmf-api/partyManagement/v5/customer/9176",
                    "name": "Jack Smith",
                },
            },
        ],
        "statusChangeHistory": [
            {
                "@type": "StatusChange",
                "statusChangeDate": "2022-05-28T07:34:45.968Z",
                "statusChangeReason": "trouble ticket created ",
                "status": "acknowledged",
            },
            {
                "@type": "StatusChange",
                "statusChangeDate": "2022-05-28T08:34:45.968Z",
                "statusChangeReason": "start process",
                "status": "inProgress",
            },
        ],
        "troubleTicketRelationship": [
            {
                "@type": "TroubleTicketRelationship",
                "id": "567433",
                "href": f"{BASE}/troubleTicket/567433",
                "name": "Network Coverage",
                "relationshipType": "dependency",
            }
        ],
        "externalIdentifier": [
            {
                "@type": "ExternalIdentifier",
                "id": "3331234",
                "owner": "BMC Remedy",
                "externalIdentifierType": "Incident",
            }
        ],
    }


@pytest.fixture
def trouble_ticket_specification_dict():
    return {
        "@type": "TroubleTicketSpecification",
        "id": "25632415",
        "href": f"{BASE}/troubleTicketSpecification/25632415",
        "name": "Bill Dispute",
        "description": "Characteristics and rules to apply when creating a trouble ticket",
        "creationDate": "2022-05-22T10:36:30.709Z",
        "lastUpdate": "2022-06-22T10:36:30.709Z",
        "lifecycleStatus": "active",
        "version": "1",
        "validFor": {"startDateTime": "2022-06-22T23:20:50.52Z"},
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "role": "approver",
                "partyOrPartyRole": {
                    "@type": "PartyRef",
                    "@referredType": "Individual",
                    "id": "6678",
                    "name": "Sara Smith",
                },
            }
        ],
        "specCharacteristic": [
            {
                "@type": "CharacteristicSpecification",
                "id": "2",
                "configurable": True,
                "maxCardinality": 0,
                "minCardinality": 1,
                "name": "creditAmount",
                "valueType": "number",
                "charSpecRelationship": [
                    {
                        "@type": "CharacteristicSpecificationRelationship",
                        "characteristicSpecificationId": "3",
                        "name": "creditReason",
                        "relationshipType": "dependency",
                        "parentSpecificationId": "25632415",
                    }
                ],
            },
            {
                "@type": "CharacteristicSpecification",
                "id": "3",
                "configurable": True,
                "name": "creditReason",
                "valueType": "string",
            },
        ],
    }


def test_trouble_ticket_instantiates_classes(trouble_ticket_dict):
    ticket = TroubleTicket.from_dict(trouble_ticket_dict, strict=True)

    assert isinstance(ticket, TroubleTicket)
    assert ticket.id == "3180"
    assert ticket.status is TroubleTicketStatusType.RESOLVED
    assert isinstance(ticket.troubleTicketSpecification, TroubleTicketSpecificationRef)
    assert ticket.troubleTicketSpecification.version == "1"
    assert isinstance(ticket.channel, ChannelRef)
    assert isinstance(ticket.troubleTicketCharacteristic[0], NumberCharacteristic)
    assert isinstance(
        ticket.troubleTicketCharacteristic[0].characteristicRelationship[0],
        CharacteristicRelationship,
    )
    assert isinstance(ticket.troubleTicketCharacteristic[1], StringCharacteristic)
    assert isinstance(ticket.note[0], Note)
    assert isinstance(ticket.relatedEntity[0], RelatedEntity)
    assert isinstance(ticket.relatedEntity[0].entity, EntityRef)
    assert isinstance(ticket.relatedParty[0], RelatedPartyRefOrPartyRoleRef)
    assert isinstance(ticket.relatedParty[0].partyOrPartyRole, PartyRef)
    assert isinstance(ticket.relatedParty[1].partyOrPartyRole, PartyRoleRef)
    assert isinstance(ticket.statusChangeHistory[0], StatusChange)
    assert isinstance(ticket.troubleTicketRelationship[0], TroubleTicketRelationship)
    assert isinstance(ticket.externalIdentifier[0], ExternalIdentifier)


def test_trouble_ticket_attachment_resolves_ref_or_value(trouble_ticket_dict):
    ticket = TroubleTicket.from_dict(trouble_ticket_dict)

    assert type(ticket.attachment[0]) is Attachment
    assert ticket.attachment[0].attachmentType == "billCopy"
    assert type(ticket.attachment[1]) is AttachmentRef
    assert ticket.attachment[1].id == "4455"


def test_trouble_ticket_status_change_history_uses_status_enum(trouble_ticket_dict):
    ticket = TroubleTicket.from_dict(trouble_ticket_dict)

    assert [change.status for change in ticket.statusChangeHistory] == [
        TroubleTicketStatusType.ACKNOWLEDGED,
        TroubleTicketStatusType.IN_PROGRESS,
    ]


def test_trouble_ticket_relationship_defaults_referred_type():
    relationship = TroubleTicketRelationship(id="1", relationshipType="dependency")

    result = relationship.to_dict()

    assert result["@type"] == "TroubleTicketRelationship"
    assert result["@referredType"] == "TroubleTicket"
    assert result["relationshipType"] == "dependency"


def test_trouble_ticket_defaults_to_empty_lists():
    ticket = TroubleTicket()

    assert ticket.attachment == []
    assert ticket.note == []
    assert ticket.statusChangeHistory == []
    assert ticket.troubleTicketRelationship == []
    assert ticket.troubleTicketCharacteristic == []


def test_trouble_ticket_rejects_non_list_note():
    with pytest.raises(ValueError):
        TroubleTicket(note=Note(text="not a list"))


def test_trouble_ticket_to_dict_round_trip(trouble_ticket_dict):
    result = TroubleTicket.from_dict(trouble_ticket_dict).to_dict()

    assert result["@type"] == "TroubleTicket"
    assert "@baseType" not in result
    assert result["@schemaLocation"] == trouble_ticket_dict["@schemaLocation"]
    assert result["status"] == "resolved"
    assert result["resolutionDate"] == "2022-05-31T07:34:45.968Z"
    assert result["channel"]["@referredType"] == "Channel"
    assert result["troubleTicketSpecification"]["@type"] == (
        "TroubleTicketSpecificationRef"
    )
    assert result["troubleTicketSpecification"]["@referredType"] == (
        "TroubleTicketSpecification"
    )
    assert result["troubleTicketSpecification"]["version"] == "1"
    assert result["troubleTicketCharacteristic"][0]["@type"] == "NumberCharacteristic"
    assert result["troubleTicketCharacteristic"][0]["value"] == 40
    assert result["attachment"][0]["@type"] == "Attachment"
    assert result["attachment"][1]["@type"] == "AttachmentRef"
    assert result["relatedParty"][1]["partyOrPartyRole"]["@type"] == "PartyRoleRef"
    assert result["statusChangeHistory"][1]["@type"] == "StatusChange"
    assert result["statusChangeHistory"][1]["status"] == "inProgress"
    assert result["troubleTicketRelationship"][0]["@referredType"] == "TroubleTicket"
    assert result["troubleTicketRelationship"][0]["relationshipType"] == "dependency"
    assert result["relatedEntity"][0]["entity"]["@referredType"] == "CustomerBill"


def test_trouble_ticket_specification_instantiates_classes(
    trouble_ticket_specification_dict,
):
    spec = TroubleTicketSpecification.from_dict(
        trouble_ticket_specification_dict, strict=True
    )

    assert isinstance(spec, TroubleTicketSpecification)
    assert spec.lifecycleStatus == "active"
    assert spec.version == "1"
    assert isinstance(spec.validFor, TimePeriod)
    assert isinstance(spec.relatedParty[0].partyOrPartyRole, PartyRef)
    assert isinstance(spec.specCharacteristic[0], CharacteristicSpecification)
    assert spec.specCharacteristic[0].minCardinality == 1
    assert isinstance(
        spec.specCharacteristic[0].charSpecRelationship[0],
        CharacteristicSpecificationRelationship,
    )


def test_trouble_ticket_specification_defaults_to_empty_lists():
    spec = TroubleTicketSpecification()

    assert spec.specCharacteristic == []
    assert spec.relatedParty == []


def test_trouble_ticket_specification_to_dict_round_trip(
    trouble_ticket_specification_dict,
):
    result = TroubleTicketSpecification.from_dict(
        trouble_ticket_specification_dict
    ).to_dict()

    assert result["@type"] == "TroubleTicketSpecification"
    assert "@baseType" not in result
    assert result["lifecycleStatus"] == "active"
    assert result["creationDate"] == "2022-05-22T10:36:30.709Z"
    assert result["validFor"]["startDateTime"] == "2022-06-22T23:20:50.52Z"
    assert result["specCharacteristic"][0]["@type"] == "CharacteristicSpecification"
    relationship = result["specCharacteristic"][0]["charSpecRelationship"][0]
    assert relationship["@type"] == "CharacteristicSpecificationRelationship"
    assert relationship["characteristicSpecificationId"] == "3"
    assert result["relatedParty"][0]["role"] == "approver"


def test_trouble_ticket_status_type_values():
    assert [member.value for member in TroubleTicketStatusType] == [
        "acknowledged",
        "rejected",
        "pending",
        "held",
        "inProgress",
        "cancelled",
        "closed",
        "resolved",
    ]


def test_trouble_ticket_resource_paths(context):
    base = "https://host:port/tmf-api/troubleTicket/v5"

    assert TroubleTicket.get_resource_path(context) == f"{base}/troubleTicket"
    assert (
        TroubleTicketSpecification.get_resource_path(context)
        == f"{base}/troubleTicketSpecification"
    )
