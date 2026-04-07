"""
GreenShield+ Coverage Mapping
Source: University of Ottawa Graduate Students' Association Benefit Plan Booklet
Billing Divisions: 23785 and 32012 | Revised Effective Date: September 1, 2025
Benefit Year: September 1 – August 31

All values quoted directly from booklet unless marked [NOT IN BOOKLET — FLAG].
"""

import json

coverage_by_group = {

    # ─────────────────────────────────────────────────────────────────
    # SPECIAL ENTRY: Overall plan maximums
    # ─────────────────────────────────────────────────────────────────
    "_overall": {
        "booklet_section": "Schedule of Benefits — Health Benefit Plan",
        "deductible": "Nil",
        "prescription_drug_max": "$2,000 per covered person per benefit year",
        "all_other_health_max": "$5,000 per covered person per benefit year (excluding Gender Affirmation)",
        "dental_max": "$1,000 per covered person per benefit year for all eligible dental services combined",
        "benefit_year": "September 1 to August 31 (12 consecutive months)",
        "notes": (
            "The health benefits are intended to supplement your provincial health insurance plan "
            "or provincial equivalent plan. Reimbursement will be limited to reasonable and "
            "customary charges, in addition to any specific limitations and maximums stated."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # 1. ADMINISTRATIVE
    # ─────────────────────────────────────────────────────────────────
    "Administrative": {
        "booklet_section": "[NOT IN BOOKLET — FLAG]",
        "co_pay": "[NOT IN BOOKLET — FLAG]",
        "annual_limit": "[NOT IN BOOKLET — FLAG]",
        "per_visit_limit": "N/A",
        "conditions": (
            "The booklet references pre-authorization processes (submit a Pre-Authorization Form "
            "to GreenShield) and provincial replacement plans (LINK/ZONE personal health plans "
            "if group benefits end), but these are not covered benefit categories with dollar limits. "
            "They are administrative procedures."
        ),
        "not_covered": "N/A — these are administrative processes, not benefit categories",
        "sub_groups": None,
        "flag": (
            "FLAG: 'Administrative' is not a covered benefit group in the booklet. "
            "'Estimate/Pre-Authorization' is described as a process (submit a Pre-Authorization "
            "Form to GreenShield), not a paid benefit. 'Provincial Replacement Plan' refers to "
            "LINK/ZONE plans available when group coverage ends. Please clarify whether these "
            "should map to a booklet section or be marked as process-only categories."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # 2. DENTAL
    # ─────────────────────────────────────────────────────────────────
    "Dental": {
        "booklet_section": "Dental Benefit Plan — Basic Services / Comprehensive Basic Services / Major Services",
        "co_pay": "Varies by tier — see sub_groups",
        "annual_limit": "$1,000 per covered person per benefit year for all eligible dental services combined",
        "per_visit_limit": "N/A",
        "conditions": (
            "Based on the current less 1 year Provincial Dental Association Fee Guide for General "
            "Practitioners in the province where services are rendered. For independent Dental "
            "Hygienists, the lesser of the current less 1 year Provincial Dental Hygienists' "
            "Association Fee Guide and Provincial Dental Association Fee Guide for General "
            "Practitioners in the province where services are rendered. Predetermination required "
            "before treatment when total cost is expected to exceed $500."
        ),
        "not_covered": (
            "Implants; restorations for wear/acid erosion/vertical dimension/restoring occlusion; "
            "appliances for myofacial pain syndrome; posterior cantilever pontics; sleep dentistry; "
            "TMJ diagnostic/repositioning appliances; cosmetic/aesthetic purposes; items from "
            "government agencies obtained without cost; motor vehicle accident injuries."
        ),
        "sub_groups": {
            "Dental Services — Basic diagnostic and preventive / periodontal scaling / basic oral surgery": {
                "co_pay": "0%",
                "annual_limit": "$1,000 per covered person per benefit year (combined for all dental)",
                "includes": (
                    "complete oral examinations once every 3 years based on date of first paid claim; "
                    "emergency and specific oral examinations; full series X-rays and panoramic X-rays "
                    "once every 3 years; bitewing X-rays once every 6 months; recall examinations once "
                    "every 6 months; cleaning of teeth (up to 1 unit of polishing plus up to 1 unit of "
                    "scaling) once per recall period; denture cleaning once every 6 months; pit and "
                    "fissure sealants on molars only for covered persons 14 years of age and under; "
                    "space maintainers; protective mouth guards once every 12 months; periodontal "
                    "scaling 3 time-units per benefit year; extractions of teeth (2 wisdom teeth "
                    "extractions per benefit year) and/or residual roots; general anaesthesia in "
                    "conjunction with eligible oral surgery only."
                ),
            },
            "Dental Services — Basic restorative / standard denture / comprehensive oral surgery / anaesthesia": {
                "co_pay": "25%",
                "annual_limit": "$1,000 per covered person per benefit year (combined for all dental)",
                "includes": (
                    "amalgam, tooth coloured filling restorations, and temporary sedative fillings; "
                    "inlay restorations (paid to the equivalent non-bonded amalgam); denture repairs "
                    "and/or tooth/teeth additions; standard relining and rebasing of dentures once "
                    "every 3 years; denture adjustments; soft tissue conditioning linings; remake of "
                    "a partial denture using existing framework once every 5 years; comprehensive "
                    "oral surgery (surgical exposure, repositioning, transplantation, enucleation, "
                    "remodeling, excision, incision, fractures, frenectomy)."
                ),
            },
            "Dental Services — Endodontic": {
                "co_pay": "70%",
                "annual_limit": "$1,000 per covered person per benefit year (combined for all dental)",
                "includes": (
                    "root canal therapy; pulpotomy; pulpectomy; apexification; apical curettage; "
                    "root resections and retrograde fillings; root amputation and hemisection; "
                    "bleaching of non-vital tooth/teeth; emergency procedures including opening or "
                    "draining of the gum/tooth; periodontal treatment of diseased bone and gums "
                    "including periodontal scaling 3 time units per benefit year."
                ),
            },
            "Dental Services — Major": {
                "co_pay": "70%",
                "annual_limit": "$1,000 per covered person per benefit year (combined for all dental)",
                "includes": (
                    "standard onlays or crown restorations to restore diseased or accidentally injured "
                    "natural teeth, once every 5 years based on date of first paid claim; standard "
                    "repair or recementing of crowns, onlays and bridge work on natural teeth."
                ),
            },
            "Accidental Dental": {
                "booklet_section": "Extended Health Services — Accidental Dental",
                "co_pay": "0%",
                "annual_limit": "Reasonable and customary charges",
                "conditions": (
                    "Dental care to natural teeth when necessitated by a direct blow to the mouth "
                    "and not by an object wittingly or unwittingly placed in the mouth. The accident "
                    "must occur while the coverage is in force. You must notify GreenShield immediately "
                    "following the accident and the treatment must commence within 180 days of the "
                    "accident. GreenShield will not be liable for any services performed after the "
                    "earlier of a) 365 days following the accident, or b) the date you or your "
                    "dependent cease to be covered under this plan. When natural teeth have been "
                    "damaged eligible services are limited to one set of artificial teeth."
                ),
                "not_covered": "No amount will be paid for periodontia or orthodontia treatments or the repair or replacement of artificial teeth.",
                "claim_note": "In the event of a dental accident, claims should be submitted under the health benefit plan before submitting them under the dental plan.",
            },
        },
        "flag": (
            "FLAG: The benefit_groups_list includes 'Orthodontic Services (Braces - initial and "
            "monthly fee)' and 'Other Orthodontic/Dental Services' under Dental. Orthodontic "
            "treatment (braces) is NOT explicitly listed as a covered dental service in the booklet. "
            "The dental sections cover Basic, Restorative, Endodontic, and Major — but orthodontics "
            "is not mentioned. Please confirm whether orthodontic services are covered and under "
            "which category/co-pay tier they fall."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # 3. EMERGENCY TRANSPORTATION
    # ─────────────────────────────────────────────────────────────────
    "Emergency Transportation": {
        "booklet_section": "Extended Health Services — Emergency Transportation",
        "co_pay": "0%",
        "annual_limit": "$250 per benefit year",
        "per_visit_limit": "N/A",
        "conditions": (
            "Reimbursement for professional land or air ambulance to the nearest hospital equipped "
            "to provide the required treatment, when medically required as the result of an injury, "
            "illness or acute physical disability."
        ),
        "not_covered": (
            "General health exclusions apply. Services received as a result of war, riot, criminal "
            "offence; services outside Canada on a non-emergency basis."
        ),
        "sub_groups": None,
        "flag": (
            "FLAG: The benefit_groups_list includes '[Emergency Transportation / Medical Items] "
            "Other emergency services'. The booklet only explicitly covers 'professional land or "
            "air ambulance'. It is unclear what other emergency services would be covered under "
            "this category. Please clarify what 'Other emergency services' encompasses."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # 4. HOSPITAL
    # ─────────────────────────────────────────────────────────────────
    "Hospital": {
        "booklet_section": "Schedule of Benefits — Hospital / Extended Health Services — Hospital Accommodation",
        "co_pay": "50%",
        "annual_limit": "Up to 5 days per disability",
        "per_visit_limit": "N/A",
        "conditions": (
            "Reimbursement of reasonable and customary charges in the area where received, for "
            "accommodation in a public general hospital, or a convalescent or rehabilitation hospital "
            "or a convalescent or rehabilitation wing in a public general hospital, or a public "
            "chronic hospital or chronic care in a public general hospital, provided your provincial "
            "health insurance plan has accepted or agreed to pay the ward or standard rate. "
            "Semi-private room means a room having only two treatment beds."
        ),
        "not_covered": "General health exclusions apply.",
        "sub_groups": None,
    },

    # ─────────────────────────────────────────────────────────────────
    # 5. MEDICAL ITEMS — AIDS FOR DAILY LIVING
    # ─────────────────────────────────────────────────────────────────
    "Medical Items - Aids for Daily Living": {
        "booklet_section": "Extended Health Services — Medical Items and Services (section a)",
        "co_pay": "0%",
        "annual_limit": "Reasonable and customary",
        "per_visit_limit": "N/A",
        "conditions": (
            "Reimbursement for reasonable and customary charges. Booklet lists: 'hospital style "
            "beds, including rails and mattresses; bedpans; standard commodes; decubitus "
            "(bedridden) supplies; I.V. stands; portable patient lifts; trapezes/transfer poles; "
            "urinals'. Some items may require pre-authorization. Durable medical equipment must "
            "be appropriate for use in the home, able to withstand repeated use and generally "
            "not useful in the absence of illness or injury. The rental price of durable medical "
            "equipment will not exceed the purchase price."
        ),
        "not_covered": (
            "Items that are not primarily medical in nature or that are for comfort and convenience "
            "are not eligible. Equipment that has been refurbished by the supplier for resale is "
            "not an eligible benefit."
        ),
        "sub_groups": None,
        "flag": (
            "FLAG: Some items in the benefit_groups_list (Bath Bench/Chair, Bed Rails, Grab Bar/"
            "Bath Bar, Raised Toilet Seat, Stationary Commode, Versa Frame, Wheeled Commode) "
            "broadly match the booklet's 'aids for daily living' description but are not named "
            "individually in the booklet. The booklet's list includes 'standard commodes' and "
            "'I.V. stands' but not every item by its exact name. Verify that each specific item "
            "in the list is considered eligible under this category."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # 6. MEDICAL ITEMS — BRACES AND CASTS
    # ─────────────────────────────────────────────────────────────────
    "Medical Items - Braces and Casts": {
        "booklet_section": "Schedule of Benefits — Medical Items and Services / Extended Health Services — Medical Items and Services (section b)",
        "co_pay": "50%",
        "annual_limit": "$500 per benefit year combined",
        "per_visit_limit": "N/A",
        "conditions": (
            "Reimbursement for reasonable and customary charges for braces, casts. Some items "
            "may require pre-authorization. To confirm eligibility prior to purchasing or renting "
            "equipment, submit a Pre-Authorization Form to GreenShield."
        ),
        "not_covered": "General health exclusions apply.",
        "sub_groups": None,
        "flag": (
            "FLAG: The benefit_groups_list includes 'Other garment brace services (i.e. compression "
            "gloves)'. Compression gloves are not explicitly mentioned in the booklet under Braces "
            "and Casts. They may fall under Medical Items - Compression Stockings or Medical Items "
            "- Other. Please clarify."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # 7. MEDICAL ITEMS — COMPRESSION STOCKINGS
    # ─────────────────────────────────────────────────────────────────
    "Medical Items - Compression Stockings": {
        "booklet_section": "Schedule of Benefits — Medical Items and Services / Extended Health Services — Medical Items and Services (section g)",
        "co_pay": "50%",
        "annual_limit": "$500 per benefit year",
        "per_visit_limit": "N/A",
        "conditions": (
            "Compression stockings with a pressure measurement of 15 mmhg or higher. "
            "Some items may require pre-authorization."
        ),
        "not_covered": (
            "Compression stockings with a pressure measurement below 15 mmhg are NOT covered. "
            "General health exclusions apply."
        ),
        "sub_groups": None,
        "flag": (
            "FLAG: The benefit_groups_list includes 'Compression Stockings, any length (up to "
            "14 mmhg)'. The booklet explicitly requires 'a pressure measurement of 15 mmhg or "
            "higher', so stockings up to 14 mmhg are NOT covered under this plan. This must be "
            "reflected in the chatbot logic."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # 8. MEDICAL ITEMS — DIABETIC SUPPLIES
    # ─────────────────────────────────────────────────────────────────
    "Medical Items - Diabetic Supplies": {
        "booklet_section": "Prescription Drugs (for supplies/injectables) — see flag",
        "co_pay": "20% per prescription or refill (for drug/supply items covered under Prescription Drugs)",
        "annual_limit": "$2,000 per covered person per benefit year (Prescription Drugs maximum)",
        "per_visit_limit": "N/A",
        "conditions": (
            "The Prescription Drugs section states: 'this plan includes drugs with a Drug "
            "Identification Number (DIN) that do not legally require a prescription, including "
            "insulin and all other approved injectables, as well as related supplies such as "
            "diabetic syringes, needles and testing agents.' These are covered under the "
            "Prescription Drug benefit (Pay Direct Drug Card) at 20% co-pay."
        ),
        "not_covered": (
            "Insulin pumps and supplies are explicitly excluded in Health Exclusions: 'are for "
            "Insulin pumps and supplies (unless specifically identified and included as eligible "
            "under the plan)' — and the booklet does NOT specifically include them. Medical "
            "cannabis is NOT covered. General health exclusions apply."
        ),
        "sub_groups": None,
        "flag": (
            "FLAG — REQUIRES YOUR DECISION: This group overlaps two booklet sections:\n"
            "1. PRESCRIPTION DRUGS section: covers 'insulin and all other approved injectables, "
            "as well as related supplies such as diabetic syringes, needles and testing agents' "
            "at 20% co-pay, up to $2,000/year. This likely covers: Lancet, Insulin Pen Injector, "
            "Insulin Gun (auto/manual), alcohol swabs, and testing agents.\n"
            "2. MEDICAL ITEMS section: Blood glucose meters and CGM systems "
            "(Receiver, Transmitter, Sensors/Supplies) are not explicitly listed in the booklet's "
            "Medical Items section. They may fall under 'Other items and services' at 0% co-pay "
            "and reasonable & customary, but this is not certain.\n"
            "3. INSULIN PUMPS: The Health Exclusions section explicitly states 'are for Insulin "
            "pumps and supplies (unless specifically identified and included as eligible under "
            "the plan)' — and they are NOT specified as eligible. This means 'Insulin infusion "
            "pump' and 'Insulin infusion pump supplies' from the benefit_groups_list appear to "
            "be NOT COVERED.\n"
            "Please confirm: (a) Which diabetic supply items map to Prescription Drugs vs Medical "
            "Items? (b) Are CGM devices (Receiver, Transmitter, Sensors) covered under Medical "
            "Items - Other? (c) Confirm insulin pumps are excluded."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # 9. MEDICAL ITEMS — DIAGNOSTIC TESTS
    # ─────────────────────────────────────────────────────────────────
    "Medical Items - Diagnostic Tests": {
        "booklet_section": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
        "co_pay": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
        "annual_limit": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
        "per_visit_limit": "N/A",
        "conditions": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
        "not_covered": (
            "Health Exclusions note that services 'would normally be paid through any provincial "
            "health insurance plan... or which would have been payable under such a plan had proper "
            "application for coverage been made' are excluded. Many diagnostic tests (X-rays, "
            "ultrasounds, MRIs) are typically covered by provincial plans. The booklet does not "
            "contain a dedicated Diagnostic Tests section."
        ),
        "sub_groups": None,
        "flag": (
            "FLAG — REQUIRES YOUR INPUT: The booklet does not contain a dedicated 'Diagnostic "
            "Tests' section. The Medical Items and Services section lists aids for daily living, "
            "braces, incontinence/ostomy, mobility aids, prosthetics, respiratory equipment, and "
            "compression stockings — but not diagnostic tests. The 16 categories listed in "
            "benefit_groups_list (MRI, Ultrasound, X-Ray, Blood tests, Colonoscopy, Sleep Study, "
            "etc.) are not explicitly mentioned as covered benefits. Many would typically be "
            "covered by provincial health plans (and therefore excluded from this plan). "
            "Please advise how diagnostic tests should be handled in the chatbot."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # 10. MEDICAL ITEMS — INCONTINENCE/OSTOMY
    # ─────────────────────────────────────────────────────────────────
    "Medical Items - Incontinence/Ostomy": {
        "booklet_section": "Extended Health Services — Medical Items and Services (section c)",
        "co_pay": "0%",
        "annual_limit": "Reasonable and customary",
        "per_visit_limit": "N/A",
        "conditions": (
            "Reimbursement for reasonable and customary charges for 'Incontinence/Ostomy "
            "equipment, such as catheter supplies and ostomy supplies'. Some items may require "
            "pre-authorization."
        ),
        "not_covered": "General health exclusions apply.",
        "sub_groups": None,
    },

    # ─────────────────────────────────────────────────────────────────
    # 11. MEDICAL ITEMS — MOBILITY AIDS
    # ─────────────────────────────────────────────────────────────────
    "Medical Items - Mobility Aids": {
        "booklet_section": "Extended Health Services — Medical Items and Services (section d)",
        "co_pay": "0%",
        "annual_limit": "Reasonable and customary",
        "per_visit_limit": "N/A",
        "conditions": (
            "Reimbursement for reasonable and customary charges for 'Mobility aids, such as "
            "canes, crutches, walkers and wheelchairs (including wheelchair batteries)'. "
            "The rental price of durable medical equipment will not exceed the purchase price. "
            "Some items may require pre-authorization."
        ),
        "not_covered": (
            "Equipment that has been refurbished by the supplier for resale is not an eligible "
            "benefit. Items not primarily medical in nature or for comfort and convenience are "
            "not eligible. General health exclusions apply."
        ),
        "sub_groups": None,
    },

    # ─────────────────────────────────────────────────────────────────
    # 12. MEDICAL ITEMS — OTHER
    # ─────────────────────────────────────────────────────────────────
    "Medical Items - Other": {
        "booklet_section": "Extended Health Services — Medical Items and Services (general / 'Other items and services')",
        "co_pay": "0%",
        "annual_limit": "Reasonable and customary",
        "per_visit_limit": "N/A",
        "conditions": (
            "Schedule of Benefits states: 'Other items and services – See the Description of "
            "Benefits section for details' at 0% co-pay, reasonable and customary. Items must be "
            "medically necessary for the treatment of an illness or injury."
        ),
        "not_covered": (
            "Items that are not primarily medical in nature or for comfort and convenience; "
            "video instructional kits, informational manuals or pamphlets; batteries (unless "
            "specifically included); duplicate prosthetic devices; replacements for lost/stolen "
            "items. General health exclusions apply."
        ),
        "sub_groups": None,
        "flag": (
            "FLAG: The benefit_groups_list contains several items under 'Medical Items - Other' "
            "that are not individually named in the booklet:\n"
            "- Breast Pump: Not explicitly listed. May qualify as medical equipment if prescribed.\n"
            "- Cervical Pillow: Not explicitly listed. May be considered comfort/convenience "
            "and therefore not eligible.\n"
            "- Cold Therapy / Heat Therapy (re-usable): Not explicitly listed.\n"
            "- Medic Alert Bracelet: Not explicitly listed.\n"
            "- Nursing Home and Long Term Care: Not explicitly listed as a covered benefit. "
            "Would likely be provincial plan territory.\n"
            "- Stimulator, muscle/nerve (TENS): Not explicitly listed by name, but may qualify "
            "under medical equipment.\n"
            "- Stimulator, supplies: Same as above.\n"
            "Please advise how each should be handled."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # 13. MEDICAL ITEMS — PROSTHETICS
    # ─────────────────────────────────────────────────────────────────
    "Medical Items - Prosthetics": {
        "booklet_section": "Extended Health Services — Medical Items and Services (section e)",
        "co_pay": "0%",
        "annual_limit": "Reasonable and customary",
        "per_visit_limit": "N/A",
        "conditions": (
            "Reimbursement for 'Standard prosthetics, such as an arm, hand, leg, foot, breast, "
            "eye and larynx'. Some items may require pre-authorization. Replacements are eligible "
            "when required due to natural wear, growth or relevant change in your medical condition "
            "but only when the equipment/prostheses cannot be adjusted or repaired at a lesser cost "
            "and the item is still medically required."
        ),
        "not_covered": (
            "Duplicate prosthetic device or appliance; replacements for lost, missing or stolen "
            "items or items damaged due to negligence. General health exclusions apply."
        ),
        "sub_groups": None,
        "flag": (
            "FLAG: The benefit_groups_list includes 'Mastectomy bra' and 'Wig' under Prosthetics.\n"
            "- Mastectomy bra: The booklet lists 'breast' under standard prosthetics; a mastectomy "
            "bra is related but not the same as a breast prosthetic. It is not named explicitly.\n"
            "- Wig: Not listed in the booklet's prosthetics section (arm, hand, leg, foot, breast, "
            "eye, larynx). A wig may be considered a prosthetic for hair loss due to cancer "
            "treatment, but this is not stated in the booklet.\n"
            "Please confirm whether mastectomy bras and wigs are intended to be covered under "
            "this plan."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # 14. MEDICAL ITEMS — RESPIRATORY EQUIPMENT
    # ─────────────────────────────────────────────────────────────────
    "Medical Items - Respiratory Equipment": {
        "booklet_section": "Extended Health Services — Medical Items and Services (section f)",
        "co_pay": "0%",
        "annual_limit": "Reasonable and customary",
        "per_visit_limit": "N/A",
        "conditions": (
            "Reimbursement for 'Respiratory/Cardiology equipment, such as compressors, inhalant "
            "devices, tracheotomy supplies and oxygen'. Some items may require pre-authorization. "
            "The rental price of durable medical equipment will not exceed the purchase price."
        ),
        "not_covered": (
            "Equipment that has been refurbished by the supplier for resale; items not primarily "
            "medical in nature or for comfort and convenience. General health exclusions apply."
        ),
        "sub_groups": None,
        "flag": (
            "FLAG: The benefit_groups_list includes 'Blood pressure monitor' under Respiratory "
            "Equipment. The booklet groups this under 'Respiratory/Cardiology equipment' which "
            "broadly covers cardiology equipment, so a blood pressure monitor may qualify. "
            "However, it is not named explicitly. Also, 'Humidifier (Table Top)' and "
            "'Vaporizer (table top)' are not named in the booklet's respiratory equipment list. "
            "Please confirm these items are intended to be covered."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # 15. PRESCRIPTION DRUGS
    # ─────────────────────────────────────────────────────────────────
    "Prescription Drugs": {
        "booklet_section": "Health Benefit Plan — Prescription Drugs / Schedule of Benefits — Prescription Drug Benefit",
        "co_pay": "20% per prescription or refill (all other covered drugs). Special rates apply — see sub_groups.",
        "annual_limit": "$2,000 per covered person per benefit year",
        "per_visit_limit": "N/A",
        "conditions": (
            "Drugs must be: (a) prescribed by a legally qualified medical practitioner or dental "
            "practitioner as permitted by law; (b) legally require a prescription and have a Drug "
            "Identification Number (DIN); (c) approved under GreenShield's drug review process; "
            "(d) paid on a Pay Direct basis. Maintenance drugs required to treat lifelong chronic "
            "conditions may be required to be purchased in a 90-day supply at any one time. "
            "Non-maintenance drugs may be purchased in a supply not exceeding 3-months (90-day) "
            "supply at any one time. For all drugs, 6 months for a vacation supply may be purchased "
            "and not more than a 13-month supply in any 12 consecutive months. Generic substitution "
            "applies: reimbursement will be made for the cost of the lowest priced equivalent drug "
            "based on specific provincial regulations unless 'no substitution' is specified."
        ),
        "not_covered": (
            "Drugs for the treatment of obesity, erectile dysfunction and infertility; "
            "vitamins that do not legally require a prescription; smoking cessation drugs and "
            "nicotine replacement products (patches, gum, lozenges, inhalers); products which "
            "may lawfully be sold other than through retail pharmacies; ingredients not approved "
            "by Health Canada; compounded mixtures that do not conform to GreenShield's current "
            "Compound Policy; ANY FORM OF MEDICAL CANNABIS for the treatment of any medical "
            "condition, regardless of whether it is authorized by way of a medical document or "
            "prescription (explicitly excluded in Health Exclusions section 6)."
        ),
        "sub_groups": {
            "Drug (standard)": {
                "co_pay": "20% per prescription or refill",
                "annual_limit": "$2,000 per covered person per benefit year",
            },
            "Contraceptives — Oral Contraceptives": {
                "co_pay": "10% per prescription or refill",
                "annual_limit": "$350 per benefit year (included in the Prescription Drug maximum)",
            },
            "Contraceptives — Other (injections, IUD's and patch)": {
                "co_pay": "10% per prescription or refill",
                "annual_limit": "$350 per benefit year (included in the Prescription Drug maximum)",
            },
            "HPV vaccines": {
                "co_pay": "20% per prescription or refill",
                "annual_limit": "Reasonable and customary charges (included in the Prescription Drugs Maximum)",
            },
            "All other vaccines": {
                "co_pay": "50% per prescription or refill",
                "annual_limit": "Reasonable and customary charges (included in the Prescription Drugs Maximum)",
            },
            "Alcohol swabs": {
                "co_pay": "20% per prescription or refill (covered as diabetic supply/related supply)",
                "annual_limit": "$2,000 per covered person per benefit year (combined Rx max)",
                "note": (
                    "Booklet states the plan includes 'related supplies such as diabetic syringes, "
                    "needles and testing agents'. Alcohol swabs are not named explicitly but are "
                    "commonly considered related diabetic supplies — FLAG for confirmation."
                ),
            },
            "Medical Cannabis": {
                "co_pay": "NOT COVERED",
                "annual_limit": "NOT COVERED",
                "note": (
                    "Explicitly excluded: 'Any form of medical cannabis for the treatment of any "
                    "medical condition, regardless of whether it is authorized by way of a medical "
                    "document or prescription from a legally-authorized medical practitioner and "
                    "obtained from a Health Canada-licensed producer pursuant to any federal or "
                    "provincial legislation or regulation regarding access to and/or distribution "
                    "of medical cannabis.'"
                ),
            },
        },
    },

    # ─────────────────────────────────────────────────────────────────
    # 16. PRIVATE DUTY NURSING
    # ─────────────────────────────────────────────────────────────────
    "Private Duty Nursing": {
        "booklet_section": "Schedule of Benefits — Private Duty Nursing in the Home / Extended Health Services — Private Duty Nursing in the Home",
        "co_pay": "0%",
        "annual_limit": "Minimum 8 hours per shift (limited to reasonable and customary charges)",
        "per_visit_limit": "N/A",
        "conditions": (
            "Reimbursement for the services of a Registered Nurse (R.N.) in the home on a visit "
            "or shift basis. A Pre-Authorization Form for Private Duty Nursing must be completed "
            "by the attending physician and submitted to GreenShield."
        ),
        "not_covered": (
            "No amount will be paid for services which are custodial and/or services which do not "
            "require the skill level of a Registered Nurse (R.N.). General health exclusions apply."
        ),
        "sub_groups": None,
    },

    # ─────────────────────────────────────────────────────────────────
    # 17. PROFESSIONAL SERVICES
    # ─────────────────────────────────────────────────────────────────
    "Professional Services": {
        "booklet_section": "Schedule of Benefits — Professional Services / Extended Health Services — Professional Services",
        "co_pay": "0%",
        "annual_limit": "Varies by sub-group — see sub_groups",
        "per_visit_limit": "Varies by sub-group — see sub_groups",
        "conditions": (
            "Reimbursement for the services of practitioners included, when the practitioner "
            "rendering the service is licensed by their provincial regulatory agency or a registered "
            "member of a professional association and that association is recognized by GreenShield. "
            "Please contact the GreenShield Customer Service Centre to confirm practitioner eligibility."
        ),
        "not_covered": (
            "Practitioners not licensed by their provincial regulatory agency or not recognized "
            "by GreenShield. General health exclusions apply."
        ),
        "sub_groups": {
            "Professional Services Group A": {
                "practitioners": "Chiropractor; Registered Massage Therapist; Naturopath; Speech Therapist; Physiotherapist",
                "co_pay": "0%",
                "per_visit_limit": "$50 per visit",
                "annual_limit": "$500 per practitioner per benefit year",
                "note": "Booklet text: '$50 per visit, limited to $500 per practitioner per benefit year'",
            },
            "Professional Services Group B": {
                "practitioners": "Psychologist; Psychotherapist; Social Worker; Clinical Counsellor or Master of Social Work",
                "co_pay": "0%",
                "per_visit_limit": "$80 per visit",
                "annual_limit": "$1,000 per benefit year combined",
                "note": "Booklet text: '$80 per visit, limited to $1,000 per benefit year combined'",
            },
            "Holistic Nutritional Consultant": {
                "co_pay": "0%",
                "per_visit_limit": "$80 per visit",
                "annual_limit": "Combined with the overall maximum of $1,000 per benefit year for Psychologist, Psychotherapist, Social Worker, Clinical Counsellor and Master of Social Work",
                "note": (
                    "Booklet text: '$80 per visit combined with the overall maximum of $1,000 per "
                    "benefit year for Psychologist, Psychotherapist, Social Worker, Clinical "
                    "Counsellor and Master of Social Work'. NOTE: 'Holistic Nutritional Consultant' "
                    "appears in the booklet Schedule but NOT in the benefit_groups_list.txt. "
                    "The benefit_groups_list has 'Dietitian Services' under Allied Health instead."
                ),
            },
            "Professional Services - Allied Health": {
                "practitioners": "Acupuncture; Athletic Therapy; Dietitian Services; Homeopathic Treatment; Occupational Therapy; Osteopath",
                "co_pay": "[NOT EXPLICITLY IN BOOKLET SCHEDULE — FLAG]",
                "per_visit_limit": "[NOT EXPLICITLY IN BOOKLET SCHEDULE — FLAG]",
                "annual_limit": "[NOT EXPLICITLY IN BOOKLET SCHEDULE — FLAG]",
                "note": (
                    "FLAG: These practitioners are NOT listed in the Schedule of Benefits under "
                    "Professional Services. The Schedule only names Group A (Chiropractor, RMT, "
                    "Naturopath, Speech Therapist, Physiotherapist) and Group B (Psychologist, "
                    "Psychotherapist, Social Worker, Clinical Counsellor, MSW). Allied Health "
                    "practitioners are not mentioned. Please confirm their coverage and rates."
                ),
            },
            "Digital Cognitive Behavioural Therapy": {
                "co_pay": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
                "per_visit_limit": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
                "annual_limit": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
                "note": (
                    "FLAG: 'Digital Cognitive Behavioural Therapy' is not mentioned in the booklet. "
                    "It appears in the benefit_groups_list under Group B. If it is intended to fall "
                    "under Group B, it would be $80/visit up to $1,000/year combined — but this "
                    "must be confirmed as the booklet does not list it."
                ),
            },
            "Other mental health services": {
                "co_pay": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
                "per_visit_limit": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
                "annual_limit": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
                "note": (
                    "FLAG: 'Other mental health services' is listed in benefit_groups_list under "
                    "Group B but not named in the booklet. If intended to fall under Group B, it "
                    "would be $80/visit, $1,000/year combined — but this must be confirmed."
                ),
            },
        },
    },

    # ─────────────────────────────────────────────────────────────────
    # 18. PROFESSIONAL SERVICES — FOOT CARE
    # ─────────────────────────────────────────────────────────────────
    "Professional Services - Foot Care": {
        "booklet_section": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
        "co_pay": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
        "annual_limit": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
        "per_visit_limit": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
        "conditions": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
        "not_covered": "General health exclusions apply.",
        "sub_groups": None,
        "flag": (
            "FLAG — REQUIRES YOUR INPUT: Foot care services (Chiropody, Podiatry, Orthotics, "
            "Orthopaedic shoes) are NOT mentioned anywhere in the booklet's Schedule of Benefits "
            "or Description of Benefits. The Professional Services section only lists "
            "Chiropractor, RMT, Naturopath, Speech Therapist, Physiotherapist (Group A), and "
            "Psychologist/Psychotherapist/Social Worker/Clinical Counsellor/MSW (Group B). "
            "None of the 6 foot care categories in the benefit_groups_list appear in the booklet. "
            "Please confirm: (a) Are foot care services covered? (b) If so, under which booklet "
            "section and at what rate? (c) Do custom foot orthotics fall under Medical Items or "
            "Professional Services?"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # 19. PROFESSIONAL SERVICES — HEARING
    # ─────────────────────────────────────────────────────────────────
    "Professional Services - Hearing": {
        "booklet_section": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
        "co_pay": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
        "annual_limit": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
        "per_visit_limit": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
        "conditions": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
        "not_covered": (
            "Health Exclusions explicitly state: 'are for medical examinations, audiometric "
            "examinations or hearing aid evaluation tests unless specifically identified and "
            "included as eligible under the plan'. These services are NOT specifically identified "
            "as eligible in the Schedule or Description of Benefits."
        ),
        "sub_groups": None,
        "flag": (
            "FLAG — REQUIRES YOUR INPUT: Hearing services (Audiologist, Audiometric Exam, "
            "Ear Plugs, Hearing Aids) are NOT listed in the booklet's Schedule of Benefits. "
            "Furthermore, the Health Exclusions section explicitly excludes 'audiometric "
            "examinations or hearing aid evaluation tests unless specifically identified and "
            "included as eligible under the plan' — and they are NOT so identified. This "
            "suggests hearing services may be EXCLUDED from this plan. Please confirm whether "
            "any hearing services are intended to be covered and, if so, at what rate."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # 20. VISION
    # ─────────────────────────────────────────────────────────────────
    "Vision": {
        "booklet_section": "Schedule of Benefits — Vision / Extended Health Services — Vision",
        "co_pay": "0%",
        "annual_limit": "Varies by service — see sub_groups",
        "per_visit_limit": "N/A",
        "conditions": (
            "Reimbursement for services performed by a licensed Optometrist, Optician or "
            "Ophthalmologist."
        ),
        "not_covered": (
            "Medical or surgical treatment; special or unusual procedures such as orthoptics, "
            "vision training, subnormal vision aids and aniseikonic lenses; follow-up visits "
            "associated with the dispensing and fitting of contact lenses; charges for eyeglass cases."
        ),
        "sub_groups": {
            "Prescription Glasses / Prescription Contacts": {
                "co_pay": "0%",
                "limit": "$150 per 24 months based on date of first paid claim",
                "includes": (
                    "Prescription eyeglasses or contact lenses; medically necessary contact lenses "
                    "when visual acuity cannot otherwise be corrected to at least 20/40 in the "
                    "better eye or when medically necessary due to keratoconus, irregular "
                    "astigmatism, irregular corneal curvature or physical deformity resulting in "
                    "an inability to wear normal frames; replacement parts for prescription eyeglasses; "
                    "non-prescription sunglasses prescribed by a legally qualified medical practitioner "
                    "for the treatment of specific ophthalmic diseases or conditions."
                ),
            },
            "Eye Exam / Diagnostic Vision Test": {
                "co_pay": "0%",
                "limit": "$75 for one eye exam every 2 years based on date of first paid claim",
                "conditions": (
                    "Optometric eye examinations for visual acuity performed by a licensed "
                    "optometrist, ophthalmologist or physician. Available only in those provinces "
                    "where eye examinations are not covered by the provincial health insurance plan."
                ),
            },
            "Safety Glasses / Other vision services": {
                "co_pay": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
                "limit": "[NOT EXPLICITLY IN BOOKLET — FLAG]",
                "note": (
                    "FLAG: 'Safety Glasses' and 'Other vision services' are listed in the "
                    "benefit_groups_list under Vision. The booklet does not explicitly list "
                    "safety glasses as a covered vision benefit. The Schedule of Benefits "
                    "lists only prescription eyeglasses/contacts ($150/24 months) and eye "
                    "exams ($75/2 years). Please confirm whether safety glasses are intended "
                    "to be covered and, if so, at what limit."
                ),
            },
        },
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# SUMMARY OF FLAGS — Items requiring your input before chatbot can answer
# ─────────────────────────────────────────────────────────────────────────────

flags_requiring_input = [
    {
        "group": "Administrative",
        "question": (
            "'Estimate/Pre-Authorization' and 'Provincial Replacement Plan' are not benefit "
            "categories with coverage rates in the booklet — they are administrative processes. "
            "How should the chatbot handle claims submitted under these categories?"
        ),
    },
    {
        "group": "Dental — Orthodontic Services",
        "question": (
            "The benefit_groups_list includes 'Orthodontic Services (Braces)' and 'Other "
            "Orthodontic/Dental Services' but the booklet does not list orthodontics anywhere "
            "in the dental sections. Are these covered? If so, at which co-pay tier?"
        ),
    },
    {
        "group": "Emergency Transportation — Other emergency services",
        "question": (
            "The booklet only covers 'professional land or air ambulance'. What does 'Other "
            "emergency services' in the benefit_groups_list refer to?"
        ),
    },
    {
        "group": "Medical Items - Diabetic Supplies — Device coverage split",
        "question": (
            "Which diabetic supply items (Blood glucose meter, CGM Receiver/Transmitter/Sensors, "
            "Insulin Guns, Lancet, Insulin Pen) fall under Prescription Drugs vs Medical Items? "
            "And please confirm: are insulin pumps and supplies EXCLUDED per the health exclusions?"
        ),
    },
    {
        "group": "Medical Items - Diagnostic Tests",
        "question": (
            "There is no dedicated Diagnostic Tests section in the booklet. How should the "
            "chatbot respond to claims for MRI, Ultrasound, X-Ray, Sleep Study, Blood Tests, "
            "Colonoscopy, Mammogram, PSA Test, etc.? Are any of these covered?"
        ),
    },
    {
        "group": "Medical Items - Prosthetics — Wig and Mastectomy Bra",
        "question": (
            "The booklet lists 'breast' under standard prosthetics but does not name mastectomy "
            "bras or wigs. Are these intended to be covered? At what rate?"
        ),
    },
    {
        "group": "Medical Items - Other — Individual items",
        "question": (
            "Please confirm coverage intent for: Breast Pump, Cervical Pillow, Cold/Heat "
            "Therapy items, Medic Alert Bracelet, Nursing Home/Long Term Care, and TENS "
            "Stimulator. None are named explicitly in the booklet."
        ),
    },
    {
        "group": "Medical Items - Braces — Compression Gloves",
        "question": (
            "'Other garment brace services (i.e. compression gloves)' is in the benefit_groups_list "
            "under Braces. Should this fall under Braces (50% co-pay, $500/yr) or Compression "
            "Stockings (50% co-pay, $500/yr) or Medical Items - Other (0%, R&C)?"
        ),
    },
    {
        "group": "Professional Services — Allied Health",
        "question": (
            "Acupuncture, Athletic Therapy, Dietitian Services, Homeopathic Treatment, "
            "Occupational Therapy, and Osteopath are NOT in the booklet's Schedule of Benefits. "
            "Are they covered? If so, are they Group A ($50/visit, $500/yr) or Group B "
            "($80/visit, $1,000/yr combined) or another rate?"
        ),
    },
    {
        "group": "Professional Services — Digital CBT and Other mental health services",
        "question": (
            "'Digital Cognitive Behavioural Therapy' and 'Other mental health services' are in "
            "the benefit_groups_list under Group B but not named in the booklet. Are they covered "
            "under Group B rates ($80/visit, $1,000/yr combined)?"
        ),
    },
    {
        "group": "Professional Services - Foot Care",
        "question": (
            "Chiropody, Podiatry, custom orthotics, orthopaedic shoes are NOT in the booklet. "
            "Are any foot care services covered? If so, at what rate and under which section?"
        ),
    },
    {
        "group": "Professional Services - Hearing",
        "question": (
            "Audiologist, Audiometric Exam, Ear Plugs, Hearing Aids are NOT in the booklet "
            "Schedule. The Health Exclusions section explicitly excludes audiometric exams "
            "and hearing aid evaluation tests 'unless specifically identified and included as "
            "eligible under the plan' — and they are not. Are hearing services covered? "
            "If so, at what rate?"
        ),
    },
    {
        "group": "Vision — Safety Glasses",
        "question": (
            "Safety Glasses are not explicitly listed in the booklet's vision benefit. "
            "Are they covered? If so, are they within the $150/24-month prescription "
            "eyewear limit or a separate amount?"
        ),
    },
    {
        "group": "Medical Items - Respiratory — Specific devices",
        "question": (
            "Blood pressure monitor, Humidifier (table top), Vaporizer (table top), "
            "Aerochamber, CPAP/APAP/BIPAP machine/mask/supplies, and Peak Flow Meter "
            "are not individually named in the booklet. The booklet lists 'compressors, "
            "inhalant devices, tracheotomy supplies and oxygen' as examples. "
            "Please confirm these devices are all intended to be covered."
        ),
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# AMBIGUOUS BOOKLET TEXT — For your review
# ─────────────────────────────────────────────────────────────────────────────

booklet_ambiguities = [
    {
        "topic": "Medical Items and Services — Schedule vs Description",
        "booklet_text": (
            "Schedule of Benefits: 'Other items and services – See the Description of Benefits "
            "section for details' at 0% co-pay, reasonable and customary. The Description of "
            "Benefits lists categories (a) through (g) but uses 'such as' language, suggesting "
            "the lists are examples, not exhaustive."
        ),
        "ambiguity": (
            "It is unclear which specific items qualify under 'other items and services' beyond "
            "the examples given. This affects many items in the benefit_groups_list."
        ),
    },
    {
        "topic": "Diabetic Supplies — Prescription Drugs vs Medical Items",
        "booklet_text": (
            "Prescription Drugs section: 'this plan includes drugs with a Drug Identification "
            "Number (DIN) that do not legally require a prescription, including insulin and all "
            "other approved injectables, as well as related supplies such as diabetic syringes, "
            "needles and testing agents.' Health Exclusions: 'are for Insulin pumps and supplies "
            "(unless specifically identified and included as eligible under the plan).'"
        ),
        "ambiguity": (
            "Unclear which diabetic devices (glucose meters, CGM systems) fall under Prescription "
            "Drugs vs Medical Items. Insulin pumps appear excluded."
        ),
    },
    {
        "topic": "Professional Services — Allied Health practitioners",
        "booklet_text": (
            "Schedule of Benefits Professional Services section does not mention Acupuncture, "
            "Athletic Therapy, Dietitian, Homeopathic Treatment, Occupational Therapy, or Osteopath. "
            "Description of Benefits says: 'Reimbursement for the services of the practitioners "
            "included, up to the amount shown in the Schedule of Benefits.'"
        ),
        "ambiguity": (
            "If Allied Health practitioners are not in the Schedule, it is unclear whether they "
            "are covered at all, or at which rate."
        ),
    },
    {
        "topic": "Holistic Nutritional Consultant in booklet vs benefit_groups_list",
        "booklet_text": (
            "Schedule of Benefits: 'Holistic Nutritional Consultant $80 per visit combined with "
            "the overall maximum of $1,000 per benefit year for Psychologist, Psychotherapist, "
            "Social Worker, Clinical Counsellor and Master of Social Work.'"
        ),
        "ambiguity": (
            "'Holistic Nutritional Consultant' appears in the booklet but NOT in the "
            "benefit_groups_list. The benefit_groups_list has 'Dietitian Services' under "
            "Allied Health. Are these the same? Or separate practitioners?"
        ),
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# JSON OUTPUT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    output = {
        "coverage_by_group": coverage_by_group,
        "flags_requiring_input": flags_requiring_input,
        "booklet_ambiguities": booklet_ambiguities,
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
