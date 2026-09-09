import pytest
from tmforum import (
    BalanceActionRef,
    Bucket,
    BucketCounter,
    BucketRef,
    BucketRelationship,
    BucketSpecificationRef,
    BucketStatusType,
    Characteristic,
    ConsumptionSummary,
    Context,
    EntityRelationship,
    LogicalResourceRef,
    PartyAccountRef,
    PartyRef,
    PartyRoleRef,
    ProductRef,
    Quantity,
    QueryUsageConsumption,
    RelatedPartyRefOrPartyRoleRef,
    ReserveBalanceRef,
    StringCharacteristic,
    TaskStateType,
    TimePeriod,
    UsageConsumptionProductRef,
    UsageConsumptionReport,
)


@pytest.fixture
def usage_consumption_report_dict():
    return {
        "@type": "UsageConsumptionReport",
        "id": "UC1",
        "href": "/tmf-api/usageConsumption/v5/usageConsumptionReport/UC1",
        "name": "Lara's consumption",
        "description": "Consumption report for Lara's mobile line",
        "creationDate": "2021-06-18T16:04:09.084Z",
        "lastUpdate": "2021-06-18T16:04:09.084Z",
        "validPeriod": {
            "startDateTime": "2021-06-01T00:00:00Z",
            "endDateTime": "2021-06-30T23:59:59Z",
        },
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "role": "Customer",
                "partyOrPartyRole": {
                    "@type": "PartyRoleRef",
                    "id": "3426",
                    "href": "/tmf-api/customerManagement/v5/customer/3426",
                    "name": "John Doe",
                    "@referredType": "Customer",
                },
            }
        ],
        "partyAccount": [
            {
                "@type": "PartyAccountRef",
                "id": "ACC-1",
                "href": "/tmf-api/accountManagement/v5/partyAccount/ACC-1",
                "name": "John Doe's account",
                "description": "Postpaid account",
                "status": "active",
                "@referredType": "PartyAccount",
            }
        ],
        "logicalResource": [
            {
                "@type": "LogicalResourceRef",
                "id": "1754",
                "name": "Lara's phone number",
                "value": "963161043",
                "@referredType": "MSISDN",
            }
        ],
        "product": [
            {
                "@type": "UsageConsumptionProductRef",
                "id": "PR1",
                "href": "/tmf-api/productInventory/v5/product/PR1",
                "name": "Lara's mobile line",
                "@referredType": "Product",
                "consumptionSummary": [
                    {
                        "@type": "ConsumptionSummary",
                        "id": "CT1",
                        "href": "/tmf-api/usageConsumption/v5/consumptionSummary/CT1",
                        "counterType": "voice",
                        "level": "global",
                        "valueName": "Unlimited",
                        "consumptionPeriod": {
                            "startDateTime": "2021-06-01T16:04:09.084Z",
                            "endDateTime": "2021-06-30T16:04:09.084Z",
                        },
                    },
                    {
                        "@type": "ConsumptionSummary",
                        "id": "CT2",
                        "counterType": "sms",
                        "level": "user",
                        "user": {
                            "@type": "RelatedPartyRefOrPartyRoleRef",
                            "role": "User",
                            "partyOrPartyRole": {
                                "@type": "PartyRef",
                                "id": "3427",
                                "name": "Lara Doe",
                                "@referredType": "Individual",
                            },
                        },
                        "value": {"amount": 42, "units": "sms"},
                        "valueName": "42 SMS",
                        "characteristic": [
                            {
                                "@type": "StringCharacteristic",
                                "name": "network",
                                "value": "home",
                            }
                        ],
                    },
                ],
            }
        ],
        "bucket": [
            {
                "@type": "Bucket",
                "id": "BK2",
                "href": "/tmf-api/balanceManagement/v5/bucket/BK2",
                "name": "RED Data Plus Bucket - Data",
                "description": "Bucket related to data",
                "usageType": "data",
                "isShared": False,
                "creationDate": "2021-06-01T00:00:00Z",
                "status": "active",
                "remainingValue": {"amount": 3, "units": "GB"},
                "remainingValueName": "3 GB",
                "reservedValue": {"amount": 1, "units": "GB"},
                "validFor": {
                    "startDateTime": "2021-06-01T00:00:00Z",
                    "endDateTime": "2021-06-30T23:59:59Z",
                },
                "bucketSpecification": {
                    "@type": "BucketSpecificationRef",
                    "id": "BS-DATA",
                    "name": "Data bucket spec",
                    "@referredType": "BucketSpecification",
                },
                "bucketRelationship": [
                    {
                        "@type": "BucketRelationship",
                        "id": "BK-PARENT",
                        "href": "/tmf-api/balanceManagement/v5/bucket/BK-PARENT",
                        "name": "Shared family data",
                        "relationshipType": "isAggregated",
                        "role": "child",
                        "@referredType": "Bucket",
                        "bucket": {
                            "@type": "BucketRef",
                            "id": "BK-PARENT",
                            "name": "Shared family data",
                            "usageType": "data",
                            "@referredType": "Bucket",
                        },
                    }
                ],
                "bucketCounter": [
                    {
                        "@type": "ConsumptionSummary",
                        "id": "CT4",
                        "counterType": "used",
                        "level": "global",
                        "consumptionPeriod": {
                            "startDateTime": "2021-06-18T16:04:09.084Z",
                            "endDateTime": "2021-06-01T16:04:09.084Z",
                        },
                        "value": {"amount": 2, "units": "GB"},
                    },
                    {
                        "@type": "BucketCounter",
                        "id": "CT5",
                        "counterType": "outOfBucket",
                        "level": "global",
                        "value": {"amount": 0, "units": "GB"},
                    },
                ],
                "reserveBalance": [
                    {
                        "@type": "ReserveBalanceRef",
                        "id": "RB-1",
                        "href": "/tmf-api/balanceManagement/v5/reserveBalance/RB-1",
                        "@referredType": "ReserveBalance",
                    }
                ],
                "product": [
                    {
                        "@type": "ProductRef",
                        "id": "PR2",
                        "name": "RED Data Plus",
                        "@referredType": "Product",
                    }
                ],
                "partyAccount": {
                    "@type": "PartyAccountRef",
                    "id": "ACC-1",
                    "name": "John Doe's account",
                    "@referredType": "PartyAccount",
                },
                "logicalResource": [
                    {
                        "@type": "LogicalResourceRef",
                        "id": "1754",
                        "value": "963161043",
                        "@referredType": "MSISDN",
                    }
                ],
                "relatedParty": [
                    {
                        "@type": "RelatedPartyRefOrPartyRoleRef",
                        "role": "Customer",
                        "partyOrPartyRole": {
                            "@type": "PartyRoleRef",
                            "id": "3426",
                            "name": "John Doe",
                            "@referredType": "Customer",
                        },
                    }
                ],
            },
            {
                "@type": "BucketRef",
                "id": "BK1",
                "href": "/tmf-api/balanceManagement/v5/bucket/BK1",
                "name": "RED MMS Plus Bucket - MMS",
                "usageType": "mms",
                "@referredType": "Bucket",
            },
        ],
    }


@pytest.fixture
def usage_consumption_report_1(usage_consumption_report_dict):
    return UsageConsumptionReport.from_dict(usage_consumption_report_dict)


@pytest.fixture
def query_usage_consumption_dict(usage_consumption_report_dict):
    return {
        "@type": "QueryUsageConsumption",
        "@baseType": "TaskResource",
        "id": "7655",
        "href": "/tmf-api/usageConsumption/v5/queryUsageConsumption/7655",
        "creationDate": "2021-06-18T16:04:09.084Z",
        "state": "done",
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "role": "Agent",
                "partyOrPartyRole": {
                    "@type": "PartyRef",
                    "id": "3426",
                    "href": "/tmf-api/partyManagement/v5/individual/3426",
                    "name": "Bob Smith",
                    "@referredType": "Individual",
                },
            }
        ],
        "partyAccount": [
            {
                "@type": "PartyAccountRef",
                "id": "ACC-1",
                "name": "John Doe's account",
                "@referredType": "PartyAccount",
            }
        ],
        "searchCriteria": {
            "@type": "UsageConsumptionReport",
            "logicalResource": [
                {
                    "@type": "LogicalResourceRef",
                    "id": "1754",
                    "name": "Lara's phone number",
                    "value": "963161043",
                    "@referredType": "MSISDN",
                }
            ],
        },
        "usageConsumption": [usage_consumption_report_dict],
        "errorMessage": [],
    }


@pytest.fixture
def query_usage_consumption_1(query_usage_consumption_dict):
    return QueryUsageConsumption.from_dict(query_usage_consumption_dict)


# --- UsageConsumptionReport ---------------------------------------------------


def test_usage_consumption_report_instantiates_with_id(usage_consumption_report_1):
    report = usage_consumption_report_1

    assert isinstance(report, UsageConsumptionReport)
    assert report.id == "UC1"
    assert report.href.endswith("/usageConsumptionReport/UC1")
    assert report.name == "Lara's consumption"
    assert report.creationDate == "2021-06-18T16:04:09.084Z"
    assert report.lastUpdate == "2021-06-18T16:04:09.084Z"
    assert isinstance(report.validPeriod, TimePeriod)
    assert report.validPeriod.endDateTime == "2021-06-30T23:59:59Z"


def test_usage_consumption_report_instantiates_parties_and_resources(
    usage_consumption_report_1,
):
    report = usage_consumption_report_1

    assert isinstance(report.relatedParty[0], RelatedPartyRefOrPartyRoleRef)
    assert report.relatedParty[0].role == "Customer"
    assert isinstance(report.relatedParty[0].partyOrPartyRole, PartyRoleRef)
    assert report.relatedParty[0].partyOrPartyRole._referred_type == "Customer"

    account = report.partyAccount[0]
    assert isinstance(account, PartyAccountRef)
    assert account.id == "ACC-1"
    assert account.description == "Postpaid account"
    assert account.status == "active"
    assert account._referred_type == "PartyAccount"

    msisdn = report.logicalResource[0]
    assert isinstance(msisdn, LogicalResourceRef)
    assert msisdn.value == "963161043"
    assert msisdn._referred_type == "MSISDN"


def test_usage_consumption_report_instantiates_product_summaries(
    usage_consumption_report_1,
):
    product = usage_consumption_report_1.product[0]

    assert isinstance(product, UsageConsumptionProductRef)
    assert isinstance(product, ProductRef)
    assert product.name == "Lara's mobile line"
    assert product._referred_type == "Product"

    voice, sms = product.consumptionSummary
    assert isinstance(voice, ConsumptionSummary)
    assert isinstance(voice, BucketCounter)
    assert voice.counterType == "voice"
    assert voice.level == "global"
    assert voice.valueName == "Unlimited"
    assert isinstance(voice.consumptionPeriod, TimePeriod)
    assert voice.consumptionPeriod.startDateTime == "2021-06-01T16:04:09.084Z"

    assert sms.counterType == "sms"
    assert sms.level == "user"
    assert isinstance(sms.user, RelatedPartyRefOrPartyRoleRef)
    assert isinstance(sms.user.partyOrPartyRole, PartyRef)
    assert sms.user.partyOrPartyRole.name == "Lara Doe"
    assert isinstance(sms.value, Quantity)
    assert sms.value.amount == 42
    assert sms.value.units == "sms"
    assert isinstance(sms.characteristic[0], StringCharacteristic)
    assert isinstance(sms.characteristic[0], Characteristic)
    assert sms.characteristic[0].value == "home"


def test_usage_consumption_report_instantiates_bucket_value_and_ref(
    usage_consumption_report_1,
):
    bucket, bucket_ref = usage_consumption_report_1.bucket

    assert isinstance(bucket, Bucket)
    assert bucket.id == "BK2"
    assert bucket.name == "RED Data Plus Bucket - Data"
    assert bucket.usageType == "data"
    assert bucket.isShared is False
    assert bucket.status is BucketStatusType.ACTIVE
    assert isinstance(bucket.remainingValue, Quantity)
    assert bucket.remainingValue.amount == 3
    assert bucket.remainingValue.units == "GB"
    assert bucket.remainingValueName == "3 GB"
    assert isinstance(bucket.reservedValue, Quantity)
    assert bucket.reservedValue.amount == 1
    assert isinstance(bucket.validFor, TimePeriod)

    assert isinstance(bucket_ref, BucketRef)
    assert bucket_ref.id == "BK1"
    assert bucket_ref.usageType == "mms"
    assert bucket_ref._referred_type == "Bucket"


def test_bucket_instantiates_nested_refs_and_counters(usage_consumption_report_1):
    bucket = usage_consumption_report_1.bucket[0]

    assert isinstance(bucket.bucketSpecification, BucketSpecificationRef)
    assert bucket.bucketSpecification.id == "BS-DATA"
    assert bucket.bucketSpecification._referred_type == "BucketSpecification"

    relationship = bucket.bucketRelationship[0]
    assert isinstance(relationship, BucketRelationship)
    assert isinstance(relationship, EntityRelationship)
    assert relationship.relationshipType == "isAggregated"
    assert relationship.role == "child"
    assert relationship.name == "Shared family data"
    assert relationship._referred_type == "Bucket"
    assert isinstance(relationship.bucket, BucketRef)
    assert relationship.bucket.usageType == "data"

    used, out_of_bucket = bucket.bucketCounter
    assert isinstance(used, ConsumptionSummary)
    assert used.counterType == "used"
    assert isinstance(used.value, Quantity)
    assert used.value.amount == 2
    assert isinstance(out_of_bucket, BucketCounter)
    assert not isinstance(out_of_bucket, ConsumptionSummary)
    assert out_of_bucket.counterType == "outOfBucket"
    assert out_of_bucket.value.amount == 0

    reserve = bucket.reserveBalance[0]
    assert isinstance(reserve, ReserveBalanceRef)
    assert isinstance(reserve, BalanceActionRef)
    assert reserve.id == "RB-1"
    assert reserve._referred_type == "ReserveBalance"

    assert isinstance(bucket.product[0], ProductRef)
    assert bucket.product[0].name == "RED Data Plus"
    assert isinstance(bucket.partyAccount, PartyAccountRef)
    assert bucket.partyAccount.id == "ACC-1"
    assert isinstance(bucket.logicalResource[0], LogicalResourceRef)
    assert bucket.logicalResource[0].value == "963161043"
    assert isinstance(bucket.relatedParty[0].partyOrPartyRole, PartyRoleRef)


def test_usage_consumption_report_defaults_to_empty_lists():
    report = UsageConsumptionReport.from_dict(
        {"@type": "UsageConsumptionReport", "id": "UC-empty"}
    )

    assert report.bucket == []
    assert report.relatedParty == []
    assert report.partyAccount == []
    assert report.product == []
    assert report.logicalResource == []
    assert report.validPeriod is None


def test_bucket_defaults_to_empty_lists():
    bucket = Bucket(id="BK-empty")

    assert bucket.relatedParty == []
    assert bucket.product == []
    assert bucket.logicalResource == []
    assert bucket.bucketRelationship == []
    assert bucket.bucketCounter == []
    assert bucket.reserveBalance == []
    assert bucket.status is None


def test_usage_consumption_report_rejects_non_list_bucket():
    with pytest.raises(ValueError):
        UsageConsumptionReport(id="UC1", bucket=BucketRef(id="BK1"))


def test_bucket_rejects_non_list_counter():
    with pytest.raises(ValueError):
        Bucket(id="BK1", bucketCounter=BucketCounter(id="CT1"))


def test_bucket_unknown_status_passes_through():
    bucket = Bucket.from_dict({"@type": "Bucket", "id": "BK1", "status": "frozen"})

    assert bucket.status == "frozen"
    assert bucket.to_dict()["status"] == "frozen"


def test_bucket_status_type_values():
    assert BucketStatusType("active") is BucketStatusType.ACTIVE
    assert BucketStatusType("suspended") is BucketStatusType.SUSPENDED
    assert BucketStatusType("expired") is BucketStatusType.EXPIRED


def test_usage_consumption_report_resource_path():
    context = Context(api_base_url="https://mycsp.com:8080/tmf-api")
    assert UsageConsumptionReport.get_resource_path(context) == (
        "https://mycsp.com:8080/tmf-api/usageConsumption/v5/usageConsumptionReport"
    )


def test_usage_consumption_report_to_dict_round_trip(usage_consumption_report_dict):
    result = UsageConsumptionReport.from_dict(usage_consumption_report_dict).to_dict()

    assert result["@type"] == "UsageConsumptionReport"
    assert "@baseType" not in result
    assert result["validPeriod"]["startDateTime"] == "2021-06-01T00:00:00Z"

    assert result["partyAccount"][0]["@type"] == "PartyAccountRef"
    assert result["partyAccount"][0]["@baseType"] == "AccountRef"
    assert result["partyAccount"][0]["@referredType"] == "PartyAccount"
    assert result["partyAccount"][0]["status"] == "active"

    assert result["logicalResource"][0]["@type"] == "LogicalResourceRef"
    assert result["logicalResource"][0]["@referredType"] == "MSISDN"
    assert result["logicalResource"][0]["value"] == "963161043"

    product = result["product"][0]
    assert product["@type"] == "UsageConsumptionProductRef"
    assert product["@baseType"] == "ProductRef"
    assert product["consumptionSummary"][0]["@type"] == "ConsumptionSummary"
    assert product["consumptionSummary"][0]["@baseType"] == "BucketCounter"
    assert product["consumptionSummary"][1]["value"]["@type"] == "Quantity"
    assert product["consumptionSummary"][1]["value"]["units"] == "sms"
    assert product["consumptionSummary"][1]["value"]["amount"] == 42
    assert (
        product["consumptionSummary"][1]["characteristic"][0]["@type"]
        == "StringCharacteristic"
    )

    bucket, bucket_ref = result["bucket"]
    assert bucket["@type"] == "Bucket"
    assert "@baseType" not in bucket
    assert bucket["status"] == "active"
    assert bucket["remainingValue"]["@type"] == "Quantity"
    assert bucket["remainingValue"]["units"] == "GB"
    assert bucket["remainingValue"]["amount"] == 3
    assert bucket["bucketSpecification"]["@type"] == "BucketSpecificationRef"
    assert bucket["bucketRelationship"][0]["@type"] == "BucketRelationship"
    assert bucket["bucketRelationship"][0]["@baseType"] == "EntityRelationship"
    assert bucket["bucketRelationship"][0]["@referredType"] == "Bucket"
    assert bucket["bucketRelationship"][0]["bucket"]["@type"] == "BucketRef"
    assert bucket["bucketCounter"][0]["@type"] == "ConsumptionSummary"
    assert bucket["bucketCounter"][1]["@type"] == "BucketCounter"
    assert "@baseType" not in bucket["bucketCounter"][1]
    assert bucket["reserveBalance"][0]["@type"] == "ReserveBalanceRef"
    assert bucket["reserveBalance"][0]["@baseType"] == "BalanceActionRef"
    assert bucket["reserveBalance"][0]["@referredType"] == "ReserveBalance"
    assert bucket["partyAccount"]["@type"] == "PartyAccountRef"

    assert bucket_ref["@type"] == "BucketRef"
    assert bucket_ref["@referredType"] == "Bucket"
    assert bucket_ref["usageType"] == "mms"


# --- QueryUsageConsumption ----------------------------------------------------


def test_query_usage_consumption_instantiates_with_id(query_usage_consumption_1):
    task = query_usage_consumption_1

    assert isinstance(task, QueryUsageConsumption)
    assert task.id == "7655"
    assert task.href.endswith("/queryUsageConsumption/7655")
    assert task.creationDate == "2021-06-18T16:04:09.084Z"
    assert task.state is TaskStateType.DONE
    assert task.errorMessage == []


def test_query_usage_consumption_instantiates_parties(query_usage_consumption_1):
    task = query_usage_consumption_1

    assert isinstance(task.relatedParty[0], RelatedPartyRefOrPartyRoleRef)
    assert task.relatedParty[0].role == "Agent"
    assert isinstance(task.relatedParty[0].partyOrPartyRole, PartyRef)
    assert task.relatedParty[0].partyOrPartyRole.name == "Bob Smith"
    assert task.relatedParty[0].partyOrPartyRole._referred_type == "Individual"

    assert isinstance(task.partyAccount[0], PartyAccountRef)
    assert task.partyAccount[0].id == "ACC-1"


def test_query_usage_consumption_instantiates_search_criteria(
    query_usage_consumption_1,
):
    criteria = query_usage_consumption_1.searchCriteria

    assert isinstance(criteria, UsageConsumptionReport)
    assert criteria.id is None
    assert criteria.bucket == []
    assert isinstance(criteria.logicalResource[0], LogicalResourceRef)
    assert criteria.logicalResource[0].value == "963161043"
    assert criteria.logicalResource[0]._referred_type == "MSISDN"


def test_query_usage_consumption_instantiates_reports(query_usage_consumption_1):
    reports = query_usage_consumption_1.usageConsumption

    assert len(reports) == 1
    report = reports[0]
    assert isinstance(report, UsageConsumptionReport)
    assert report.id == "UC1"
    assert isinstance(report.bucket[0], Bucket)
    assert isinstance(report.bucket[1], BucketRef)
    assert isinstance(report.product[0], UsageConsumptionProductRef)
    assert isinstance(report.product[0].consumptionSummary[0], ConsumptionSummary)


def test_query_usage_consumption_defaults_to_empty_lists():
    task = QueryUsageConsumption.from_dict(
        {"@type": "QueryUsageConsumption", "id": "q-1", "state": "inProgress"}
    )

    assert task.usageConsumption == []
    assert task.relatedParty == []
    assert task.partyAccount == []
    assert task.errorMessage == []
    assert task.searchCriteria is None
    assert task.state is TaskStateType.IN_PROGRESS


def test_query_usage_consumption_rejects_non_list_reports():
    with pytest.raises(ValueError):
        QueryUsageConsumption(
            id="q-1", usageConsumption=UsageConsumptionReport(id="UC1")
        )


def test_query_usage_consumption_unknown_state_passes_through(
    query_usage_consumption_dict,
):
    query_usage_consumption_dict = dict(query_usage_consumption_dict, state="queued")
    task = QueryUsageConsumption.from_dict(query_usage_consumption_dict)

    assert task.state == "queued"
    assert task.to_dict()["state"] == "queued"


def test_query_usage_consumption_resource_path():
    context = Context(api_base_url="https://mycsp.com:8080/tmf-api")
    assert QueryUsageConsumption.get_resource_path(context) == (
        "https://mycsp.com:8080/tmf-api/usageConsumption/v5/queryUsageConsumption"
    )


def test_query_usage_consumption_to_dict_round_trip(query_usage_consumption_dict):
    result = QueryUsageConsumption.from_dict(query_usage_consumption_dict).to_dict()

    assert result["@type"] == "QueryUsageConsumption"
    assert result["@baseType"] == "TaskResource"
    assert result["state"] == "done"
    assert result["creationDate"] == "2021-06-18T16:04:09.084Z"
    assert "errorMessage" not in result

    assert result["relatedParty"][0]["partyOrPartyRole"]["@type"] == "PartyRef"
    assert (
        result["relatedParty"][0]["partyOrPartyRole"]["@referredType"] == "Individual"
    )
    assert result["partyAccount"][0]["@type"] == "PartyAccountRef"

    assert result["searchCriteria"]["@type"] == "UsageConsumptionReport"
    assert "id" not in result["searchCriteria"]
    assert result["searchCriteria"]["logicalResource"][0]["@referredType"] == "MSISDN"

    report = result["usageConsumption"][0]
    assert report["@type"] == "UsageConsumptionReport"
    assert report["bucket"][0]["@type"] == "Bucket"
    assert report["bucket"][0]["status"] == "active"
    assert report["bucket"][1]["@type"] == "BucketRef"
    assert report["product"][0]["@type"] == "UsageConsumptionProductRef"
    assert (
        report["product"][0]["consumptionSummary"][0]["@type"] == "ConsumptionSummary"
    )
