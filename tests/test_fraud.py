import pytest
from tmforum import (
    ContactType,
    Context,
    Duration,
    EmailContactMedium,
    EvaluateFraudRisk,
    FraudEvaluationCriteria,
    FraudEvaluationResult,
    FraudNetworkAuthenticationCriteria,
    FraudNetworkAuthenticationResult,
    FraudProfileMatchCriteria,
    FraudProfileMatchResult,
    FraudRiskProfileCriteria,
    FraudRiskProfileResult,
    FraudScoreCriteria,
    FraudScoreResult,
    GeographicAddressContactMedium,
    GeographicAddressRef,
    PartyRef,
    PaymentMethodRef,
    PhoneContactMedium,
    ProfileMatch,
    RelatedPartyRefOrPartyRoleRef,
    ServiceStateType,
    TaskStateType,
    TimePeriod,
    WebFormContactMedium,
)


@pytest.fixture
def evaluate_fraud_risk_dict():
    return {
        "@type": "EvaluateFraudRisk",
        "@baseType": "TaskResource",
        "id": "f3a34f89-0046-tsk-01",
        "href": "/tmf-api/fraudManagement/v5/evaluateFraudRisk/f3a34f89-0046-tsk-01",
        "requestedFraudEvaluationDate": "2024-11-20T09:34:58Z",
        "state": "done",
        "fraudTargetIdentifier": [
            {
                "@type": "PhoneContactMedium",
                "@baseType": "ContactMedium",
                "phoneNumber": "01 09 75 83 51",
            },
            {
                "@type": "WebFormContactMedium",
                "@baseType": "ContactMedium",
                "url": "https://mycsp.com/contact/f3a34f89",
            },
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "role": "Merchant",
                "partyOrPartyRole": {
                    "@type": "PartyRef",
                    "id": "f3a34f89-0046-pty-01",
                    "href": (
                        "/tmf-api/partyManagement/v5/Organization/f3a34f89-0046-pty-01"
                    ),
                    "name": "Bank XYZ",
                    "@referredType": "Organization",
                },
            }
        ],
        "fraudEvaluationCriteria": {
            "@type": "FraudEvaluationCriteria",
            "fraudRiskProfileCriteria": {
                "@type": "FraudRiskProfileCriteria",
                "simTenure": False,
                "deviceTenure": True,
                "lineTenure": False,
                "paymentMethod": False,
                "callForwarding": True,
                "serviceStatus": True,
                "simSwap": False,
            },
            "fraudNetworkAuthenticationCriteria": {
                "@type": "FraudNetworkAuthenticationCriteria",
                "callVerification": False,
            },
            "fraudScoreCriteria": {
                "@type": "FraudScoreCriteria",
                "isExplanationRequired": True,
            },
            "fraudProfileMatchCriteria": {
                "@type": "FraudProfileMatchCriteria",
                "email": {
                    "@type": "EmailContactMedium",
                    "@baseType": "ContactMedium",
                    "emailAddress": "neo@matrix.com",
                },
                "partyName": "Joe Doe",
                "address": {
                    "@type": "GeographicAddressContactMedium",
                    "@baseType": "ContactMedium",
                    "id": "address-001",
                    "preferred": True,
                    "contactType": "personal",
                    "validFor": {
                        "startDateTime": "2025-01-29T10:40:52Z",
                        "endDateTime": "2025-07-29T10:40:52Z",
                    },
                    "city": "Gurgaon",
                    "country": "India",
                    "postCode": "121001",
                    "stateOrProvince": "Harayana",
                    "street1": "Sector 39",
                    "street2": "Near Unitech cyber park",
                    "geographicAddress": {
                        "@type": "GeographicAddressRef",
                        "id": "35dcfeec-9051-4b05-830e7a0f67dc541d",
                        "href": (
                            "/tmf-api/geographicAddressManagement/v5"
                            "/geographicAddress/35dcfeec-9051-4b05-830e7a0f67dc541d"
                        ),
                        "name": "address1",
                        "@referredType": "GeographicAddress",
                    },
                },
            },
        },
        "fraudEvaluationResult": {
            "@type": "FraudEvaluationResult",
            "fraudRiskProfileResult": {
                "@type": "FraudRiskProfileResult",
                "simTenure": {"units": "month", "amount": 120},
                "deviceTenure": {"units": "month", "amount": 48},
                "lineTenure": {"units": "month", "amount": 120},
                "paymentMethod": {
                    "@type": "PaymentMethodRef",
                    "id": "pm-cc-01",
                    "name": "Credit Card",
                    "@referredType": "BankCard",
                },
                "callForwardingStatus": True,
                "serviceStatus": "active",
                "role": "Admin",
                "simSwapStatus": False,
            },
            "fraudNetworkAuthenticationResult": {
                "@type": "FraudNetworkAuthenticationResult",
                "callVerification": "VERIFIED",
            },
            "fraudScoreResult": {
                "@type": "FraudScoreResult",
                "score": "70",
                "explanation": "Credit Score low",
            },
            "fraudProfileMatchResult": {
                "@type": "FraudProfileMatchResult",
                "globalMatchScore": "90",
                "profileMatch": [
                    {
                        "@type": "ProfileMatch",
                        "matchElement": "name",
                        "matchScore": "90",
                    }
                ],
            },
        },
        "errorMessage": [],
    }


@pytest.fixture
def evaluate_fraud_risk_1(evaluate_fraud_risk_dict):
    return EvaluateFraudRisk.from_dict(evaluate_fraud_risk_dict)


def test_evaluate_fraud_risk_instantiates_with_id(evaluate_fraud_risk_dict):
    task = EvaluateFraudRisk.from_dict(evaluate_fraud_risk_dict)

    assert isinstance(task, EvaluateFraudRisk)
    assert task.id == "f3a34f89-0046-tsk-01"
    assert task.href.endswith("/evaluateFraudRisk/f3a34f89-0046-tsk-01")
    assert task.requestedFraudEvaluationDate == "2024-11-20T09:34:58Z"
    assert task.state is TaskStateType.DONE


def test_evaluate_fraud_risk_instantiates_target_and_parties(evaluate_fraud_risk_1):
    task = evaluate_fraud_risk_1

    phone, web_form = task.fraudTargetIdentifier
    assert isinstance(phone, PhoneContactMedium)
    assert phone.phoneNumber == "01 09 75 83 51"
    assert isinstance(web_form, WebFormContactMedium)
    assert web_form.url == "https://mycsp.com/contact/f3a34f89"

    assert isinstance(task.relatedParty[0], RelatedPartyRefOrPartyRoleRef)
    assert task.relatedParty[0].role == "Merchant"
    assert isinstance(task.relatedParty[0].partyOrPartyRole, PartyRef)
    assert task.relatedParty[0].partyOrPartyRole.name == "Bank XYZ"
    assert task.relatedParty[0].partyOrPartyRole._referred_type == "Organization"


def test_evaluate_fraud_risk_instantiates_criteria(evaluate_fraud_risk_1):
    criteria = evaluate_fraud_risk_1.fraudEvaluationCriteria

    assert isinstance(criteria, FraudEvaluationCriteria)

    assert isinstance(criteria.fraudRiskProfileCriteria, FraudRiskProfileCriteria)
    assert criteria.fraudRiskProfileCriteria.deviceTenure is True
    assert criteria.fraudRiskProfileCriteria.simSwap is False

    assert isinstance(
        criteria.fraudNetworkAuthenticationCriteria,
        FraudNetworkAuthenticationCriteria,
    )
    assert criteria.fraudNetworkAuthenticationCriteria.callVerification is False

    assert isinstance(criteria.fraudScoreCriteria, FraudScoreCriteria)
    assert criteria.fraudScoreCriteria.isExplanationRequired is True

    match_criteria = criteria.fraudProfileMatchCriteria
    assert isinstance(match_criteria, FraudProfileMatchCriteria)
    assert match_criteria.partyName == "Joe Doe"
    assert isinstance(match_criteria.email, EmailContactMedium)
    assert match_criteria.email.emailAddress == "neo@matrix.com"
    assert isinstance(match_criteria.address, GeographicAddressContactMedium)
    assert match_criteria.address.city == "Gurgaon"
    assert match_criteria.address.contactType is ContactType.PERSONAL
    assert isinstance(match_criteria.address.validFor, TimePeriod)
    assert isinstance(match_criteria.address.geographicAddress, GeographicAddressRef)
    assert match_criteria.address.geographicAddress.name == "address1"


def test_evaluate_fraud_risk_instantiates_result(evaluate_fraud_risk_1):
    result = evaluate_fraud_risk_1.fraudEvaluationResult

    assert isinstance(result, FraudEvaluationResult)

    profile = result.fraudRiskProfileResult
    assert isinstance(profile, FraudRiskProfileResult)
    assert isinstance(profile.simTenure, Duration)
    assert profile.simTenure.amount == 120
    assert profile.simTenure.units == "month"
    assert isinstance(profile.deviceTenure, Duration)
    assert profile.deviceTenure.amount == 48
    assert isinstance(profile.lineTenure, Duration)
    assert isinstance(profile.paymentMethod, PaymentMethodRef)
    assert profile.paymentMethod._referred_type == "BankCard"
    assert profile.callForwardingStatus is True
    assert profile.serviceStatus is ServiceStateType.ACTIVE
    assert profile.role == "Admin"
    assert profile.simSwapStatus is False

    assert isinstance(
        result.fraudNetworkAuthenticationResult, FraudNetworkAuthenticationResult
    )
    assert result.fraudNetworkAuthenticationResult.callVerification == "VERIFIED"

    assert isinstance(result.fraudScoreResult, FraudScoreResult)
    assert result.fraudScoreResult.score == "70"
    assert result.fraudScoreResult.explanation == "Credit Score low"

    match_result = result.fraudProfileMatchResult
    assert isinstance(match_result, FraudProfileMatchResult)
    assert match_result.globalMatchScore == "90"
    assert isinstance(match_result.profileMatch[0], ProfileMatch)
    assert match_result.profileMatch[0].matchElement == "name"
    assert match_result.profileMatch[0].matchScore == "90"


def test_evaluate_fraud_risk_defaults_to_empty_lists():
    task = EvaluateFraudRisk.from_dict(
        {"@type": "EvaluateFraudRisk", "id": "tsk-1", "state": "inProgress"}
    )

    assert task.fraudTargetIdentifier == []
    assert task.relatedParty == []
    assert task.errorMessage == []
    assert task.fraudEvaluationCriteria is None
    assert task.fraudEvaluationResult is None
    assert task.state is TaskStateType.IN_PROGRESS


def test_evaluate_fraud_risk_rejects_non_list_target_identifier():
    with pytest.raises(ValueError):
        EvaluateFraudRisk(
            id="tsk-1",
            fraudTargetIdentifier=PhoneContactMedium(phoneNumber="01 09 75 83 51"),
        )


def test_evaluate_fraud_risk_unknown_state_passes_through(evaluate_fraud_risk_dict):
    evaluate_fraud_risk_dict = dict(evaluate_fraud_risk_dict, state="pendingReview")
    task = EvaluateFraudRisk.from_dict(evaluate_fraud_risk_dict)

    assert task.state == "pendingReview"
    assert task.to_dict()["state"] == "pendingReview"


def test_service_state_type_covers_pending_states():
    assert ServiceStateType("created") is ServiceStateType.CREATED
    assert ServiceStateType("pendingActive") is ServiceStateType.PENDING_ACTIVE
    assert ServiceStateType("pendingTerminate") is ServiceStateType.PENDING_TERMINATE


def test_evaluate_fraud_risk_resource_path():
    context = Context(api_base_url="https://mycsp.com:8080/tmf-api")
    assert EvaluateFraudRisk.get_resource_path(context) == (
        "https://mycsp.com:8080/tmf-api/fraudManagement/v5/evaluateFraudRisk"
    )


def test_evaluate_fraud_risk_to_dict_round_trip(evaluate_fraud_risk_dict):
    result = EvaluateFraudRisk.from_dict(evaluate_fraud_risk_dict).to_dict()

    assert result["@type"] == "EvaluateFraudRisk"
    assert result["@baseType"] == "TaskResource"
    assert result["state"] == "done"
    assert result["fraudTargetIdentifier"][0]["@type"] == "PhoneContactMedium"
    assert result["fraudTargetIdentifier"][1]["@type"] == "WebFormContactMedium"
    assert result["relatedParty"][0]["partyOrPartyRole"]["@type"] == "PartyRef"
    assert (
        result["relatedParty"][0]["partyOrPartyRole"]["@referredType"] == "Organization"
    )
    assert (
        result["fraudEvaluationCriteria"]["fraudProfileMatchCriteria"]["address"][
            "contactType"
        ]
        == "personal"
    )
    assert (
        result["fraudEvaluationResult"]["fraudRiskProfileResult"]["serviceStatus"]
        == "active"
    )
    assert (
        result["fraudEvaluationResult"]["fraudRiskProfileResult"]["simTenure"]["amount"]
        == 120
    )
    assert (
        result["fraudEvaluationResult"]["fraudProfileMatchResult"]["profileMatch"][0][
            "matchScore"
        ]
        == "90"
    )
