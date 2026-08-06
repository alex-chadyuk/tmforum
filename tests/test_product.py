import pytest
from tmforum import (
    AccountBalance,
    AppliedBillingTaxRate,
    AppliedCustomerBillingRate,
    AppliedCustomerBillingRateType,
    BalanceType,
    BillingAccount,
    BillingAccountRef,
    BillingCycleSpecification,
    BillPresentationMedia,
    BillStructure,
    BundledProductOffering,
    BundledProductSpecification,
    BundledProductOfferingOption,
    Category,
    ChannelRef,
    ChargeType,
    CheckProductConfiguration,
    CheckProductConfigurationItem,
    CheckProductConfigurationItemState,
    ConfigurationAction,
    ConfigurationTerm,
    CustomerBillRef,
    Duration,
    EmailContactMedium,
    GeographicAddressContactMedium,
    Individual,
    IndividualRef,
    ItemActionType,
    LifecycleStatus,
    Money,
    OrderItemRelationship,
    OrderPrice,
    OrderTerm,
    Organization,
    Party,
    PartyRef,
    Price,
    PriceAlteration,
    PriceType,
    Product,
    ProductActionType,
    ProductConfiguration,
    ProductConfigurationItemRelationship,
    ProductOffering,
    ProductOfferingPrice,
    ProductOfferingRef,
    ProductOfferingPriceRef,
    ProductOrder,
    ProductOrderItem,
    ProductOrderItemRef,
    ProductOrderItemRelationshipType,
    ProductOrderRef,
    ProductRelationshipType,
    ProductPrice,
    ProductRef,
    ProductSpecification,
    ProductSpecificationRelationship,
    ProductStatusType,
    ProductTerm,
    BillingAccountRef,
    RatePlanProduct,
    RecurringChargePeriod,
    RelatedChannel,
    RelatedPartyRefOrPartyRoleRef,
    RenewalAction,
    RoleEnum,
    TaskStateType,
    TaxCategory,
    TimePeriod,
)


@pytest.fixture
def product_dict():
    product = {
        "@type": "Product",
        "id": "edb3d35b-a60d-40c2-994b-e7489053d71a",
        "@baseType": "Entity",
        "description": "Pendrick Demo Product",
        "href": "/Product/edb3d35b-a60d-40c2-994b-e7489053d71a",
        "isBundle": False,
        "name": "Pendrick Internet",
        "product": [],
        "quantity": 1,
        "startDate": "2024-11-28T19:52:58Z",
        "status": "active",
        "terminationDate": "2025-11-28T19:52:58Z",
        "createOn": "2024-11-28T19:52:57.372Z",
        "lastUpdate": "2024-11-28T19:52:58.571Z",
        "billingAccount": {
            "@type": "BillingAccountRef",
            "id": "89827405-1463-4a63-8804-38af97daaa87",
            "@baseType": "Entity",
        },
        "realizingResource": [],
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "id": "98fc24fd-3e0e-4630-8fec-c0f745c08b9b",
                "@baseType": "Entity",
            }
        ],
        "realizingService": [],
        "place": [],
        "productTerm": [
            {
                "@type": "ProductTerm",
                "id": "a9ae577f-8699-496f-b5dc-c6214e9ab65f",
                "@baseType": "Entity",
                "duration": {
                    "@type": "Duration",
                    "@baseType": "Entity",
                    "units": "months",
                    "amount": 12,
                },
                "expiryNotificationPeriod": {
                    "@type": "Duration",
                    "@baseType": "Entity",
                    "units": "months",
                    "amount": 1,
                },
                "name": "Flexible Daily",
                "renewalAction": "manualRepurchase",
                "validFor": {
                    "startDateTime": "2024-11-28T19:52:58Z",
                    "endDateTime": "2025-11-28T19:52:58Z",
                },
            }
        ],
        "agreementItem": [],
        "productCharacteristic": [],
        "productOffering": {
            "@type": "ProductOfferingRef",
            "id": "4005333b-dbf7-4504-a888-436a4897d252",
            "@baseType": "Entity",
        },
        "productOrderItem": [],
        "productPrice": [
            {
                "@type": "ProductPrice",
                "id": "b5a491ef-20d4-467d-8b14-cfd714d0194d",
                "@baseType": "Entity",
                "chargeType": "inAdvance",
                "description": "Price for Pendrick product",
                "name": "Pendrick Internet Price",
                "priceType": "recurringCharge",
                "recurringChargePeriod": "monthly",
                "unitOfMeasure": "month",
                "priceAlteration": [
                    {
                        "@type": "PriceAlteration",
                        "id": "f7dfadf9-81df-4be5-bf20-76c6eb25639a",
                        "@baseType": "Entity",
                        "applicationDuration": 10,
                        "description": "Discount",
                        "isPercentage": True,
                        "priceType": "discount",
                        "priority": 10,
                        "recurringChargePeriod": "monthly",
                        "unitOfMeasure": "month",
                        "productOfferingPrice": {
                            "@type": "ProductOfferingPriceRef",
                            "id": "4b2585aa-3a7c-49bc-87fe-c80f54693587",
                            "@baseType": "Entity",
                        },
                        "price": {
                            "@type": "Price",
                            "id": "e55aa169-0115-4937-b257-3768957a698a",
                            "@baseType": "Entity",
                            "percentage": 12.5,
                        },
                    }
                ],
                "price": {
                    "@type": "Price",
                    "id": "9d6155b6-cb6e-45ad-99d5-081b9aa797f1",
                    "@baseType": "Entity",
                    "dutyFreeAmount": {
                        "@type": "Money",
                        "@baseType": "Entity",
                        "unit": "USD",
                        "value": 29.95,
                    },
                },
                "productOfferingPrice": {
                    "@type": "ProductOfferingPriceRef",
                    "id": "4b2585aa-3a7c-49bc-87fe-c80f54693587",
                    "@baseType": "Entity",
                },
            }
        ],
        "productRelationship": [],
        "externalId": [],
    }
    return product


@pytest.fixture
def product_1(product_dict):
    return Product.from_dict(product_dict)


@pytest.fixture
def rate_plan_product():
    rate_plan_product = {
        "@type": "RatePlanProduct",
        "name": "Test Rate Plan Product",
        "quantity": 1,
        "status": "active",
        "productPrice": [
            {
                "@type": "ProductPrice",
                "name": "Test Price",
                "priceType": "recurringCharge",
                "chargeType": "inAdvance",
                "recurringChargePeriod": "monthly",
                "price": {
                    "@type": "Price",
                    "dutyFreeAmount": {
                        "@type": "Money",
                        "unit": "USD",
                        "value": 29.95,
                    },
                },
            }
        ],
        "billingAccount": {
            "@type": "BillingAccountRef",
            "id": "test-billing-account-id",
        },
    }
    return rate_plan_product

@pytest.fixture
def product_offering_1():
    po = {
        "id": "08b88d3a-80d5-4da2-a8d9-a0dadddb06f6",
        "@type": "ProductOffering",
        "attachment": [],
        "href": "/ProductOffering/08b88d3a-80d5-4da2-a8d9-a0dadddb06f6",
        "isBundle": False,
        "lifecycleStatus": "active",
        "minimumCardinality": 1,
        "name": "PO 1",
        "productOfferingPrice": [
            {
                "@type": "ProductOfferingPriceRef",
                "id": "77044b26-dd4f-451b-b7bd-7eb9ef1e2605",
                "name": "One Time Charge",
            },
            {
                "@type": "ProductOfferingPrice",
                "id": "4b572ccd-60ab-46e9-82ca-8b4184d76aaf",
                "name": "One Time Charge for change",
                "validFor": {},
                "lifecycleStatus": "active",
                "priceType": "discount",
                "popRelationship": [
                    {
                        "name": "One Time Charge",
                        "id": "77044b26-dd4f-451b-b7bd-7eb9ef1e2605",
                        "relationshipType": "discount",
                        "@type": "ProductOfferingPriceRef",
                    }
                ],
                "isPercentage": False,
                "price": {"value": "1", "unit": "CAD"},
                "tax": [],
                "prodSpecCharValueUse": [],
            },
            {
                "@type": "ProductOfferingPrice",
                "id": "aa507729-e6ef-4ba0-a6f8-5a614b74c492",
                "name": "Recurring Charge",
                "validFor": {},
                "lifecycleStatus": "active",
                "priceType": "recurringCharge",
                "recurringChargePeriodType": "month",
                "recurringChargePeriodLength": "20",
                "price": {"value": "10", "unit": "USD"},
                "chargeType": "inAdvance",
                "isRange": True,
                "lowerValueLimit": "9",
                "tax": [],
                "prodSpecCharValueUse": [],
                "productOfferingTerm": [
                    {
                        "id": "cdc2695a-8e37-4974-ac9e-d73e05c0e03e",
                        "duration": {"amount": 12, "units": "month"},
                        "expiryNotificationPeriod": {"amount": 1, "units": "month"},
                        "name": "12 months",
                        "renewalAction": "autoRenew",
                        "@type": "ProductOfferingTerm",
                    }
                ],
            },
        ],
        "validFor": {
            "startDateTime": "2024-08-08T08:24:22.572Z",
            "endDateTime": "3024-08-08T08:24:22.577Z",
        },
        "version": "v1",
        "createOn": "2024-08-08T08:24:23.323Z",
        "lastUpdate": "2024-12-05T08:37:35.576Z",
        "productSpecification": {
            "id": "81ba41ef-5a29-4672-9c1d-6c805f9ec72e",
            "@type": "ProductSpecificationRef",
            "name": "PS 1 Internal provider",
        },
        "allowedAction": [],
        "productOfferingRelationship": [],
        "productOfferingCharacteristic": [],
        "bundledProductOffering": [],
        "channel": [],
        "place": [
            {
                "id": "fe83a9c1-2b3e-49bf-a269-fb0b8688da05",
                "@type": "PlaceRef",
                "name": "China",
            }
        ],
        "marketSegment": [
            {
                "id": "ea77f664-0020-4d3c-9cb6-21ad4caf8435",
                "@type": "MarketSegmentRef",
                "name": "Enterprise Companies",
            }
        ],
        "policy": [],
        "category": [
            {
                "id": "5c7e4d1d-7b3d-450b-9ef1-5329dd0615eb",
                "@type": "CategoryRef",
                "name": "zhiqiang_categorg01",
            }
        ],
        "productOfferingTerm": [
            {
                "id": "76202563-7721-47e7-942b-1c4f6761345b",
                "@type": "ProductOfferingTerm",
                "duration": {"amount": 24, "units": "month"},
                "expiryNotificationPeriod": {"amount": 1, "units": "month"},
                "name": "24 months",
                "renewalAction": "autoRenew",
            },
            {
                "id": "cdc2695a-8e37-4974-ac9e-d73e05c0e03e",
                "@type": "ProductOfferingTerm",
                "duration": {"amount": 12, "units": "month"},
                "expiryNotificationPeriod": {"amount": 1, "units": "month"},
                "name": "12 months",
                "renewalAction": "autoRenew",
            },
        ],
        "agreement": [],
        "bundledGroupProductOffering": [],
        "prodSpecCharValueUse": [
            {
                "id": "476255c2-a158-43f9-8288-879d4adb1309",
                "@type": "ProductSpecificationCharacteristicValueUse",
                "name": "C1 value 2",
                "characteristicSpecificationRef": {
                    "id": "7b0b485a-a43e-4111-a984-8303f002d5be",
                    "@type": "CharacteristicSpecificationRef",
                },
                "productSpecCharacteristicValue": [],
            },
            {
                "id": "9545c46e-ee98-4af0-a6ad-92249a76a09c",
                "@type": "ProductSpecificationCharacteristicValueUse",
                "name": "C1 value 1",
                "characteristicSpecificationRef": {
                    "id": "90215d7a-962a-47b7-9413-7bf5a6354da9",
                    "@type": "CharacteristicSpecificationRef",
                },
                "productSpecCharacteristicValue": [],
            },
        ],
        "externalIdentifier": [],
    }

    return ProductOffering.from_dict(po)


@pytest.fixture
def pconf_1():
    pconf = {
        "@type": "CheckProductConfiguration",
        "@baseType": "Entity",
        "instantSync": True,
        "provideAlternatives": False,
        "contextCharacteristic": [],
        "checkProductConfigurationItem": [
            {
                "@type": "CheckProductConfigurationItem",
                "@baseType": "Entity",
                "id": "001",
                "stateReason": [],
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
                "alternateProductConfigurationProposal": [],
                "productConfigurationItemRelationship": [],
                "productConfigurationItem": [],
                "state": "approved",
            }
        ],
        "relatedParty": [],
        "state": "done",
    }
    return CheckProductConfiguration.from_dict(pconf)


@pytest.fixture
def acbr_1():
    acbr = {
        "@type": "AppliedCustomerBillingRate",
        "@baseType": "Entity",
        "appliedBillingRateType": "appliedBillingChargeProductRecurringCharge",
        "date": "2024-12-14T12:36:08.885Z",
        "name": "Shenandoah River Cabin",
        "periodCoverage": {
            "startDateTime": "2024-12-14T12:36:08.885Z",
            "endDateTime": "2024-12-14T12:36:08.885Z",
        },
        "taxExcludedAmount": {"unit": "USD", "value": 9.95},
        "taxIncludedAmount": {"value": 11.144, "unit": "USD"},
        "billingAccount": {
            "@type": "BillingAccountRef",
            "@referredType": "BillingAccount",
            "id": "249acecb-6420-4764-b6df-e831c87f036f",
        },
        "description": "Shenandoah River Cabin - Product 3",
        "id": "1be3cdba-beb6-4f72-bc39-b8cc99d60d9c",
        "href": "/AppliedCustomerBillingRate/1be3cdba-beb6-4f72-bc39-b8cc99d60d9c",
        "product": {
            "@type": "ProductRef",
            "@referredType": "Product",
            "id": "30c07084-b641-4162-8a84-a740956479cd",
            "name": "Product Three",
        },
        "appliedTax": [
            {
                "@type": "AppliedBillingTaxRate",
                "@baseType": "Entity",
                "taxAmount": {"value": 1.194},
                "taxCategory": "VAT",
                "taxRate": 12,
                "id": "7b53bb88-0a64-45d2-a854-d998eecb56a1",
            }
        ],
        "isBilled": False,
    }
    return AppliedCustomerBillingRate.from_dict(acbr)


@pytest.fixture
def bill_acct_1():
    bill_acct = {
        "id": "fc5ac257-3072-475b-8a2c-70f00e72ede7",
        "@type": "BillingAccount",
        "generateEmptyBill": False,
        "name": "Billing Account [Charter Demo Dec 9]",
        "nextBillNo": "1",
        "state": "created",
        "createOn": "2024-12-15T13:37:14.210Z",
        "lastUpdate": "2024-12-15T13:37:14.210Z",
        "relatedParty": [
            {
                "id": "aa1a6427-86fa-4eb4-80b4-668cb26f6382",
                "@type": "PartyRef",
                "partyOrPartyRole": {
                    "id": "ebdc06b0-176b-4155-aacc-c794000d21c0",
                    "@referredType": "Organization",
                    "@type": "OrganizationRef",
                    "name": "Parent Organization",
                    "characteristic": [
                        {
                            "@type": "StringCharacteristic",
                            "name": "TIN",
                            "valueType": "string",
                            "value": "123456",
                        }
                    ],
                },
                "role": "owner",
            }
        ],
        "billStructure": {
            "id": "8b272213-f11b-45f0-b388-e1d26493990c",
            "@type": "BillStructure",
            "cycleSpecification": {
                "id": "7819e772-2607-46ae-8c3b-1fde17c59f97",
                "name": "name-7819e772-2607-46ae-8c3b-1fde17c59f97",
                "@type": "BillingCycleSpecification",
            },
            "format": {
                "name": "format",
                "@type": "BillFormat",
                "templateEngine": "LF-DE",
                "templateHref": "StagingCreedTemplate",
                "basePresentationType": "rendered",
            },
            "presentationMedia": [
                {
                    "name": "email",
                    "@type": "BillPresentationMedia",
                    "basePresentationType": "rendered",
                }
            ],
        },
        "financialAccount": {"id": "50a4f2fd-fdcf-4a94-aaad-94f0aca5d254"},
        "externalIdentifier": [
            {"id": "a27d1eff7dae4032a9a7503e0e8aaee4", "externalIdentifierType": "DNO"},
            {"id": "412243776", "externalIdentifierType": "ExternalAccountID"},
        ],
        "taxExemption": [],
        "contact": [
            {
                "id": "c86dc3a5-002b-4e51-9b10-ba7da0aa2e07",
                "@type": "Contact",
                "contactName": "Mister Primary Caretaker",
                "contactType": "billingAddress",
                "contactMedium": [
                    {
                        "id": "7ea5badd-ece9-4f07-bcd8-7dea2a1001b5",
                        "@baseType": "ContactMedium",
                        "@type": "GeographicAddressContactMedium",
                        "preferred": True,
                        "city": "Fleet City",
                        "country": "Canada",
                        "postCode": "A1A 1A1",
                        "stateOrProvince": "ON",
                        "street1": "123 Fleet St",
                        "street2": "Unit 123",
                    },
                    {
                        "id": "dbe14b32-85d4-463b-a906-7c1f0826b552",
                        "@baseType": "ContactMedium",
                        "@type": "EmailContactMedium",
                        "contactType": "email",
                        "preferred": True,
                        "emailAddress": "nonexistent@example.com",
                    },
                ],
            }
        ],
        "accountBalance": [
            {
                "id": "f1305884-087c-4c64-9447-ecd03f468d49",
                "amount": {"value": 0, "unit": "USD"},
                "balanceType": "payableBalance",
                "validFor": {
                    "startDateTime": "2024-06-01",
                    "endDateTime": "2029-06-01",
                },
            }
        ],
        "accountRelationship": [],
        "paymentPlan": [],
        "href": "/BillingAccount/fc5ac257-3072-475b-8a2c-70f00e72ede7",
    }
    return BillingAccount.from_dict(bill_acct)


def test_product_instantiates_with_id(product_dict):
    product = Product.from_dict(product_dict)
    assert product.id == "edb3d35b-a60d-40c2-994b-e7489053d71a"
    assert product.productPrice[0].priceAlteration[0].price.percentage == 12.5


def test_product_instantiates_classes(product_1):
    prod_term = product_1.productTerm[0]
    prod_price = product_1.productPrice[0]
    price_alt = prod_price.priceAlteration[0]
    assert isinstance(product_1.billingAccount, BillingAccountRef)
    assert isinstance(product_1.relatedParty[0], RelatedPartyRefOrPartyRoleRef)
    assert isinstance(prod_term, ProductTerm)
    assert isinstance(prod_term.duration, Duration)
    assert isinstance(prod_term.validFor, TimePeriod)
    assert isinstance(prod_term.renewalAction, RenewalAction)
    assert isinstance(product_1.productOffering, ProductOfferingRef)
    assert isinstance(prod_price, ProductPrice)
    assert isinstance(prod_price.productOfferingPrice, ProductOfferingPriceRef)
    assert isinstance(prod_price.price, Price)
    assert isinstance(prod_price.chargeType, ChargeType)
    assert isinstance(prod_price.price.dutyFreeAmount, Money)
    assert isinstance(price_alt, PriceAlteration)
    assert isinstance(price_alt.price, Price)
    assert isinstance(price_alt.productOfferingPrice, ProductOfferingPriceRef)
    assert isinstance(price_alt.recurringChargePeriod, RecurringChargePeriod)


def test_product_offering_instantiates_classes(product_offering_1):
    pop = product_offering_1.productOfferingPrice
    assert isinstance(product_offering_1, ProductOffering)
    assert isinstance(pop[0], ProductOfferingPriceRef)
    assert isinstance(pop[1], ProductOfferingPrice)
    assert isinstance(pop[1].lifecycleStatus, LifecycleStatus)
    assert isinstance(pop[2], ProductOfferingPrice)
    assert isinstance(pop[2].chargeType, ChargeType)
    assert isinstance(pop[2].price, Money)


def test_recurring_charge_throws_exception_when_charge_type_missing():
    product = {
        "isBundle": False,
        "name": "Pendrick Internet",
        "quantity": 1,
        "status": "active",
        "billingAccount": {
            "@type": "BillingAccountRef",
            "id": "89827405-1463-4a63-8804-38af97daaa87",
            "@baseType": "Entity",
        },
        "productPrice": [
            {
                "name": "Pendrick Internet Price",
                "priceType": "recurringCharge",
                "recurringChargePeriod": "monthly",
                "price": {
                    "dutyFreeAmount": {
                        "unit": "USD",
                        "value": 29.95,
                    },
                },
            }
        ],
        "productRelationship": [],
        "externalId": [],
    }
    with pytest.raises(ValueError) as e_info:
        product_pbj = Product.from_dict(product)


def test_recurring_charge_throws_exception_when_charge_period_missing():
    product = {
        "isBundle": False,
        "name": "Pendrick Internet",
        "quantity": 1,
        "status": "active",
        "billingAccount": {
            "@type": "BillingAccountRef",
            "id": "89827405-1463-4a63-8804-38af97daaa87",
            "@baseType": "Entity",
        },
        "productPrice": [
            {
                "chargeType": "inAdvance",
                "name": "Pendrick Internet Price",
                "priceType": "recurringCharge",
                "price": {
                    "dutyFreeAmount": {
                        "unit": "USD",
                        "value": 29.95,
                    },
                },
            }
        ],
        "productRelationship": [],
        "externalId": [],
    }
    with pytest.raises(ValueError) as e_info:
        product_pbj = Product.from_dict(product)


def test_product_throws_exception_when_name_missing():
    product = {
        "isBundle": False,
        "quantity": 1,
        "status": "active",
        "billingAccount": {
            "@type": "BillingAccountRef",
            "id": "89827405-1463-4a63-8804-38af97daaa87",
            "@baseType": "Entity",
        },
        "productPrice": [
            {
                "chargeType": "inAdvance",
                "name": "Pendrick Internet Price",
                "priceType": "recurringCharge",
                "recurringChargePeriod": "monthly",
                "price": {
                    "dutyFreeAmount": {
                        "unit": "USD",
                        "value": 29.95,
                    },
                },
            }
        ],
        "productRelationship": [],
        "externalId": [],
    }
    with pytest.raises(ValueError) as e_info:
        product_pbj = Product.from_dict(product)


# def test_product_throws_exception_when_quantity_missing():
#     product = {
#         "isBundle": False,
#         "name": "Pendrick Internet",
#         "status": "active",
#         "billingAccount": {
#             "@type": "BillingAccountRef",
#             "id": "89827405-1463-4a63-8804-38af97daaa87",
#             "@baseType": "Entity",
#         },
#         "productPrice": [
#             {
#                 "chargeType": "inAdvance",
#                 "name": "Pendrick Internet Price",
#                 "priceType": "recurringCharge",
#                 "recurringChargePeriod": "monthly",
#                 "price": {
#                     "dutyFreeAmount": {
#                         "unit": "USD",
#                         "value": 29.95,
#                     },
#                 },
#             }
#         ],
#         "productRelationship": [],
#         "externalId": [],
#     }
#     with pytest.raises(ValueError) as e_info:
#         product_pbj = Product.from_dict(product)


# def test_product_throws_exception_when_billing_account_missing():
#     product = {
#         "isBundle": False,
#         "name": "Pendrick Internet",
#         "quantity": 1,
#         "status": "active",
#         "productPrice": [
#             {
#                 "chargeType": "inAdvance",
#                 "name": "Pendrick Internet Price",
#                 "priceType": "recurringCharge",
#                 "recurringChargePeriod": "monthly",
#                 "price": {
#                     "dutyFreeAmount": {
#                         "unit": "USD",
#                         "value": 29.95,
#                     },
#                 },
#             }
#         ],
#         "productRelationship": [],
#         "externalId": [],
#     }
#     with pytest.raises(ValueError) as e_info:
#         product_pbj = Product.from_dict(product)


# def test_product_throws_exception_when_status_missing():
#     product = {
#         "isBundle": False,
#         "name": "Pendrick Internet",
#         "quantity": 1,
#         "productPrice": [
#             {
#                 "chargeType": "inAdvance",
#                 "name": "Pendrick Internet Price",
#                 "priceType": "recurringCharge",
#                 "recurringChargePeriod": "monthly",
#                 "price": {
#                     "dutyFreeAmount": {
#                         "unit": "USD",
#                         "value": 29.95,
#                     },
#                 },
#             }
#         ],
#         "productRelationship": [],
#         "externalId": [],
#     }
#     with pytest.raises(ValueError) as e_info:
#         product_pbj = Product.from_dict(product)


def test_product_ref_composition(product_1):
    product_ref = ProductRef.from_entity(product_1).to_dict()
    assert product_ref["@type"] == "ProductRef"
    assert product_ref["@referredType"] == "Product"
    assert product_ref["id"] == product_1.id


def test_cpc_instantiates_classes(pconf_1):
    cpci = pconf_1.checkProductConfigurationItem[0]
    prod_config = cpci.productConfiguration
    assert isinstance(pconf_1, CheckProductConfiguration)
    assert isinstance(cpci, CheckProductConfigurationItem)
    assert isinstance(cpci.state, CheckProductConfigurationItemState)
    assert isinstance(pconf_1.state, TaskStateType)
    assert isinstance(prod_config, ProductConfiguration)
    assert isinstance(prod_config.configurationAction[0], ConfigurationAction)
    assert isinstance(prod_config.productOffering, ProductOfferingRef)


def test_acbr_instantiates_classes(acbr_1):
    applied_tax = acbr_1.appliedTax[0]
    assert isinstance(acbr_1, AppliedCustomerBillingRate)
    assert isinstance(acbr_1.appliedBillingRateType, AppliedCustomerBillingRateType)
    assert isinstance(acbr_1.periodCoverage, TimePeriod)
    assert isinstance(acbr_1.taxExcludedAmount, Money)
    assert isinstance(acbr_1.billingAccount, BillingAccountRef)
    assert isinstance(acbr_1.product, ProductRef)
    assert isinstance(applied_tax, AppliedBillingTaxRate)
    assert isinstance(applied_tax.taxAmount, Money)
    assert isinstance(applied_tax.taxCategory, TaxCategory)


def test_billing_account_instantiates_classes(bill_acct_1):
    balance = bill_acct_1.accountBalance[0]
    contact_medium_1 = bill_acct_1.contact[0].contactMedium[0]
    contact_medium_2 = bill_acct_1.contact[0].contactMedium[1]
    struct = bill_acct_1.billStructure
    assert isinstance(bill_acct_1, BillingAccount)
    assert isinstance(balance, AccountBalance)
    assert isinstance(balance.balanceType, BalanceType)
    assert isinstance(contact_medium_1, GeographicAddressContactMedium)
    assert isinstance(contact_medium_2, EmailContactMedium)
    assert isinstance(struct, BillStructure)
    assert isinstance(struct.cycleSpecification, BillingCycleSpecification)
    assert isinstance(struct.presentationMedia[0], BillPresentationMedia)


@pytest.fixture
def order():
    return ProductOrder.from_dict(
        {
            "@type": "ProductOrder",
            "@baseType": "Entity",
            "createOn": "2024-12-31T14:47:08.055Z",
            "lastUpdate": "2024-12-31T14:47:22.179Z",
            "href": "/ProductOrder/ff47a779-1771-4e21-ba7f-481ab4b47f10",
            "id": "ff47a779-1771-4e21-ba7f-481ab4b47f10",
            "priority": "medium",
            "state": "inProgress",
            "billingAccount": {
                "@type": "BillingAccountRef",
                "@referredType": "BillingAccount",
                "id": "2372677a-9ecc-422a-888e-9db864015b01",
                "name": "PCONF Order Adapter Billing Account",
                "href": "/BillingAccount/2372677a-9ecc-422a-888e-9db864015b01",
            },
            "relatedParty": [
                {
                    "@type": "RelatedPartyRefOrPartyRoleRef",
                    "@baseType": "Entity",
                    "id": "ecad2d03-6cc9-4641-82c2-9bc7c3926b85",
                    "partyOrPartyRole": {
                        "@type": "Organization",
                        "@baseType": "Party",
                        "href": "/Organization/4d6111fa-ddf5-4234-ac7c-1a6a7ce7f39c",
                        "id": "4d6111fa-ddf5-4234-ac7c-1a6a7ce7f39c",
                        "contactMedium": [
                            {
                                "@type": "EmailContactMedium",
                                "@baseType": "ContactMedium",
                                "contactType": "other",
                                "id": "e1067b70-83e0-40fd-bec2-bbccfa47fe2f",
                                "preferred": True,
                                "emailAddress": "jane.doe@example.com",
                            }
                        ],
                        "relatedParty": [
                            {
                                "@type": "RelatedPartyRefOrPartyRoleRef",
                                "@baseType": "Entity",
                                "id": "7284a7c6-1a86-4f13-9cf1-0f80a657c6c4",
                                "partyOrPartyRole": {
                                    "@type": "IndividualRef",
                                    "@referredType": "Individual",
                                    "id": "cbbaa0f2-c9aa-472f-a7e9-4b447856b243",
                                    "name": "Elizabeth Bennet",
                                    "href": "/Individual/cbbaa0f2-c9aa-472f-a7e9-4b447856b243",
                                },
                                "role": "billingResponsible",
                            },
                            {
                                "@type": "RelatedPartyRefOrPartyRoleRef",
                                "@baseType": "Entity",
                                "id": "c61091a1-1540-4e96-8983-55c93b82ecbc",
                                "partyOrPartyRole": {
                                    "@type": "IndividualRef",
                                    "@referredType": "Individual",
                                    "id": "cbbaa0f2-c9aa-472f-a7e9-4b447856b243",
                                    "name": "Elizabeth Bennet",
                                    "href": "/Individual/cbbaa0f2-c9aa-472f-a7e9-4b447856b243",
                                },
                                "role": "paymentResponsible",
                            },
                            {
                                "@type": "RelatedPartyRefOrPartyRoleRef",
                                "@baseType": "Entity",
                                "id": "ac51a58c-e4b4-4e6f-91b9-68d2cf6b2383",
                                "partyOrPartyRole": {
                                    "@type": "PartyRole",
                                    "@baseType": "Entity",
                                    "name": "customer",
                                    "engagedParty": {
                                        "@type": "OrganizationRef",
                                        "@referredType": "Organization",
                                        "id": "4d6111fa-ddf5-4234-ac7c-1a6a7ce7f39c",
                                        "name": "PCONF Order Adapter",
                                        "href": "/Organization/4d6111fa-ddf5-4234-ac7c-1a6a7ce7f39c",
                                    },
                                },
                                "role": "customer",
                            },
                        ],
                        "partyCharacteristic": [
                            {
                                "@type": "StringCharacteristic",
                                "@baseType": "Characteristic",
                                "name": "customerId",
                                "value": "BC00000019",
                                "valueType": "string",
                                "id": "1a55bc9d-7eb7-4601-b0df-4b4c4a8e84e8",
                            }
                        ],
                        "isHeadOffice": True,
                        "isLegalEntity": True,
                        "name": "PCONF Order Adapter",
                        "organizationType": "company",
                        "status": "validated",
                        "place": [
                            {
                                "@type": "PlaceRef",
                                "@referredType": "Place",
                                "id": "ca4630f4-ece6-4166-a220-3966443150fb",
                                "name": "United States",
                            }
                        ],
                        "marketSegment": [
                            {
                                "@type": "MarketSegmentRef",
                                "@referredType": "MarketSegment",
                                "id": "a30e21bd-bcd9-477e-ad2b-6b50b8b57697",
                                "name": "Small and Medium Companies",
                            }
                        ],
                    },
                    "role": "customer",
                }
            ],
            "productOrderItem": [
                {
                    "@type": "ProductOrderItem",
                    "@baseType": "Entity",
                    "action": "delete",
                    "id": "72dfbc24-fd78-4de7-8f83-85d789de65dd",
                    "quantity": 1,
                    "state": "draft",
                    "productOffering": {
                        "@type": "ProductOfferingRef",
                        "@referredType": "ProductOffering",
                        "id": "4005333b-dbf7-4504-a888-436a4897d252",
                    },
                    "product": {
                        "@type": "Product",
                        "@baseType": "Entity",
                        "name": "Product 1 - PCONF Order Adapter",
                        "status": "terminated",
                        "isBundle": False,
                        "productPrice": [
                            {
                                "@type": "ProductPrice",
                                "@baseType": "Entity",
                                "price": {
                                    "@type": "Price",
                                    "@baseType": "Entity",
                                    "dutyFreeAmount": {
                                        "@type": "Money",
                                        "@baseType": "Entity",
                                        "unit": "PHP",
                                        "value": 100,
                                    },
                                },
                                "name": "Product 1 Price",
                                "description": "Product 1 Price - PCONF Order Adapter",
                                "priceAlteration": [
                                    {
                                        "@type": "PriceAlteration",
                                        "@baseType": "Entity",
                                        "price": {
                                            "@type": "Price",
                                            "@baseType": "Entity",
                                            "percentage": 10,
                                        },
                                        "applicationDuration": 1,
                                        "description": "10 percent discount",
                                        "name": "Promo percentage discount",
                                        "priceType": "discount",
                                        "priority": 1,
                                        "recurringChargePeriod": "monthly",
                                        "isPercentage": True,
                                    },
                                    {
                                        "@type": "PriceAlteration",
                                        "@baseType": "Entity",
                                        "price": {
                                            "@type": "Price",
                                            "@baseType": "Entity",
                                            "dutyFreeAmount": {
                                                "@type": "Money",
                                                "@baseType": "Entity",
                                                "unit": "PHP",
                                                "value": 10,
                                            },
                                        },
                                        "description": "10 PHP discount",
                                        "name": "Promo fixed discount",
                                        "priceType": "discount",
                                        "priority": 1,
                                        "isPercentage": False,
                                    },
                                ],
                                "recurringChargePeriod": "monthly",
                                "unitOfMeasure": "100 Mb",
                                "priceType": "recurringCharge",
                                "chargeType": "inAdvance",
                                "productOfferingPrice": {
                                    "@type": "ProductOfferingPriceRef",
                                    "@referredType": "ProductOfferingPrice",
                                    "id": "4b2585aa-3a7c-49bc-87fe-c80f54693587",
                                },
                            }
                        ],
                        "id": "a9dbdf49-7805-4978-a4ab-8a05c63bc1d0",
                        "description": "Demo Product 1",
                        "terminationDate": "2025-12-31T14:47:02.681Z",
                    },
                },
                {
                    "@type": "ProductOrderItem",
                    "@baseType": "Entity",
                    "action": "noChange",
                    "id": "2c2482a4-f8bc-4682-98af-63e03f8ad0d8",
                    "quantity": 1,
                    "state": "draft",
                    "productOffering": {
                        "@type": "ProductOfferingRef",
                        "@referredType": "ProductOffering",
                        "id": "4005333b-dbf7-4504-a888-436a4897d252",
                    },
                    "product": {
                        "@type": "Product",
                        "@baseType": "Entity",
                        "name": "Product 2 - PCONF Order Adapter",
                        "status": "active",
                        "isBundle": False,
                        "productPrice": [
                            {
                                "@type": "ProductPrice",
                                "@baseType": "Entity",
                                "price": {
                                    "@type": "Price",
                                    "@baseType": "Entity",
                                    "dutyFreeAmount": {
                                        "@type": "Money",
                                        "@baseType": "Entity",
                                        "unit": "PHP",
                                        "value": 100,
                                    },
                                },
                                "name": "Product Price 2",
                                "description": "Price for Product 2 - PCONF Order Adapter",
                                "recurringChargePeriod": "monthly",
                                "unitOfMeasure": "day",
                                "priceType": "recurringCharge",
                                "chargeType": "inArrear",
                                "productOfferingPrice": {
                                    "@type": "ProductOfferingPriceRef",
                                    "@referredType": "ProductOfferingPrice",
                                    "id": "4b2585aa-3a7c-49bc-87fe-c80f54693587",
                                },
                            }
                        ],
                        "id": "c26b4348-8f36-46e1-8271-162076614497",
                        "description": "Demo Product 2",
                        "terminationDate": "2025-12-31T14:47:03.695Z",
                    },
                },
            ],
        }
    )


@pytest.fixture
def cpc_order():
    return ProductOrder(
        id="order-id",
        channel=[
            RelatedChannel(
                role="someChannel",
                channel=ChannelRef(id="some-channel-id"),
            )
        ],
        relatedParty=[
            RelatedPartyRefOrPartyRoleRef(
                role="customer",
                partyOrPartyRole=Organization(
                    id="org-id",
                    relatedParty=[
                        RelatedPartyRefOrPartyRoleRef(
                            partyOrPartyRole=IndividualRef(
                                id="individual-id",
                                name="Elizabeth Bennet",
                            ),
                            role=RoleEnum.BILLING_RESPONSIBLE,
                        ),
                        RelatedPartyRefOrPartyRoleRef(
                            partyOrPartyRole=IndividualRef(
                                id="individual-id-2",
                                name="Jane Bennet",
                            ),
                            role=RoleEnum.OWNER,
                        ),
                    ],
                ),
            )
        ],
        productOrderItem=[
            ProductOrderItem(
                action=ItemActionType.ADD,
                id="1",
                orderTerm=[
                    OrderTerm(
                        description="term-description",
                        duration=Duration(
                            units="year",
                            amount=1,
                        ),
                    )
                ],
                itemPrice=[
                    OrderPrice(
                        priceType=PriceType.RECURRING_CHARGE,
                        recurringChargePeriod=RecurringChargePeriod.MONTHLY,
                    )
                ],
            ),
            ProductOrderItem(
                action=ItemActionType.ADD,
                id="2",
                productOrderItemRelationship=[
                    OrderItemRelationship(
                        id="1",
                        relationshipType=ProductOrderItemRelationshipType.REQUIRES,
                    )
                ],
            ),
        ],
    )


def test_cpc_from_order(order):
    cpc = CheckProductConfiguration.from_order(product_order=order)
    assert isinstance(
        cpc.contextEntity,
        ProductOrderRef,
    )
    assert isinstance(
        cpc.checkProductConfigurationItem[0].contextItem,
        ProductOrderItemRef,
    )
    assert isinstance(
        cpc.checkProductConfigurationItem[0]
        .productConfiguration.configurationAction[0]
        .action,
        ProductActionType,
    )
    assert cpc.checkProductConfigurationItem[0].productConfiguration.quantity == 1
    assert isinstance(
        cpc.checkProductConfigurationItem[
            0
        ].productConfiguration.product.billingAccount,
        BillingAccountRef,
    )


def test_cpc_from_order_channel(cpc_order):
    cpc = CheckProductConfiguration.from_order(product_order=cpc_order)
    assert isinstance(cpc.channel, ChannelRef)
    assert isinstance(
        cpc.relatedParty[0].partyOrPartyRole.relatedParty[1].partyOrPartyRole,
        IndividualRef,
    )
    assert isinstance(
        cpc.checkProductConfigurationItem[1]
        .productConfigurationItemRelationship[0]
        .relationshipType,
        ProductRelationshipType,
    )
    assert isinstance(
        cpc.checkProductConfigurationItem[0].productConfiguration.configurationTerm[0],
        ConfigurationTerm,
    )


def test_cpc_from_order_no_channel():
    order = ProductOrder(id="some-id")
    cpc = CheckProductConfiguration.from_order(product_order=order)
    assert cpc.channel is None


@pytest.fixture
def ps_rel():
    return {
        "id": "23",
        "@referredType": "ProductSpecification",
        "@type": "ProductSpecificationRelationship",
        "href": "https://mycsp.com:8080/tmf-api/productCatalogManagement/v5/productSpecification/23",
        "name": "DataPlan",
        "relationshipType": "substitutedBy",
        "validFor": {"startDateTime": "2020-09-23T16:42:23.000Z"},
        "characteristic": [],
    }


def test_ps_relationship_from_dict(ps_rel):
    psr = ProductSpecificationRelationship.from_dict(ps_rel)
    assert psr._referred_type == "ProductSpecification"
    assert psr.to_dict()["@referredType"] == "ProductSpecification"


@pytest.fixture
def ps_dict():
    return {
        "id": "d16f75b5-df9a-45f5-90e9-504994e61d1b",
        "@type": "ProductSpecification",
        "attachment": [
            {
                "id": "22",
                "url": "https://mycsp.com:7070/docloader?docnum=774451234",
                "href": "https://mycsp.com:8080/tmf-api/documentManagement/v5/attachment/22",
                "name": "Product Picture",
                "@type": "AttachmentRef",
                "@referredType": "Attachment",
            },
            {
                "id": "33",
                "url": "https://mycsp.com:7070/docloader?docnum=774454321",
                "href": "https://mycsp.com:8080/tmf-api/documentManagement/v5/attachment/22",
                "name": "Product Manual",
                "@type": "AttachmentRef",
                "@referredType": "Attachment",
            },
        ],
        "brand": "Cisco",
        "description": "Powerful product that integrates with a firewall, including intrusion prevention, advanced malware protection, cloud-based sandboxing, URL filtering, endpoint protection, web gateway, email security, network traffic analysis, network access control and CASB.",
        "fulfilmentData": [],
        "isBundle": True,
        "lifecycleStatus": "inDraft",
        "name": "Cisco Firepower NGFW",
        "productNumber": "CSC-340-NGFW",
        "validFor": {
            "startDateTime": "2020-09-23T00:00:00.000Z",
            "endDateTime": "2022-11-24T16:42:23.000Z",
        },
        "version": "1.0",
        "createOn": "2024-08-22T16:41:38.462Z",
        "lastUpdate": "2020-09-23T16:42:23.000Z",
        "category": [],
        "policy": [],
        "serviceSpecification": [
            {
                "id": "22",
                "@referredType": "ServiceSpecification",
                "@type": "ServiceSpecificationRef",
                "href": "https://mycsp.com:8080/tmf-api/serviceCatalogManagement/v5/serviceSpecification/22",
                "name": "Firewall",
                "version": "1.0",
            }
        ],
        "productSpecificationRelationship": [
            {
                "id": "23",
                "@referredType": "ProductSpecification",
                "@type": "ProductSpecificationRelationship",
                "href": "https://mycsp.com:8080/tmf-api/productCatalogManagement/v5/productSpecification/23",
                "name": "DataPlan",
                "relationshipType": "substitutedBy",
                "validFor": {"startDateTime": "2020-09-23T16:42:23.000Z"},
                "characteristic": [],
            }
        ],
        "targetProductSchema": {
            "id": "b7a04996-0b70-45f8-b342-28dd1bb9ba71",
            "@schemaLocation": "https://mycsp.com:8080/tmf-api/schema/Product/Firewall.schema.json",
            "@type": "Firewall",
        },
        "bundledProductSpecification": [
            {
                "id": "64",
                "@type": "BundledProductSpecification",
                "href": "https://mycsp.com:8080/tmf-api/productCatalogManagement/v5/productSpecification/64",
                "lifecycleStatus": "active",
                "name": "Malware Protector",
            },
            {
                "id": "15",
                "@type": "BundledProductSpecification",
                "href": "https://mycsp.com:8080/tmf-api/productCatalogManagement/v5/productSpecification/15",
                "lifecycleStatus": "active",
                "name": "URL Filter",
            },
        ],
        "relatedParty": [
            {
                "id": "ef1d9e72-47b4-425e-bcf6-47152b5a22d4",
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "partyOrPartyRole": {
                    "id": "1234",
                    "href": "https://mycsp.com:8080/tmf-api/partyManagement/v5/partyRole/1234",
                    "name": "Gustave Flaubert",
                    "@type": "PartyRef",
                    "@referredType": "Individual",
                },
                "role": "Owner",
            }
        ],
        "resourceSpecification": [
            {
                "id": "63",
                "@referredType": "PhysicalResourceSpecification",
                "@type": "ResourceSpecificationRef",
                "href": "https://mycsp.com:8080/tmf-api/resourceCatalogManagement/v5/resourceSpecification/63",
                "name": "Firewall Port",
                "version": "1.0",
            }
        ],
        "productSpecCharacteristic": [
            {
                "id": "097e34e4-f0fe-42c0-acee-5d72468cadce",
                "@type": "CharacteristicSpecification",
                "configurable": True,
                "description": "Color of the Firewall housing",
                "extensible": True,
                "isUnique": True,
                "maxCardinality": 1,
                "minCardinality": 1,
                "name": "Color",
                "validFor": {"startDateTime": "2020-09-23T16:42:23.000Z"},
                "valueType": "string",
                "createOn": "2024-08-22T16:41:38.462Z",
                "lastUpdate": "2024-08-22T16:41:38.462Z",
                "charSpecRelationship": [],
                "characteristicValueSpecification": [
                    {
                        "id": "2e23132f-1fb0-4ca0-968f-1978ca339efc",
                        "@type": "StringCharacteristicValueSpecification",
                        "isDefault": False,
                        "valueType": "string",
                        "value": "White",
                    },
                    {
                        "id": "b83654be-4eca-41be-99b8-0d87019f8dbc",
                        "@type": "StringCharacteristicValueSpecification",
                        "isDefault": True,
                        "valueType": "string",
                        "value": "Black",
                    },
                ],
            },
            {
                "id": "99753619-c8f7-4088-9570-cad7538f0569",
                "@type": "CharacteristicSpecification",
                "configurable": True,
                "description": "The total Number of Ports for this product",
                "isUnique": True,
                "maxCardinality": 1,
                "minCardinality": 1,
                "name": "Number of Ports",
                "validFor": {"startDateTime": "2020-09-23T16:42:23.000Z"},
                "valueType": "number",
                "createOn": "2024-08-22T16:41:38.462Z",
                "lastUpdate": "2024-08-22T16:41:38.462Z",
                "charSpecRelationship": [
                    {
                        "id": "58beb9df-36bb-481e-b616-2cdcbbfffa23",
                        "@type": "CharacteristicSpecificationRelationship",
                        "characteristicSpecificationId": "2",
                        "name": "Bandwidth",
                        "parentSpecificationHref": "https://mycsp.com:8080/tmf-api/productCatalogManagement/v5/productSpecification/43",
                        "parentSpecificationId": "43",
                        "relationshipType": "substitutedBy",
                        "validFor": {"startDateTime": "2020-09-23T20:42:23.000Z"},
                    }
                ],
                "characteristicValueSpecification": [
                    {
                        "id": "2d7490e7-4ad9-44cb-9783-c12b175b4005",
                        "@type": "NumberCharacteristicValueSpecification",
                        "isDefault": False,
                        "validFor": {
                            "startDateTime": "2020-09-23T00:00:00.000Z",
                            "endDateTime": "2022-11-24T00:00:00.000Z",
                        },
                        "valueType": "number",
                        "value": "24",
                    },
                    {
                        "id": "305214ee-18d2-4f3b-a869-e47de8454187",
                        "@type": "NumberCharacteristicValueSpecification",
                        "isDefault": False,
                        "validFor": {
                            "startDateTime": "2020-09-23T00:00:00.000Z",
                            "endDateTime": "2022-11-24T00:00:00.000Z",
                        },
                        "valueType": "number",
                        "value": "16",
                    },
                    {
                        "id": "2bf61455-9f45-4de3-8776-470e93d1bcad",
                        "@type": "NumberCharacteristicValueSpecification",
                        "isDefault": True,
                        "validFor": {
                            "startDateTime": "2020-09-23T00:00:00.000Z",
                            "endDateTime": "2022-11-24T00:00:00.000Z",
                        },
                        "valueType": "number",
                        "value": "8",
                    },
                ],
            },
        ],
        "externalIdentifier": [],
        "href": "/ProductSpecification/d16f75b5-df9a-45f5-90e9-504994e61d1b",
    }


def test_ps_from_dict(ps_dict):
    ps = ProductSpecification.from_dict(ps_dict)
    assert isinstance(ps.bundledProductSpecification[0], BundledProductSpecification)
    assert ps.resourceSpecification[0]._referred_type == "PhysicalResourceSpecification"


@pytest.fixture
def category_1():
    return Category.from_dict(
        {
            "@type": "Category",
            "categoryType": "Commercial",
            "href": "/Category/e611ed76-a0d6-423b-88bb-ad7a43e919d1",
            "id": "e611ed76-a0d6-423b-88bb-ad7a43e919d1",
            "name": "Devices",
            "isRoot": False,
            "lastUpdate": "2024-11-20T18:11:22.007Z",
            "externalIdentifier": [
                {
                    "@type": "ExternalIdentifier",
                    "externalIdentifierType": "External Account ID",
                    "id": "baff288e-ce07-4a02-be7b-cb7aa9d75093",
                }
            ],
            "lifecycleStatus": "active",
            "parent": {
                "@type": "CategoryRef",
                "id": "52ef2102-b3ca-4ab5-bcbe-6de224358399",
                "@referredType": "Category",
            },
            "productOffering": [
                {
                    "@type": "ProductOfferingRef",
                    "id": "83d36da9-81a4-44c1-ad90-f993798b5894",
                    "name": "iPhone 17 Pro - PI Demo",
                    "@referredType": "ProductOffering",
                },
                {
                    "@type": "BundledProductOffering",
                    "@baseType": "ProductOfferingRef",
                    "id": "some_id",
                    "name": "some-name",
                    "@referredType": "ProductOffering",
                    "bundledProductOfferingOption": {
                        "@type": "BundledProductOfferingOption",
                        "numberRelOfferDefault": 1,
                        "numberRelOfferLowerLimit": 1,
                        "numberRelOfferUpperLimit": 5,
                    },
                },
            ],
        }
    )


def test_category_class_init(category_1):
    p_off = category_1.productOffering
    assert isinstance(p_off[0], ProductOfferingRef)
    assert isinstance(p_off[1], BundledProductOffering)
    assert isinstance(
        p_off[1].bundledProductOfferingOption,
        BundledProductOfferingOption,
    )


def test_rate_plan_product(rate_plan_product):
    product_instance = Product.from_dict(rate_plan_product)

    assert isinstance(product_instance, RatePlanProduct)
    assert product_instance.__class__.__name__ == "RatePlanProduct"

    product_dict = product_instance.to_dict()
    assert product_dict["@type"] == "RatePlanProduct"
    assert product_dict["@baseType"] == "Product"

def test_party_ref_has_no_version():
    party = Individual(id="123", familyName="Doe", version="1.0")
    party_ref = PartyRef.from_entity(party)
    assert not hasattr(party_ref, "version")