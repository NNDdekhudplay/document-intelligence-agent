"""
Run this script once to generate sample/sample_contract.pdf.
Usage: python sample/create_sample.py
Requires: reportlab (included in requirements.txt)
"""

import os
from pathlib import Path
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


OUTPUT_PATH = Path(__file__).parent / "sample_contract.pdf"


def build_pdf():
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=LETTER,
        leftMargin=1.1 * inch,
        rightMargin=1.1 * inch,
        topMargin=1.0 * inch,
        bottomMargin=1.0 * inch,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=6,
        textColor=colors.HexColor("#1a1a2e"),
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=18,
        textColor=colors.HexColor("#444444"),
    )
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=12,
        spaceBefore=14,
        spaceAfter=4,
        textColor=colors.HexColor("#1a1a2e"),
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    )
    label_style = ParagraphStyle(
        "Label",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        spaceAfter=4,
    )

    story = []

    # Title block
    story.append(Paragraph("SOFTWARE DEVELOPMENT SERVICES AGREEMENT", title_style))
    story.append(Paragraph("Contract Reference: SDA-2025-0042", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 14))

    # Parties
    story.append(Paragraph("PARTIES", section_style))
    story.append(Paragraph(
        "<b>Client:</b> Meridian Ventures Pte. Ltd., a company incorporated under the laws of Singapore, "
        "with registered address at 18 Cross Street, #10-08 China Square Central, Singapore 048423. "
        "Represented by <b>Ms. Rachel Tan Wei Ling</b>, Chief Executive Officer.",
        label_style,
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Service Provider:</b> Codecraft Technologies Ltd., a company registered in England and Wales "
        "(Company No. 12847563), with principal office at 4 Charterhouse Square, London, EC1M 6EA, UK. "
        "Represented by <b>Mr. James Harrington</b>, Managing Director.",
        label_style,
    ))

    story.append(Paragraph("AGREEMENT DATE", section_style))
    story.append(Paragraph(
        "This Agreement is entered into as of <b>March 1, 2025</b>, and shall remain in effect "
        "through <b>February 28, 2026</b>, unless terminated earlier in accordance with Section 9.",
        body_style,
    ))

    # Section 1 — Scope
    story.append(Paragraph("1. SCOPE OF SERVICES", section_style))
    story.append(Paragraph(
        "Codecraft Technologies Ltd. agrees to design, develop, test, and deliver a cloud-based "
        "inventory management platform ('the Platform') as specified in Schedule A attached hereto. "
        "The Platform shall include: (a) a web-based dashboard accessible via modern browsers; "
        "(b) RESTful API integration with Meridian's existing ERP system (SAP Business One); "
        "(c) real-time stock tracking across three warehouse locations in Singapore, Kuala Lumpur, "
        "and Jakarta; and (d) automated low-stock alert notifications via email and SMS.",
        body_style,
    ))

    # Section 2 — Fees
    story.append(Paragraph("2. FEES AND PAYMENT SCHEDULE", section_style))
    story.append(Paragraph(
        "The total contract value is <b>USD 120,000</b> (One Hundred Twenty Thousand US Dollars), "
        "payable in four installments as follows:",
        body_style,
    ))
    story.append(Paragraph(
        "&#8226;  <b>USD 30,000</b> — upon execution of this Agreement (March 1, 2025)<br/>"
        "&#8226;  <b>USD 30,000</b> — upon delivery of the prototype (June 1, 2025)<br/>"
        "&#8226;  <b>USD 40,000</b> — upon User Acceptance Testing completion (October 1, 2025)<br/>"
        "&#8226;  <b>USD 20,000</b> — upon go-live and final handover (January 15, 2026)",
        label_style,
    ))
    story.append(Paragraph(
        "All payments shall be made by bank transfer to Codecraft Technologies Ltd.'s designated "
        "account within 14 days of invoice receipt. Late payments shall accrue interest at 1.5% "
        "per month on the outstanding balance.",
        body_style,
    ))

    # Section 3 — IP
    story.append(Paragraph("3. INTELLECTUAL PROPERTY", section_style))
    story.append(Paragraph(
        "Upon receipt of full payment, all intellectual property rights in the Platform — including "
        "source code, documentation, and design assets — shall transfer exclusively to Meridian "
        "Ventures Pte. Ltd. Codecraft Technologies Ltd. retains the right to use anonymized "
        "technical concepts and general methodologies developed during the project for internal "
        "knowledge purposes, provided no client-specific data or proprietary business logic is disclosed.",
        body_style,
    ))

    # Page 2 content
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#dddddd")))
    story.append(Spacer(1, 10))

    # Section 4 — Confidentiality
    story.append(Paragraph("4. CONFIDENTIALITY AND DATA PROTECTION", section_style))
    story.append(Paragraph(
        "Both parties agree to maintain strict confidentiality regarding any proprietary information, "
        "trade secrets, or business data shared during the term of this Agreement. Codecraft "
        "Technologies Ltd. shall implement industry-standard security measures, including AES-256 "
        "encryption at rest and TLS 1.3 in transit, for all data handled on behalf of Meridian. "
        "Both parties shall comply with the Singapore Personal Data Protection Act 2012 (PDPA) "
        "and the UK General Data Protection Regulation (UK GDPR) as applicable.",
        body_style,
    ))

    # Section 5 — Warranties
    story.append(Paragraph("5. WARRANTIES AND LIABILITY", section_style))
    story.append(Paragraph(
        "Codecraft Technologies Ltd. warrants that the Platform will perform materially in accordance "
        "with the functional specifications in Schedule A for a period of <b>12 months</b> following "
        "the go-live date. In the event of a material defect, Codecraft shall remedy the defect within "
        "<b>5 business days</b> of written notification. The total liability of either party under "
        "this Agreement shall not exceed the total fees paid in the preceding 6 months, except in "
        "cases of willful misconduct or gross negligence.",
        body_style,
    ))

    # Section 6 — Termination
    story.append(Paragraph("6. TERMINATION", section_style))
    story.append(Paragraph(
        "Either party may terminate this Agreement with <b>30 days written notice</b> if the other "
        "party materially breaches any provision and fails to cure such breach within 15 days of "
        "receiving written notice. Upon termination, Meridian shall pay for all work completed "
        "and accepted up to the termination date on a pro-rata basis.",
        body_style,
    ))

    # Section 7 — Governing Law
    story.append(Paragraph("7. GOVERNING LAW", section_style))
    story.append(Paragraph(
        "This Agreement shall be governed by and construed in accordance with the laws of Singapore. "
        "Any disputes arising out of or in connection with this Agreement shall be referred to and "
        "finally resolved by arbitration administered by the Singapore International Arbitration "
        "Centre (SIAC) in accordance with its Arbitration Rules.",
        body_style,
    ))

    # Signatures
    story.append(Spacer(1, 20))
    story.append(Paragraph("SIGNATURES", section_style))
    story.append(Paragraph(
        "IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.",
        body_style,
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>For Meridian Ventures Pte. Ltd.:</b><br/>"
        "Ms. Rachel Tan Wei Ling, Chief Executive Officer<br/>"
        "Date: March 1, 2025",
        label_style,
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "<b>For Codecraft Technologies Ltd.:</b><br/>"
        "Mr. James Harrington, Managing Director<br/>"
        "Date: March 1, 2025",
        label_style,
    ))

    doc.build(story)
    print(f"Sample PDF created: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
