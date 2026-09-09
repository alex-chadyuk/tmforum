import pytest
from tmforum import (
    Context,
    ErrorMessage,
    EventRef,
    ExternalIdentifier,
    GeographicAddress,
    ImpactPattern,
    Note,
    NumberCharacteristic,
    PartyRoleRef,
    ProblemAcknowledgement,
    ProblemGroup,
    ProblemUnacknowledgement,
    ProblemUngroup,
    RelatedEntity,
    RelatedPartyRefOrPartyRoleRef,
    RelatedPlaceRefOrValue,
    ResourceAlarmRef,
    ResourceRef,
    ServiceProblem,
    ServiceProblemEventRecord,
    ServiceProblemRef,
    ServiceProblemStateType,
    ServiceRef,
    SLAViolationRef,
    StandardIdentifier,
    StringCharacteristic,
    TaskStateType,
    TrackingRecord,
    TroubleTicketRef,
)


@pytest.fixture
def service_problem_dict():
    return {
        "@type": "ServiceProblem",
        "@baseType": "Entity",
        "id": "sp_001",
        "href": (
            "https://mycsp.com:8080/tmf-api/serviceProblemManagement/v5"
            "/serviceProblem/sp_001"
        ),
        "name": "Broadband degradation in Leeds North",
        "description": "Packet loss above 5% on the Leeds North aggregation ring",
        "category": "serviceProvider.declarer",
        "reason": "Fibre cut on the northbound path",
        "priority": 2,
        "status": "inProgress",
        "statusChangeDate": "2026-05-11T09:20:00.000Z",
        "statusChangeReason": "Field engineer dispatched",
        "creationDate": "2026-05-11T08:02:00.000Z",
        "lastUpdate": "2026-05-11T09:20:00.000Z",
        "resolutionDate": "2026-05-11T14:45:00.000Z",
        "originatingSystem": "NetworkAssuranceOSS",
        "problemEscalation": "3",
        "impactImportanceFactor": "72",
        "affectedNumberOfServices": 1450,
        "impactPattern": {
            "@type": "ImpactPattern",
            "id": "ip-1",
            "description": "Degraded throughput without total loss of service",
            "characteristic": [
                {
                    "@type": "NumberCharacteristic",
                    "name": "packetLossPercent",
                    "valueType": "Number",
                    "value": 5.4,
                }
            ],
        },
        "firstAlert": {
            "@type": "RelatedEntity",
            "role": "firstAlert",
            "entity": {
                "@type": "ResourceAlarmRef",
                "@referredType": "ResourceAlarm",
                "id": "alarm-9001",
                "name": "LOS on port 3/1/2",
            },
        },
        "responsibleParty": {
            "@type": "RelatedPartyRefOrPartyRoleRef",
            "role": "problemHandler",
            "partyOrPartyRole": {
                "@type": "PartyRoleRef",
                "@referredType": "PartyRole",
                "id": "pr-21",
                "name": "NOC Tier 2",
            },
        },
        "originatorParty": {
            "@type": "RelatedPartyRefOrPartyRoleRef",
            "role": "originator",
            "partyOrPartyRole": {
                "@type": "PartyRoleRef",
                "@referredType": "PartyRole",
                "id": "pr-04",
                "name": "Service Desk",
            },
        },
        "affectedLocation": [
            {
                "@type": "RelatedPlaceRefOrValue",
                "role": "affectedArea",
                "place": {
                    "@type": "GeographicAddress",
                    "id": "addr-77",
                    "city": "Leeds",
                    "country": "United Kingdom",
                    "postcode": "LS7 2AB",
                    "geographicAddressType": "postalAddress",
                    "countryCode": [
                        {
                            "@type": "StandardIdentifier",
                            "format": "ISO 3166-1 Alpha 2",
                            "value": "GB",
                        }
                    ],
                    "externalIdentifier": [
                        {
                            "@type": "ExternalIdentifier",
                            "owner": "AddressBase",
                            "externalIdentifierType": "UPRN",
                            "id": "100023336956",
                        }
                    ],
                },
            }
        ],
        "affectedResource": [
            {
                "@type": "ResourceRef",
                "@referredType": "Resource",
                "id": "res-agg-12",
                "name": "Leeds North aggregation router",
            }
        ],
        "affectedService": [
            {
                "@type": "ServiceRef",
                "@referredType": "Service",
                "id": "svc-bb-4410",
                "name": "Residential broadband",
            }
        ],
        "rootCauseResource": [
            {
                "@type": "ResourceRef",
                "@referredType": "Resource",
                "id": "res-fibre-88",
                "name": "Northbound fibre span",
            }
        ],
        "rootCauseService": [
            {
                "@type": "ServiceRef",
                "@referredType": "Service",
                "id": "svc-transport-9",
                "name": "Transport service",
            }
        ],
        "parentProblem": [
            {
                "@type": "ServiceProblemRef",
                "@referredType": "ServiceProblem",
                "id": "sp_000",
                "name": "Regional transport outage",
            }
        ],
        "underlyingProblem": [
            {
                "@type": "ServiceProblemRef",
                "@referredType": "ServiceProblem",
                "id": "sp_002",
            }
        ],
        "underlyingAlarm": [
            {
                "@type": "ResourceAlarmRef",
                "@referredType": "ResourceAlarm",
                "id": "alarm-9001",
                "changeRequest": {
                    "@type": "EntityRef",
                    "@referredType": "ChangeRequest",
                    "id": "cr-55",
                },
            }
        ],
        "slaViolation": [
            {
                "@type": "SLAViolationRef",
                "@referredType": "SLAViolation",
                "id": "slav-3",
            }
        ],
        "troubleTicket": [
            {
                "@type": "TroubleTicketRef",
                "@referredType": "TroubleTicket",
                "id": "tt-6621",
                "name": "Leeds North degradation",
            }
        ],
        "relatedEvent": [
            {
                "@type": "EventRef",
                "@referredType": "Event",
                "id": "ev-1",
                "eventTime": "2026-05-11T08:01:12.000Z",
            }
        ],
        "relatedEntity": [
            {
                "@type": "RelatedEntity",
                "role": "changeRequest",
                "entity": {
                    "@type": "EntityRef",
                    "@referredType": "ChangeRequest",
                    "id": "cr-55",
                },
            }
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "role": "affectedCustomer",
                "partyOrPartyRole": {
                    "@type": "PartyRoleRef",
                    "@referredType": "PartyRole",
                    "id": "pr-900",
                    "name": "Northern Retail Ltd",
                },
            }
        ],
        "trackingRecord": [
            {
                "@type": "TrackingRecord",
                "id": "tr-1",
                "description": "acknowledge",
                "systemId": "NOC-Console",
                "time": "2026-05-11T08:15:00.000Z",
                "user": "j.okafor",
                "characteristic": [
                    {
                        "@type": "StringCharacteristic",
                        "name": "shift",
                        "valueType": "String",
                        "value": "early",
                    }
                ],
            }
        ],
        "characteristic": [
            {
                "@type": "StringCharacteristic",
                "name": "ringId",
                "valueType": "String",
                "value": "LDS-N-01",
            }
        ],
        "externalIdentifier": [
            {
                "@type": "ExternalIdentifier",
                "owner": "ServiceNow",
                "externalIdentifierType": "Incident",
                "id": "INC0042311",
            }
        ],
        "errorMessage": [
            {
                "@type": "ErrorMessage",
                "code": "656-14",
                "reason": "Downstream probe unreachable",
            }
        ],
        "note": [
            {
                "@type": "Note",
                "id": "note-1",
                "author": "j.okafor",
                "date": "2026-05-11T08:16:00.000Z",
                "text": "Escalated to field operations.",
            }
        ],
    }


@pytest.fixture
def service_problem_1(service_problem_dict):
    return ServiceProblem.from_dict(service_problem_dict)


def test_service_problem_instantiates_with_id(service_problem_dict):
    sp = ServiceProblem.from_dict(service_problem_dict)

    assert sp.id == "sp_001"
    assert sp.name == "Broadband degradation in Leeds North"
    assert sp.category == "serviceProvider.declarer"
    assert sp.priority == 2
    assert sp.affectedNumberOfServices == 1450
    assert sp.impactImportanceFactor == "72"
    assert sp.problemEscalation == "3"
    assert sp.originatingSystem == "NetworkAssuranceOSS"
    assert sp.statusChangeReason == "Field engineer dispatched"
    assert sp.resolutionDate == "2026-05-11T14:45:00.000Z"
    assert sp.href.endswith("/serviceProblem/sp_001")


def test_service_problem_status_is_enum(service_problem_1):
    assert service_problem_1.status is ServiceProblemStateType.IN_PROGRESS
    assert service_problem_1.status.value == "inProgress"


def test_service_problem_instantiates_classes(service_problem_1):
    sp = service_problem_1

    assert isinstance(sp, ServiceProblem)

    assert isinstance(sp.impactPattern, ImpactPattern)
    assert isinstance(sp.impactPattern.characteristic[0], NumberCharacteristic)
    assert sp.impactPattern.characteristic[0].value == 5.4

    assert isinstance(sp.firstAlert, RelatedEntity)
    assert isinstance(sp.firstAlert.entity, ResourceAlarmRef)
    assert sp.firstAlert.entity._referred_type == "ResourceAlarm"

    assert isinstance(sp.responsibleParty, RelatedPartyRefOrPartyRoleRef)
    assert isinstance(sp.responsibleParty.partyOrPartyRole, PartyRoleRef)
    assert isinstance(sp.originatorParty, RelatedPartyRefOrPartyRoleRef)

    assert isinstance(sp.affectedLocation[0], RelatedPlaceRefOrValue)
    assert isinstance(sp.affectedLocation[0].place, GeographicAddress)
    assert sp.affectedLocation[0].place.city == "Leeds"

    assert isinstance(sp.affectedResource[0], ResourceRef)
    assert isinstance(sp.affectedService[0], ServiceRef)
    assert isinstance(sp.rootCauseResource[0], ResourceRef)
    assert isinstance(sp.rootCauseService[0], ServiceRef)

    assert isinstance(sp.parentProblem[0], ServiceProblemRef)
    assert sp.parentProblem[0]._referred_type == "ServiceProblem"
    assert isinstance(sp.underlyingProblem[0], ServiceProblemRef)

    assert isinstance(sp.underlyingAlarm[0], ResourceAlarmRef)
    assert sp.underlyingAlarm[0].changeRequest.id == "cr-55"

    assert isinstance(sp.slaViolation[0], SLAViolationRef)
    assert isinstance(sp.troubleTicket[0], TroubleTicketRef)

    assert isinstance(sp.relatedEvent[0], EventRef)
    assert sp.relatedEvent[0].eventTime == "2026-05-11T08:01:12.000Z"

    assert isinstance(sp.relatedEntity[0], RelatedEntity)
    assert isinstance(sp.relatedParty[0], RelatedPartyRefOrPartyRoleRef)

    assert isinstance(sp.trackingRecord[0], TrackingRecord)
    assert sp.trackingRecord[0].user == "j.okafor"
    assert isinstance(sp.trackingRecord[0].characteristic[0], StringCharacteristic)
    assert sp.trackingRecord[0].characteristic[0].value == "early"

    assert isinstance(sp.characteristic[0], StringCharacteristic)
    assert sp.characteristic[0].value == "LDS-N-01"
    assert isinstance(sp.externalIdentifier[0], ExternalIdentifier)
    assert isinstance(sp.errorMessage[0], ErrorMessage)
    assert isinstance(sp.note[0], Note)


def test_geographic_address_carries_country_code(service_problem_1):
    address = service_problem_1.affectedLocation[0].place

    assert address.geographicAddressType == "postalAddress"
    assert isinstance(address.countryCode[0], StandardIdentifier)
    assert address.countryCode[0].format == "ISO 3166-1 Alpha 2"
    assert address.countryCode[0].value == "GB"
    assert isinstance(address.externalIdentifier[0], ExternalIdentifier)
    assert address.externalIdentifier[0].externalIdentifierType == "UPRN"


def test_service_problem_defaults_to_empty_lists():
    sp = ServiceProblem.from_dict({"@type": "ServiceProblem", "id": "sp_x"})

    assert sp.affectedLocation == []
    assert sp.affectedResource == []
    assert sp.affectedService == []
    assert sp.rootCauseResource == []
    assert sp.rootCauseService == []
    assert sp.parentProblem == []
    assert sp.underlyingProblem == []
    assert sp.underlyingAlarm == []
    assert sp.slaViolation == []
    assert sp.troubleTicket == []
    assert sp.relatedEvent == []
    assert sp.relatedEntity == []
    assert sp.relatedParty == []
    assert sp.trackingRecord == []
    assert sp.characteristic == []
    assert sp.externalIdentifier == []
    assert sp.errorMessage == []
    assert sp.note == []
    assert sp.status is None
    assert sp.impactPattern is None
    assert sp.firstAlert is None


def test_service_problem_to_dict_round_trip(service_problem_dict):
    result = ServiceProblem.from_dict(service_problem_dict).to_dict()

    assert result["@type"] == "ServiceProblem"
    assert "@baseType" not in result
    assert result["status"] == "inProgress"
    assert result["priority"] == 2
    assert result["impactPattern"]["@type"] == "ImpactPattern"
    assert result["firstAlert"]["entity"]["@referredType"] == "ResourceAlarm"
    assert result["affectedService"][0]["@referredType"] == "Service"
    assert result["parentProblem"][0]["@referredType"] == "ServiceProblem"
    assert result["relatedEvent"][0]["eventTime"] == "2026-05-11T08:01:12.000Z"
    assert result["trackingRecord"][0]["@type"] == "TrackingRecord"
    assert (
        result["responsibleParty"]["partyOrPartyRole"]["@referredType"] == "PartyRole"
    )
    assert result["affectedLocation"][0]["place"]["countryCode"][0]["value"] == "GB"


def test_service_problem_ref_from_entity(service_problem_1):
    ref = ServiceProblemRef.from_entity(service_problem_1)

    assert isinstance(ref, ServiceProblemRef)
    assert ref.id == "sp_001"
    assert ref.name == "Broadband degradation in Leeds North"
    assert ref._referred_type == "ServiceProblem"


def test_service_problem_event_record():
    record = ServiceProblemEventRecord.from_dict(
        {
            "@type": "ServiceProblemEventRecord",
            "id": "42",
            "href": (
                "https://mycsp.com:8080/tmf-api/serviceProblemManagement/v5"
                "/serviceProblemEventRecord/42"
            ),
            "eventTime": "2026-05-11T08:01:12.000Z",
            "eventType": "serviceProblemStateChangeEvent",
            "recordTime": "2026-05-11T08:01:15.000Z",
            "serviceProblem": {
                "@type": "ServiceProblemRef",
                "@referredType": "ServiceProblem",
                "id": "sp_001",
            },
            "notification": {"eventId": "ev-1", "eventType": "stateChange"},
        }
    )

    assert record.id == "42"
    assert record.eventType == "serviceProblemStateChangeEvent"
    assert record.recordTime == "2026-05-11T08:01:15.000Z"
    assert isinstance(record.serviceProblem, ServiceProblemRef)
    assert record.serviceProblem.id == "sp_001"
    assert record.notification == {"eventId": "ev-1", "eventType": "stateChange"}

    result = record.to_dict()
    assert result["@type"] == "ServiceProblemEventRecord"
    assert result["serviceProblem"]["@referredType"] == "ServiceProblem"
    assert result["notification"]["eventId"] == "ev-1"


@pytest.fixture
def problem_acknowledgement_dict():
    return {
        "@type": "ProblemAcknowledgement",
        "id": "pa_00001",
        "href": (
            "https://mycsp.com:8080/tmf-api/serviceProblemManagement/v5"
            "/problemAcknowledgement/pa_00001"
        ),
        "state": "done",
        "trackingRecord": {
            "@type": "TrackingRecord",
            "id": "tr-9",
            "description": "acknowledge",
            "user": "a.silva",
            "time": "2026-05-11T08:15:00.000Z",
        },
        "problem": [
            {
                "@type": "ServiceProblemRef",
                "@referredType": "ServiceProblem",
                "id": "41",
            },
            {
                "@type": "ServiceProblemRef",
                "@referredType": "ServiceProblem",
                "id": "42",
            },
        ],
        "ackProblem": [
            {
                "@type": "ServiceProblemRef",
                "@referredType": "ServiceProblem",
                "id": "41",
            }
        ],
    }


def test_problem_acknowledgement(problem_acknowledgement_dict):
    ack = ProblemAcknowledgement.from_dict(problem_acknowledgement_dict)

    assert ack.id == "pa_00001"
    assert ack.state is TaskStateType.DONE
    assert isinstance(ack.trackingRecord, TrackingRecord)
    assert ack.trackingRecord.user == "a.silva"
    assert [p.id for p in ack.problem] == ["41", "42"]
    assert all(isinstance(p, ServiceProblemRef) for p in ack.problem)
    assert [p.id for p in ack.ackProblem] == ["41"]

    result = ack.to_dict()
    assert result["@type"] == "ProblemAcknowledgement"
    assert result["state"] == "done"
    assert result["problem"][0]["@referredType"] == "ServiceProblem"
    assert result["trackingRecord"]["@type"] == "TrackingRecord"


def test_problem_unacknowledgement():
    unack = ProblemUnacknowledgement.from_dict(
        {
            "@type": "ProblemUnacknowledgement",
            "id": "pu_00001",
            "state": "inProgress",
            "problem": [
                {
                    "@type": "ServiceProblemRef",
                    "@referredType": "ServiceProblem",
                    "id": "41",
                }
            ],
            "unackProblem": [
                {
                    "@type": "ServiceProblemRef",
                    "@referredType": "ServiceProblem",
                    "id": "41",
                }
            ],
        }
    )

    assert unack.state is TaskStateType.IN_PROGRESS
    assert isinstance(unack.problem[0], ServiceProblemRef)
    assert isinstance(unack.unackProblem[0], ServiceProblemRef)
    assert unack.trackingRecord is None

    assert unack.to_dict()["unackProblem"][0]["id"] == "41"


def test_problem_group():
    group = ProblemGroup.from_dict(
        {
            "@type": "ProblemGroup",
            "id": "pg_00001",
            "state": "acknowledged",
            "parentProblem": {
                "@type": "ServiceProblemRef",
                "@referredType": "ServiceProblem",
                "id": "sp_000",
            },
            "childProblem": [
                {
                    "@type": "ServiceProblemRef",
                    "@referredType": "ServiceProblem",
                    "id": "sp_001",
                },
                {
                    "@type": "ServiceProblemRef",
                    "@referredType": "ServiceProblem",
                    "id": "sp_002",
                },
            ],
        }
    )

    assert group.state is TaskStateType.ACKNOWLEDGED
    assert isinstance(group.parentProblem, ServiceProblemRef)
    assert group.parentProblem.id == "sp_000"
    assert [c.id for c in group.childProblem] == ["sp_001", "sp_002"]

    result = group.to_dict()
    assert result["@type"] == "ProblemGroup"
    assert result["parentProblem"]["@referredType"] == "ServiceProblem"


def test_problem_ungroup():
    ungroup = ProblemUngroup.from_dict(
        {
            "@type": "ProblemUngroup",
            "id": "pug_00001",
            "parentProblem": {
                "@type": "ServiceProblemRef",
                "@referredType": "ServiceProblem",
                "id": "sp_000",
            },
            "childProblem": [
                {
                    "@type": "ServiceProblemRef",
                    "@referredType": "ServiceProblem",
                    "id": "sp_001",
                }
            ],
        }
    )

    assert ungroup.state is None
    assert isinstance(ungroup.parentProblem, ServiceProblemRef)
    assert isinstance(ungroup.childProblem[0], ServiceProblemRef)

    assert ungroup.to_dict()["@type"] == "ProblemUngroup"


def test_service_problem_resource_paths():
    context = Context(api_base_url="https://mycsp.com:8080/tmf-api")
    base = "https://mycsp.com:8080/tmf-api/serviceProblemManagement/v5"

    assert ServiceProblem.get_resource_path(context) == f"{base}/serviceProblem"
    assert (
        ServiceProblemEventRecord.get_resource_path(context)
        == f"{base}/serviceProblemEventRecord"
    )
    assert (
        ProblemAcknowledgement.get_resource_path(context)
        == f"{base}/problemAcknowledgement"
    )
    assert (
        ProblemUnacknowledgement.get_resource_path(context)
        == f"{base}/problemUnacknowledgement"
    )
    assert ProblemGroup.get_resource_path(context) == f"{base}/problemGroup"
    assert ProblemUngroup.get_resource_path(context) == f"{base}/problemUngroup"
