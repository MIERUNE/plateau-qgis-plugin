from ..base import (
    Attribute,
    AttributeGroup,
)

# Attributes inherited from urf:Zone
ZONE_ATTRIBUTES = [
    AttributeGroup(
        base_element=None,
        attributes=[
            Attribute(
                name="areaClassificationType",
                path="./urf:areaClassificationType",
                datatype="string",
                predefined_codelist="Common_areaClassificationType",
            ),
            Attribute(
                name="city",
                path="./urf:city",
                datatype="string",
                predefined_codelist="Common_localPublicAuthorities",
            ),
            Attribute(
                name="custodian",
                path="./urf:custodian",
                datatype="string",
            ),
            Attribute(
                name="enactmentFiscalYear",
                path="./urf:enactmentFiscalYear",
                datatype="integer",
            ),
            Attribute(
                name="expirationFiscalYear",
                path="./urf:expirationFiscalYear",
                datatype="integer",
            ),
            Attribute(
                name="urf:finalNotificationDate",
                path="./urf:finalNotificationDate",
                datatype="date",
            ),
            Attribute(
                name="urf:finalNotificationNumber",
                path="./urf:finalNotificationNumber",
                datatype="string",
            ),
            Attribute(
                name="legalGrounds",
                path="./urf:legalGrounds",
                datatype="string",
            ),
            Attribute(
                name="location",
                path="./urf:location",
                datatype="string",
            ),
            Attribute(
                name="nominalArea",
                path="./urf:nominalArea",
                datatype="double",
            ),
            Attribute(
                name="note",
                path="./urf:note",
                datatype="string",
            ),
            Attribute(
                name="notificationNumber",
                path="./urf:notificationNumber",
                datatype="string",
            ),
            Attribute(
                name="prefecture",
                path="./urf:prefecture",
                datatype="string",
                predefined_codelist="Common_localPublicAuthorities",
            ),
            Attribute(
                name="reason",
                path="./urf:reason",
                datatype="string",
            ),
            Attribute(
                name="reference",
                path="./urf:reference",
                datatype="string",
            ),
            Attribute(
                name="urf:surveyYear",
                path="./urf:surveyYear",
                datatype="integer",
            ),
            Attribute(
                name="urbanPlanType",
                path="./urf:urbanPlanType",
                datatype="string",
                predefined_codelist="Common_urbanPlanType",
            ),
            Attribute(
                name="validFrom",
                path="./urf:validFrom",
                datatype="date",
            ),
            Attribute(
                name="validFromType",
                path="./urf:validFromType",
                datatype="string",
                predefined_codelist="Common_validType",
            ),
            Attribute(
                name="validTo",
                path="./urf:validTo",
                datatype="date",
            ),
            Attribute(
                name="validToType",
                path="./urf:validToType",
                datatype="string",
                predefined_codelist="Common_validType",
            ),
        ],
    ),
]
