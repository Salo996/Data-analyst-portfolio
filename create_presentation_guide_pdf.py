"""
Portfolio Presentation Guide PDF Generator
Creates a visual, easy-to-read interview preparation document
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

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

    # Custom styles
    cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Heading1'],
        fontSize=36,
        textColor=oxford_blue,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    section_title = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=oxford_blue,
        spaceAfter=12,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )

    project_title = ParagraphStyle(
        'ProjectTitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=accent_blue,
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    subsection_title = ParagraphStyle(
        'SubsectionTitle',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=success_green,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )

    body_text = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        spaceAfter=8,
        alignment=TA_JUSTIFY
    )

    italic_text = ParagraphStyle(
        'ItalicText',
        parent=body_text,
        fontName='Helvetica-Oblique',
        textColor=colors.HexColor('#333333'),
        leftIndent=20,
        rightIndent=20
    )

    tip_box = ParagraphStyle(
        'TipBox',
        parent=body_text,
        fontSize=9,
        textColor=colors.HexColor('#555555'),
        leftIndent=15
    )

    # COVER PAGE
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("Portfolio Presentation Guide", cover_title))
    elements.append(Paragraph("For Interview Success",
                             ParagraphStyle('Subtitle', parent=styles['Normal'],
                                          fontSize=18, alignment=TA_CENTER,
                                          textColor=accent_blue, spaceAfter=40)))

    elements.append(Paragraph("Salomón Santiago Esquivel",
                             ParagraphStyle('Name', parent=styles['Normal'],
                                          fontSize=16, alignment=TA_CENTER,
                                          fontName='Helvetica-Bold', spaceAfter=10)))
    elements.append(Paragraph("Data Analyst | 6+ Years Experience",
                             ParagraphStyle('Title', parent=styles['Normal'],
                                          fontSize=12, alignment=TA_CENTER, spaceAfter=60)))

    # Key sections overview
    overview_data = [
        ['What\'s Inside:', ''],
        ['✓', 'Portfolio Overview (30-second pitch)'],
        ['✓', '4 Projects with Natural Talking Points'],
        ['✓', '30-Second & 2-Minute Versions'],
        ['✓', 'Conversational KPI Explanations'],
        ['✓', 'Technical Q&A Preparation'],
        ['✓', 'Tips for Sounding Natural'],
        ['✓', 'Practice Strategy']
    ]
    overview_table = Table(overview_data, colWidths=[0.4*inch, 5.5*inch])
    overview_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('TEXTCOLOR', (0, 0), (-1, 0), oxford_blue),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('TEXTCOLOR', (0, 1), (0, -1), success_green),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('SPAN', (0, 0), (-1, 0))
    ]))
    elements.append(overview_table)

    elements.append(PageBreak())

    # PORTFOLIO OVERVIEW
    elements.append(Paragraph("🎯 Portfolio Overview", section_title))
    elements.append(Paragraph("When they ask: <b>\"Do you have any projects to show?\"</b>", body_text))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<i>\"Yes, I have a portfolio with four data analysis projects on my GitHub. Each one showcases different skills - from market intelligence and financial analytics to customer behavior analysis and investment modeling. They demonstrate my ability to work with APIs, SQL, Python, and visualization tools like Tableau. Would you like me to walk you through one of them?\"</i>",
                             italic_text))

    elements.append(Spacer(1, 0.2*inch))

    # PROJECT 1
    elements.append(Paragraph("📊 Project 1: Market Intelligence Dashboard", section_title))

    elements.append(Paragraph("30-Second Pitch", project_title))
    elements.append(Paragraph("<i>\"I built a market intelligence platform that analyzes over $1.3 trillion in market cap across 15 major tech companies. I collected real-time financial data through APIs, stored it in a database, wrote SQL queries for competitive analysis and risk metrics, and created an executive dashboard in Tableau. It demonstrates my ability to build end-to-end data pipelines from collection to visualization.\"</i>",
                             italic_text))

    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("2-Minute Storytelling Version", project_title))

    elements.append(Paragraph("<b>Start with the problem:</b>", subsection_title))
    elements.append(Paragraph("<i>\"The goal was to create a comprehensive market intelligence platform for analyzing the technology sector. Investors needed insights into competitive positioning, market trends, and investment risk across major companies.\"</i>",
                             italic_text))

    elements.append(Paragraph("<b>Your approach:</b>", subsection_title))
    elements.append(Paragraph("<i>\"I started by integrating with the Alpha Vantage API using Python to collect real-time financial data. I pulled stock prices and fundamentals for 15 companies over 90 days - that's about 1,350 data points. I achieved a 100% success rate, which was important because missing data would skew the analysis.\"</i>",
                             italic_text))
    elements.append(Paragraph("<i>\"Then I designed a SQLite database to store everything efficiently. The interesting part was writing the SQL queries - I did competitive analysis comparing companies, calculated Value at Risk for portfolio metrics, and created business intelligence queries for strategic insights.\"</i>",
                             italic_text))
    elements.append(Paragraph("<i>\"Finally, I built the visualization in Tableau Public. The dashboard shows market positioning, performance trends, and risk metrics in a way that executives could quickly understand and act on.\"</i>",
                             italic_text))

    elements.append(Paragraph("<b>The impact:</b>", subsection_title))
    elements.append(Paragraph("<i>\"This project shows I can handle the full data pipeline - API integration, database design, advanced SQL analytics, and executive-level storytelling through visualization. It's the kind of end-to-end work I'd be doing in this role.\"</i>",
                             italic_text))

    elements.append(PageBreak())

    # KPI Talking Points - Project 1
    elements.append(Paragraph("KPI Talking Points (Conversational)", project_title))

    kpi_data = [
        ['$1.3 Trillion', '"I analyzed 15 major tech companies representing over a trillion dollars in market capitalization - so this covered the major players in the sector comprehensively."'],
        ['100% Success', '"I achieved 100% success collecting 1,350 records over 90 days. That reliability was critical because gaps in financial data can lead to wrong conclusions."'],
        ['15 Companies', '"I focused on 15 major technology sector leaders - companies like the big tech giants. This gave us enough diversity to see competitive patterns."'],
        ['Tableau Public', '"I deployed the dashboard on Tableau Public, which made it accessible and showed I can create professional, shareable visualizations."']
    ]
    kpi_table = Table(kpi_data, colWidths=[1.3*inch, 5*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), light_blue),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TEXTCOLOR', (0, 0), (0, -1), oxford_blue)
    ]))
    elements.append(kpi_table)

    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("If They Ask Technical Questions", project_title))

    tech_qa = [
        ['Q: What SQL techniques?', 'A: "Multi-table joins, CTEs, window functions. For example, I calculated Value at Risk using rolling calculations and percentile functions."'],
        ['Q: Why SQLite?', 'A: "Perfect for this project - lightweight, no server needed. In production, I\'d consider PostgreSQL."'],
        ['Q: How to improve?', 'A: "Add real-time updating, incorporate news sentiment, add predictive analytics, build alerts for market movements."']
    ]
    qa_table = Table(tech_qa, colWidths=[2*inch, 4.3*inch])
    qa_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), light_blue),
        ('TEXTCOLOR', (0, 0), (0, -1), oxford_blue)
    ]))
    elements.append(qa_table)

    elements.append(PageBreak())

    # PROJECT 2
    elements.append(Paragraph("📊 Project 2: Sales Performance Analytics", section_title))

    elements.append(Paragraph("30-Second Pitch", project_title))
    elements.append(Paragraph("<i>\"I analyzed sales performance for an e-commerce business - about $589,000 in revenue across 30 customers. I collected data from an API, used SQL to analyze which categories drove revenue, segmented customers by demographics, and identified top-performing products. I also created comprehensive SQL documentation that other analysts could use.\"</i>",
                             italic_text))

    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("Key KPIs to Mention", project_title))

    kpi_sales = [
        ['$589,089', 'Total revenue analyzed for complete business picture'],
        ['$19,636 AOV', 'High-value transactions requiring careful customer management'],
        ['Furniture', 'Highest revenue category - informed inventory strategy'],
        ['Millennials', 'Primary demographic (25-35) - targeted marketing focus']
    ]
    kpi_sales_table = Table(kpi_sales, colWidths=[1.3*inch, 5*inch])
    kpi_sales_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), light_blue),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TEXTCOLOR', (0, 0), (0, -1), oxford_blue)
    ]))
    elements.append(kpi_sales_table)

    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("Story to Tell", project_title))
    elements.append(Paragraph("<i>\"This e-commerce business needed answers: Which categories drive revenue? How do customer segments behave? I used SQL progressively - from basic aggregations to window functions for ranking. I found Furniture was top revenue, Millennials were the primary demographic, and the $19K average order value told us we needed careful relationship management. The documentation I created meant other analysts could understand and build on my work.\"</i>",
                             italic_text))

    elements.append(PageBreak())

    # PROJECT 3
    elements.append(Paragraph("📊 Project 3: Customer Behavior Analytics", section_title))

    elements.append(Paragraph("30-Second Pitch", project_title))
    elements.append(Paragraph("<i>\"I built a customer behavior analytics platform using Google Analytics 4 data. I did cohort analysis to track retention month-over-month, created customer segmentation based on engagement scoring, and built a churn prediction model. This helps businesses proactively prevent customer loss and maximize lifetime value.\"</i>",
                             italic_text))

    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("Key Points to Emphasize", project_title))

    key_points = [
        ['Google Analytics 4', 'Real enterprise platform experience with BigQuery'],
        ['Cohort Analysis', 'Month-over-month retention tracking - identifies loyalty patterns'],
        ['Engagement Scoring', 'Weighted activity metrics to classify customer tiers'],
        ['Churn Prediction', 'Risk scoring for proactive intervention - prevents loss'],
        ['Multi-touch Attribution', 'Optimizes marketing spend by showing what drives conversions']
    ]
    key_table = Table(key_points, colWidths=[1.5*inch, 4.8*inch])
    key_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), light_blue),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TEXTCOLOR', (0, 0), (0, -1), oxford_blue)
    ]))
    elements.append(key_table)

    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("The Impact Story", project_title))
    elements.append(Paragraph("<i>\"This platform enables proactive churn prevention instead of reactive damage control. It personalizes customer engagement based on behavior tiers and optimizes marketing spend by showing what actually drives conversions. Using real GA4 data demonstrates I can work with enterprise analytics platforms - exactly what most companies use.\"</i>",
                             italic_text))

    elements.append(PageBreak())

    # PROJECT 4
    elements.append(Paragraph("📊 Project 4: Real Estate Investment Analysis", section_title))

    elements.append(Paragraph("30-Second Pitch", project_title))
    elements.append(Paragraph("<i>\"I built a real estate investment analysis system that integrates data from three different APIs - property valuations, economic indicators, and market analytics. I calculate ROI metrics like cap rate and cash-on-cash return, perform geographic analysis for market trends, and have a weighted scoring algorithm to rank investment opportunities.\"</i>",
                             italic_text))

    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("What Makes This Impressive", project_title))

    impressive = [
        ['3 API Integration', 'RentCast + FRED + ATTOM - demonstrates multi-source data handling'],
        ['Financial Modeling', 'Cap Rate, Cash Flow, ROI - real metrics investors use'],
        ['SQL Progression', '5 complexity levels - shows range from basic to advanced'],
        ['Investment Scoring', 'Multi-factor algorithm weighing 5+ factors objectively'],
        ['Geographic Analysis', 'Location trends + market velocity - timing is everything']
    ]
    impressive_table = Table(impressive, colWidths=[1.5*inch, 4.8*inch])
    impressive_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), light_blue),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TEXTCOLOR', (0, 0), (0, -1), oxford_blue)
    ]))
    elements.append(impressive_table)

    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("Story Flow", project_title))
    elements.append(Paragraph("<i>\"Real estate investors can't rely on gut feelings when investing hundreds of thousands. I integrated three data sources for a complete picture, built financial models with the metrics investors actually use, added geographic analysis to catch market trends, and created a systematic scoring algorithm. It's having a framework instead of guessing - reduces risk through comprehensive, data-driven analysis.\"</i>",
                             italic_text))

    elements.append(PageBreak())

    # TIPS FOR SUCCESS
    elements.append(Paragraph("🎯 Tips for Sounding Natural", section_title))

    do_dont_data = [
        ['DO ✓', 'DON\'T ✗'],
        ['Use "I" statements: "I built..." "I analyzed..."', 'Read word-for-word from the PDF'],
        ['Tell stories: Problem → Approach → Impact', 'Jump into technical jargon unless asked'],
        ['Use analogies: "Like GPS for investments"', 'Apologize or downplay: "It\'s just small..."'],
        ['Show enthusiasm: "The interesting part was..."', 'Ramble - stick to 30s or 2min versions'],
        ['Connect to role: "Similar to what I\'d do here"', 'Forget to breathe and pause for questions']
    ]
    do_dont_table = Table(do_dont_data, colWidths=[3.15*inch, 3.15*inch])
    do_dont_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), success_green),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#e74c3c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    elements.append(do_dont_table)

    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("💡 Handling Common Situations", project_title))

    situations = [
        ['If they seem bored:', '"I can share more details if you\'d like, or we can move on to your questions."'],
        ['If they want technical depth:', '"Happy to dive deeper into the SQL techniques or walk through specific queries."'],
        ['Most proud of?:', '"Market Intelligence - shows full pipeline. Customer Behavior - solves real business problems."'],
        ['We use Power BI:', '"The tool is just the medium - what matters is telling the data story effectively. I can work with any BI tool."']
    ]
    situations_table = Table(situations, colWidths=[1.8*inch, 4.5*inch])
    situations_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), light_blue),
        ('TEXTCOLOR', (0, 0), (0, -1), oxford_blue)
    ]))
    elements.append(situations_table)

    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("🎤 Practice Strategy", project_title))

    practice_steps = [
        '1. Pick ONE project (Market Intelligence or Customer Behavior recommended)',
        '2. Practice the 30-second pitch until smooth without looking',
        '3. Practice the 2-minute version - focus on flow, not memorization',
        '4. Memorize key KPIs: $1.3T, $589K, 100%, etc.',
        '5. Have the project PDF ready as backup but don\'t read from it'
    ]
    for step in practice_steps:
        elements.append(Paragraph(step, tip_box))

    elements.append(Spacer(1, 0.2*inch))

    # Final reminder box
    reminder_data = [[
        '<b>Remember:</b> You\'re not presenting a school project. You\'re showing a hiring manager that you can solve their business problems with data. Focus on <b>impact</b>, not implementation details (unless they ask).<br/><br/><b>You got this! 🚀</b>'
    ]]
    reminder_table = Table(reminder_data, colWidths=[6.3*inch])
    reminder_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), light_blue),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (-1, -1), oxford_blue),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('BOX', (0, 0), (-1, -1), 2, oxford_blue)
    ]))
    elements.append(reminder_table)

    # Build PDF
    doc.build(elements)
    print(f"PDF created successfully: {filename}")
    return filename

if __name__ == "__main__":
    create_presentation_guide_pdf()
