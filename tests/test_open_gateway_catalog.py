import pytest
from tmforum import (
    ApiGrantInformation,
    ApiProductSpecification,
    ApiStandardNameType,
    ApiStatusType,
    ApiVersionInformation,
    BundledProductOffering,
    BundledProductOfferingOption,
    Context,
    DpvLegalBasisType,
    DpvPurposeType,
    OpenGatewayAllowedProductAction,
    OpenGatewayAllowedProductActionType,
    OpenGatewayAttachmentType,
    OpenGatewayFileAttachment,
    OpenGatewayProductOffering,
    OpenGatewayProductOfferingLifecycleStatusType,
    OpenGatewayProductOfferingPrice,
    OpenGatewayProductOfferingPriceLifecycleStatus,
    OpenGatewayProductOfferingPriceType,
    OpenGatewayProductOfferingTermOrConditionSpecification,
    OpenGatewayProductSpecification,
    OpenGatewayProductSpecificationLifecycleStatus,
    OpenGatewayProductSpecificationRef,
    OpenGatewayProductSpecificationRelationship,
    OpenGatewayProductSpecificationRelationshipType,
    OpenGatewayURLAttachment,
    TargetProductSchema,
    UsageVolumeProductSpecification,
)


@pytest.fixture
def open_gateway_product_offering_dict():
    return {
        "@type": "OpenGatewayProductOffering",
        "@baseType": "DcsProductOffering",
        "id": "2d4ef4d3-08ce-441d-ac76-133b6dad0ccb",
        "href": (
            "https://mycsp.com/tmf-api/openGatewayOperateAPIProductCatalog/v5"
            "/productOffering/2d4ef4d3-08ce-441d-ac76-133b6dad0ccb"
        ),
        "name": "Location Verification Antifraud CAMARA API Standalone",
        "description": (
            "Location Verification product offering standalone, for antifraud "
            "purpose, accessible with CAMARA API."
        ),
        "version": "1.0.0",
        "lifecycleStatus": "launched",
        "lastUpdate": "2023-07-01T00:00:00Z",
        "allowedAction": [
            {
                "@type": "OpenGatewayAllowedProductAction",
                "id": "1",
                "action": "add",
            },
            {
                "@type": "OpenGatewayAllowedProductAction",
                "id": "2",
                "action": "delete",
            },
        ],
        "productSpecification": {
            "@type": "OpenGatewayProductSpecificationRef",
            "id": "4b6591ef-5ede-4885-9543-0c5e9070ade9",
            "href": (
                "https://mycsp.com/tmf-api/openGatewayOperateAPIProductCatalog/v5"
                "/productSpecification/4b6591ef-5ede-4885-9543-0c5e9070ade9"
            ),
            "name": "Location Verification Antifraud CAMARA API",
            "version": "1.0.0",
            "@referredType": "ApiProductSpecification",
        },
        "productOfferingTermOrConditionSpecification": [
            {
                "@type": "OpenGatewayProductOfferingTermOrConditionSpecification",
                "id": "2d4ef4d3-08ce-441d-ac76-133b6dad0ccb_terms_1",
                "name": "Product Offering Terms and Conditions for ApplicationOwner",
                "description": (
                    "Terms and conditions to be approved by ApplicationOwner at the order."
                ),
                "attachment": {
                    "@type": "OpenGatewayFileAttachment",
                    "content": "JVBERi0xL...DQolJUVPRg==",
                    "mimeType": "application/pdf",
                    "attachmentType": "termsAndConditions",
                },
            }
        ],
        "productOfferingPrice": [
            {
                "@type": "OpenGatewayProductOfferingPrice",
                "id": "1",
                "name": "Location Verification Antifraud CAMARA API Standalone Usage Price",
                "description": "8 EUR per API call for FR, ES and GB.",
                "lifecycleStatus": "active",
                "lastUpdate": "2023-09-01T00:00:00Z",
                "priceType": "composite",
            }
        ],
        "bundledProductOffering": [
            {
                "@type": "BundledProductOffering",
                "id": "ab7792f8-6628-4c4b-a557-699adc26d4ce",
                "href": (
                    "https://mycsp.com/tmf-api/openGatewayOperateAPIProductCatalog/v5"
                    "/productOffering/ab7792f8-6628-4c4b-a557-699adc26d4ce"
                ),
                "version": "1.0.0",
                "@referredType": "OpenGatewayProductOffering",
                "bundledProductOfferingOption": {
                    "@type": "BundledProductOfferingOption",
                    "numberRelOfferDefault": 1,
                    "numberRelOfferLowerLimit": 1,
                    "numberRelOfferUpperLimit": 1,
                },
            }
        ],
    }


@pytest.fixture
def api_product_specification_dict():
    return {
        "@type": "ApiProductSpecification",
        "@baseType": "OpenGatewayProductSpecification",
        "id": "4b6591ef-5ede-4885-9543-0c5e9070ade9",
        "href": (
            "https://mycsp.com/tmf-api/openGatewayOperateAPIProductCatalog/v5"
            "/productSpecification/4b6591ef-5ede-4885-9543-0c5e9070ade9"
        ),
        "name": "Location Verification Antifraud CAMARA API",
        "version": "1.0.0",
        "lifecycleStatus": "active",
        "description": (
            "Location Verification product specification, for antifraud purpose, "
            "accessible with CAMARA API."
        ),
        "lastUpdate": "2023-09-23T16:42:23Z",
        "targetProductSchema": {
            "@type": "ApiProductLocationVerificationAntifraud",
            "@schemaLocation": (
                "https://mycsp.com/tmf-api/schemas/Tmf/Product/DCS/GSMAOperateAPI"
                "/LocationVerificationAntifraud.schema.json"
            ),
        },
        "apiStandardName": "CAMARA",
        "apiVersionInformation": [
            {
                "@type": "ApiVersionInformation",
                "apiName": "location-verification",
                "apiVersion": "1.0.0",
                "apiBasePath": "/location-verification/v1",
                "apiStatus": "active",
                "apiGrantInformation": [
                    {
                        "@type": "ApiGrantInformation",
                        "purpose": "dpv:FraudPreventionAndDetection",
                        "legalBasis": "dpv:Consent",
                        "scope": ["location-verification:verify"],
                        "grantType": [
                            "authorization_code",
                            "urn:openid:params:grant-type:ciba",
                        ],
                    }
                ],
            }
        ],
        "productSpecificationRelationship": [
            {
                "@type": "OpenGatewayProductSpecificationRelationship",
                "id": "0a2782b7-81a7-4af9-9e4f-d51bc690ec2d",
                "name": "Usage Volume for Location Verification",
                "relationshipType": "appliesOn",
            }
        ],
        "attachment": [
            {
                "@type": "OpenGatewayURLAttachment",
                "url": (
                    "https://mycsp.com/OpenGateway/documentation"
                    "/LocationVerificationDeveloperGuide.html"
                ),
                "attachmentType": "developerDocumentation",
                "mimeType": "text/html",
            }
        ],
    }


@pytest.fixture
def product_offering_1(open_gateway_product_offering_dict):
    return OpenGatewayProductOffering.from_dict(open_gateway_product_offering_dict)


@pytest.fixture
def product_specification_1(api_product_specification_dict):
    return OpenGatewayProductSpecification.from_dict(api_product_specification_dict)


def test_product_offering_instantiates_with_id(product_offering_1):
    assert product_offering_1.id == "2d4ef4d3-08ce-441d-ac76-133b6dad0ccb"
    assert product_offering_1.version == "1.0.0"
    assert product_offering_1.productOfferingPrice[0].description == (
        "8 EUR per API call for FR, ES and GB."
    )


def test_product_offering_instantiates_classes(product_offering_1):
    assert isinstance(
        product_offering_1.lifecycleStatus,
        OpenGatewayProductOfferingLifecycleStatusType,
    )
    assert isinstance(
        product_offering_1.productSpecification, OpenGatewayProductSpecificationRef
    )
    assert product_offering_1.productSpecification._referred_type == (
        "ApiProductSpecification"
    )

    action = product_offering_1.allowedAction[0]
    assert isinstance(action, OpenGatewayAllowedProductAction)
    assert action.action is OpenGatewayAllowedProductActionType.ADD
    assert (
        product_offering_1.allowedAction[1].action
        is OpenGatewayAllowedProductActionType.DELETE
    )

    terms = product_offering_1.productOfferingTermOrConditionSpecification[0]
    assert isinstance(terms, OpenGatewayProductOfferingTermOrConditionSpecification)
    assert isinstance(terms.attachment, OpenGatewayFileAttachment)
    assert terms.attachment.attachmentType is (
        OpenGatewayAttachmentType.TERMS_AND_CONDITIONS
    )
    assert terms.attachment.content == "JVBERi0xL...DQolJUVPRg=="

    price = product_offering_1.productOfferingPrice[0]
    assert isinstance(price, OpenGatewayProductOfferingPrice)
    assert (
        price.lifecycleStatus is OpenGatewayProductOfferingPriceLifecycleStatus.ACTIVE
    )
    assert price.priceType is OpenGatewayProductOfferingPriceType.COMPOSITE

    bundled = product_offering_1.bundledProductOffering[0]
    assert isinstance(bundled, BundledProductOffering)
    assert isinstance(
        bundled.bundledProductOfferingOption, BundledProductOfferingOption
    )
    assert bundled.bundledProductOfferingOption.numberRelOfferUpperLimit == 1


def test_product_specification_resolves_api_subtype(product_specification_1):
    assert isinstance(product_specification_1, ApiProductSpecification)
    assert product_specification_1.__class__.__name__ == "ApiProductSpecification"
    assert product_specification_1.apiStandardName is ApiStandardNameType.CAMARA


def test_product_specification_instantiates_classes(product_specification_1):
    assert isinstance(
        product_specification_1.lifecycleStatus,
        OpenGatewayProductSpecificationLifecycleStatus,
    )
    # targetProductSchema carries the product schema's own name in "@type"
    # (not a TM Forum class), so from_dict leaves it as a raw dict.
    assert product_specification_1.targetProductSchema["@type"] == (
        "ApiProductLocationVerificationAntifraud"
    )
    assert isinstance(
        TargetProductSchema.from_dict(
            {"@schemaLocation": "https://mycsp.com/tmf-api/schemas/target.json"}
        ),
        TargetProductSchema,
    )

    version_info = product_specification_1.apiVersionInformation[0]
    assert isinstance(version_info, ApiVersionInformation)
    assert version_info.apiBasePath == "/location-verification/v1"
    assert version_info.apiStatus is ApiStatusType.ACTIVE

    grant = version_info.apiGrantInformation[0]
    assert isinstance(grant, ApiGrantInformation)
    assert grant.purpose is DpvPurposeType.FRAUD_PREVENTION_AND_DETECTION
    assert grant.legalBasis is DpvLegalBasisType.CONSENT
    assert grant.scope == ["location-verification:verify"]
    assert "urn:openid:params:grant-type:ciba" in grant.grantType

    relationship = product_specification_1.productSpecificationRelationship[0]
    assert isinstance(relationship, OpenGatewayProductSpecificationRelationship)
    assert relationship.relationshipType is (
        OpenGatewayProductSpecificationRelationshipType.APPLIES_ON
    )

    attachment = product_specification_1.attachment[0]
    assert isinstance(attachment, OpenGatewayURLAttachment)
    assert attachment.attachmentType is (
        OpenGatewayAttachmentType.DEVELOPER_DOCUMENTATION
    )


def test_usage_volume_product_specification_resolves(api_product_specification_dict):
    payload = dict(api_product_specification_dict)
    payload["@type"] = "UsageVolumeProductSpecification"
    payload.pop("apiStandardName")
    payload.pop("apiVersionInformation")

    spec = OpenGatewayProductSpecification.from_dict(payload)
    assert isinstance(spec, UsageVolumeProductSpecification)
    assert isinstance(spec, OpenGatewayProductSpecification)


def test_product_offering_round_trip(product_offering_1):
    offering_dict = product_offering_1.to_dict()

    assert offering_dict["@type"] == "OpenGatewayProductOffering"
    assert offering_dict["@baseType"] == "ProductOffering"
    assert offering_dict["lifecycleStatus"] == "launched"
    assert offering_dict["productOfferingPrice"][0]["priceType"] == "composite"
    assert offering_dict["allowedAction"][0]["action"] == "add"
    assert (
        offering_dict["productOfferingTermOrConditionSpecification"][0]["attachment"][
            "@type"
        ]
        == "OpenGatewayFileAttachment"
    )
    assert offering_dict["productSpecification"]["@referredType"] == (
        "ApiProductSpecification"
    )


def test_product_specification_round_trip(product_specification_1):
    spec_dict = product_specification_1.to_dict()

    assert spec_dict["@type"] == "ApiProductSpecification"
    assert spec_dict["@baseType"] == "OpenGatewayProductSpecification"
    assert spec_dict["apiStandardName"] == "CAMARA"
    assert spec_dict["apiVersionInformation"][0]["apiGrantInformation"][0][
        "purpose"
    ] == ("dpv:FraudPreventionAndDetection")
    assert spec_dict["attachment"][0]["@type"] == "OpenGatewayURLAttachment"
    assert spec_dict["attachment"][0]["@baseType"] == "OpenGatewayAttachment"


def test_product_offering_rejects_non_list_for_list_field():
    with pytest.raises(ValueError):
        OpenGatewayProductOffering(
            id="1",
            productOfferingPrice=OpenGatewayProductOfferingPrice(id="1"),
        )


def test_open_gateway_resource_paths():
    context = Context(api_base_url="https://mycsp.com/tmf-api")

    assert OpenGatewayProductOffering.get_resource_path(context) == (
        "https://mycsp.com/tmf-api/openGatewayOperateAPIProductCatalog/v5"
        "/productOffering"
    )
    assert OpenGatewayProductSpecification.get_resource_path(context) == (
        "https://mycsp.com/tmf-api/openGatewayOperateAPIProductCatalog/v5"
        "/productSpecification"
    )
    assert ApiProductSpecification.get_resource_path(context) == (
        "https://mycsp.com/tmf-api/openGatewayOperateAPIProductCatalog/v5"
        "/productSpecification"
    )
