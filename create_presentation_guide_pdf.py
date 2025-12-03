"""
Portfolio Presentation Guide PDF Generator - Compact Version
Each project fits on ONE PAGE with proper text wrapping
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

def create_kpi_table(kpi_data, oxford_blue, light_blue):
    """Helper to create properly wrapped KPI tables"""
    # Wrap first row (headers)
    cell_style = ParagraphStyle('cell', fontSize=8, leading=10)
    wrapped_data = [[kpi_data[0][0], kpi_data[0][1], kpi_data[0][2], kpi_data[0][3]]]

    # Wrap data rows
    for row in kpi_data[1:]:
        wrapped_row = [
            Paragraph(row[0], cell_style),
            Paragraph(row[1], cell_style),
            Paragraph(row[2], cell_style),
            Paragraph(row[3], cell_style)
        ]
        wrapped_data.append(wrapped_row)

    table = Table(wrapped_data, colWidths=[1.1*inch, 0.9*inch, 1.2*inch, 3.1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), oxford_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_blue])
    ]))
    return table

def create_presentation_guide_pdf():
    filename = "Portfolio_Presentation_Guide.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           topMargin=0.5*inch, bottomMargin=0.5*inch,
                           leftMargin=0.7*inch, rightMargin=0.7*inch)

    elements = []
    styles = getSampleStyleSheet()

    # Oxford Blue color scheme
    oxford_blue = colors.HexColor('#002147')
    accent_blue = colors.HexColor('#4A90E2')
    light_blue = colors.HexColor('#E8F0F8')
    success_green = colors.HexColor('#27ae60')

    # Styles
    cover_title = ParagraphStyle('CoverTitle', parent=styles['Heading1'], fontSize=32,
                                 textColor=oxford_blue, spaceAfter=15, alignment=TA_CENTER,
                                 fontName='Helvetica-Bold')

    section_title = ParagraphStyle('SectionTitle', parent=styles['Heading1'], fontSize=18,
                                   textColor=oxford_blue, spaceAfter=10, fontName='Helvetica-Bold')

    project_title = ParagraphStyle('ProjectTitle', parent=styles['Heading2'], fontSize=13,
                                   textColor=accent_blue, spaceAfter=8, fontName='Helvetica-Bold')

    body_text = ParagraphStyle('BodyText', parent=styles['Normal'], fontSize=10,
                               leading=13, spaceAfter=6, alignment=TA_JUSTIFY)

    italic_text = ParagraphStyle('ItalicText', parent=body_text, fontName='Helvetica-Oblique',
                                 textColor=colors.HexColor('#333333'), leftIndent=15, rightIndent=15)

    # PAGE 1: COVER + PORTFOLIO OVERVIEW
    elements.append(Spacer(1, 0.8*inch))
    elements.append(Paragraph("Portfolio Presentation Guide", cover_title))
    elements.append(Paragraph("For Interview Success",
                             ParagraphStyle('Sub', parent=styles['Normal'], fontSize=16,
                                          alignment=TA_CENTER, textColor=accent_blue, spaceAfter=25)))

    elements.append(Paragraph("Salomón Santiago Esquivel",
                             ParagraphStyle('Name', parent=styles['Normal'], fontSize=14,
                                          alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=5)))
    elements.append(Paragraph("Data Analyst | 6+ Years Experience",
                             ParagraphStyle('Title', parent=styles['Normal'], fontSize=11,
                                          alignment=TA_CENTER, spaceAfter=35)))

    elements.append(Paragraph("🎯 Portfolio Overview", section_title))
    elements.append(Paragraph("When they ask: <b>\"Do you have any projects to show?\"</b>", body_text))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<i>\"Yes, I have a portfolio with four data analysis projects on my GitHub. Each one showcases different skills - from market intelligence and financial analytics to customer behavior analysis and investment modeling. They demonstrate my ability to work with APIs, SQL, Python, and visualization tools like Tableau. Would you like me to walk you through one of them?\"</i>", italic_text))

    elements.append(PageBreak())

    # PROJECT 1: MARKET INTELLIGENCE
    elements.append(Paragraph("📊 Project 1: Market Intelligence Dashboard", section_title))
    elements.append(Paragraph("30-Second Pitch", project_title))
    elements.append(Paragraph("<i>\"I built a market intelligence platform analyzing $1.3T in market cap across 15 major tech companies. I collected real-time financial data through APIs, designed a database, wrote SQL for competitive analysis and risk metrics, and created an executive Tableau dashboard showing end-to-end pipeline capability.\"</i>", italic_text))

    elements.append(Spacer(1, 0.12*inch))
    elements.append(Paragraph("KPI Talking Points", project_title))

    kpi1_data = [
        ['KPI', 'Value', 'Impact', 'What to Say'],
        ['Market Cap', '$1.3T', 'Comprehensive coverage', '"Analyzed 15 tech companies - $1.3T market cap covering major sector players."'],
        ['Collection Rate', '100%', '1,350 records/90 days', '"100% success rate over 90 days - reliability critical for accurate analysis."'],
        ['Companies', '15', 'Major tech leaders', '"15 tech leaders - enough diversity without overwhelming the analysis."'],
        ['Dashboard', 'Tableau Public', 'Executive visualization', '"Deployed on Tableau Public - professional, shareable visualizations."']
    ]
    elements.append(create_kpi_table(kpi1_data, oxford_blue, light_blue))

    elements.append(Spacer(1, 0.12*inch))
    elements.append(Paragraph("If Asked Technical Questions", project_title))
    qa1 = [
        [Paragraph('<b>Q: SQL techniques?</b>', ParagraphStyle('q', fontSize=8)),
         Paragraph('"Multi-table joins, CTEs, window functions for Value at Risk calculations."', ParagraphStyle('a', fontSize=8))],
        [Paragraph('<b>Q: Why SQLite?</b>', ParagraphStyle('q', fontSize=8)),
         Paragraph('"Lightweight, no server needed. For production I\'d use PostgreSQL."', ParagraphStyle('a', fontSize=8))],
        [Paragraph('<b>Q: Improvements?</b>', ParagraphStyle('q', fontSize=8)),
         Paragraph('"Real-time updates, news sentiment, predictive analytics, market alerts."', ParagraphStyle('a', fontSize=8))]
    ]
    qa1_table = Table(qa1, colWidths=[1.6*inch, 4.7*inch])
    qa1_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), light_blue)
    ]))
    elements.append(qa1_table)

    elements.append(PageBreak())

    # PROJECT 2: SALES PERFORMANCE
    elements.append(Paragraph("📊 Project 2: Sales Performance Analytics", section_title))
    elements.append(Paragraph("30-Second Pitch", project_title))
    elements.append(Paragraph("<i>\"I analyzed $589K in e-commerce revenue across 30 customers. Used SQL to identify revenue drivers, segment customers by demographics, rank products, and create documentation for team use. Found Furniture as top category and Millennials as primary demographic.\"</i>", italic_text))

    elements.append(Spacer(1, 0.12*inch))
    elements.append(Paragraph("KPI Talking Points", project_title))

    kpi2_data = [
        ['KPI', 'Value', 'Impact', 'What to Say'],
        ['Total Revenue', '$589K', 'Complete analysis', '"Analyzed $589K revenue - complete business performance picture."'],
        ['Avg Order', '$19.6K', 'High-value transactions', '"$19.6K average order - needed careful customer relationship management."'],
        ['Top Category', 'Furniture', 'Revenue driver', '"Furniture was top category - informed inventory and marketing strategy."'],
        ['Primary Demo', 'Millennials', 'Targeted marketing', '"Millennials (25-35) were primary demographic - enabled targeted campaigns."']
    ]
    elements.append(create_kpi_table(kpi2_data, oxford_blue, light_blue))

    elements.append(PageBreak())

    # PROJECT 3: CUSTOMER BEHAVIOR
    elements.append(Paragraph("📊 Project 3: Customer Behavior Analytics", section_title))
    elements.append(Paragraph("30-Second Pitch", project_title))
    elements.append(Paragraph("<i>\"Built customer analytics platform using Google Analytics 4 data. Did cohort analysis for retention tracking, engagement scoring for segmentation, and churn prediction model. Enables proactive customer retention and lifetime value maximization.\"</i>", italic_text))

    elements.append(Spacer(1, 0.12*inch))
    elements.append(Paragraph("KPI Talking Points", project_title))

    kpi3_data = [
        ['KPI', 'Value', 'Impact', 'What to Say'],
        ['Data Source', 'GA4', 'Enterprise platform', '"Used real GA4 BigQuery data - shows enterprise analytics platform experience."'],
        ['Cohort Analysis', 'Monthly', 'Retention tracking', '"Month-over-month cohorts - identified loyalty patterns over time."'],
        ['Engagement', 'Multi-tier', 'Customer classification', '"Weighted scoring - classified customers into High/Medium/Low engagement tiers."'],
        ['Churn Model', 'Risk scoring', 'Proactive intervention', '"Risk scores prioritize who needs intervention - prevents loss proactively."'],
        ['Attribution', 'Multi-touch', 'Marketing optimization', '"Mapped customer journey - shows what drives conversions, optimizes spend."']
    ]
    elements.append(create_kpi_table(kpi3_data, oxford_blue, light_blue))

    elements.append(PageBreak())

    # PROJECT 4: REAL ESTATE
    elements.append(Paragraph("📊 Project 4: Real Estate Investment Analysis", section_title))
    elements.append(Paragraph("30-Second Pitch", project_title))
    elements.append(Paragraph("<i>\"Built real estate investment system integrating 3 APIs - property valuations, economic indicators, market analytics. Calculate ROI metrics (cap rate, cash flow, ROI), perform geographic analysis, and use weighted scoring algorithm to rank investment opportunities systematically.\"</i>", italic_text))

    elements.append(Spacer(1, 0.12*inch))
    elements.append(Paragraph("KPI Talking Points", project_title))

    kpi4_data = [
        ['KPI', 'Value', 'Impact', 'What to Say'],
        ['API Integration', '3 sources', 'Complete data picture', '"Integrated RentCast, FRED, ATTOM - demonstrates multi-source handling."'],
        ['Financial Metrics', 'Cap/ROI/Flow', 'Real investor metrics', '"Calculate cap rate, cash flow, ROI - metrics investors actually use."'],
        ['SQL Levels', '5 complexity', 'Basic to advanced', '"Designed 5 SQL complexity levels - basic aggregations to complex CTEs."'],
        ['Scoring', 'Multi-factor', 'Objective ranking', '"Algorithm weighs 5+ factors - systematic, data-driven decisions."'],
        ['Geographic', 'Location-based', 'Market timing', '"Location analysis shows pricing trends and velocity - timing is key."']
    ]
    elements.append(create_kpi_table(kpi4_data, oxford_blue, light_blue))

    elements.append(PageBreak())

    # TIPS PAGE
    elements.append(Paragraph("🎯 Tips for Interview Success", section_title))

    tips_data = [
        ['DO ✓', 'DON\'T ✗'],
        ['Use "I" statements', 'Read word-for-word'],
        ['Tell stories: Problem → Solution → Impact', 'Jump into technical jargon first'],
        ['Show enthusiasm', 'Apologize or downplay work'],
        ['Connect to their role', 'Ramble - stick to 30s/2min'],
        ['Pause for questions', 'Forget to breathe']
    ]
    tips_table = Table(tips_data, colWidths=[3.15*inch, 3.15*inch])
    tips_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), success_green),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#e74c3c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    elements.append(tips_table)

    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("💡 Practice Strategy", project_title))
    practice = """1. Pick ONE project (Market Intelligence or Customer Behavior)
2. Practice 30-second pitch until smooth
3. Memorize key KPIs: $1.3T, $589K, 100%, GA4
4. Have project PDF ready but don't read from it
5. Remember: Show impact, not just implementation"""
    elements.append(Paragraph(practice, body_text))

    elements.append(Spacer(1, 0.15*inch))
    reminder = [[Paragraph('<b>Remember:</b> You\'re showing a hiring manager you can solve business problems with data. Focus on <b>impact</b>, not just technical details. <b>You got this! 🚀</b>',
                          ParagraphStyle('remind', fontSize=11, textColor=oxford_blue))]]
    reminder_table = Table(reminder, colWidths=[6.3*inch])
    reminder_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), light_blue),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BOX', (0, 0), (-1, -1), 2, oxford_blue)
    ]))
    elements.append(reminder_table)

    doc.build(elements)
    print(f"PDF created successfully: {filename}")
    return filename

if __name__ == "__main__":
    create_presentation_guide_pdf()
