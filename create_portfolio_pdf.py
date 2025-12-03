"""
Portfolio Project Overview PDF Generator
Creates a professional 5-page PDF for interview presentations
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

def create_portfolio_pdf():
    # Create PDF
    filename = "Portfolio_Project_Overview.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           topMargin=0.5*inch, bottomMargin=0.5*inch,
                           leftMargin=0.6*inch, rightMargin=0.6*inch)

    # Container for elements
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    # Oxford Blue color scheme
    oxford_blue = colors.HexColor('#002147')
    accent_blue = colors.HexColor('#4A90E2')
    light_blue = colors.HexColor('#E8F0F8')

    # Custom styles with larger fonts and better spacing
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=oxford_blue,
        spaceAfter=14,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Heading1'],
        fontSize=36,
        textColor=colors.white,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=oxford_blue,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )

    small_heading = ParagraphStyle(
        'SmallHeading',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=accent_blue,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        spaceAfter=8
    )

    # PAGE 1: COVER PAGE
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("Data Analyst Portfolio", cover_title))
    elements.append(Paragraph("Project Overview & Technical Showcase",
                             ParagraphStyle('CoverSub', parent=cover_title, fontSize=20, spaceAfter=30)))

    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("<b>Salomón Santiago Esquivel</b>",
                             ParagraphStyle('Name', parent=styles['Normal'], fontSize=18, alignment=TA_CENTER, spaceAfter=5)))
    elements.append(Paragraph("Service Offering Manager & Data Analyst",
                             ParagraphStyle('Title', parent=styles['Normal'], fontSize=14, alignment=TA_CENTER, spaceAfter=20)))

    elements.append(Paragraph("6+ Years Experience | Python, SQL, Tableau, Excel",
                             ParagraphStyle('Skills', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER, spaceAfter=30)))

    # Contact info
    contact_data = [
        ['Email:', 'salo.santiago96@gmail.com'],
        ['Phone:', '+52 551916 4142'],
        ['LinkedIn:', 'linkedin.com/in/salomon-santiago-493002a7'],
        ['Portfolio:', 'salo996.github.io/Data-analyst-portfolio']
    ]
    contact_table = Table(contact_data, colWidths=[1.2*inch, 4*inch])
    contact_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(contact_table)

    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("4 Featured Projects | End-to-End Data Analysis",
                             ParagraphStyle('Footer', parent=styles['Normal'], fontSize=11, alignment=TA_CENTER, spaceAfter=5)))
    elements.append(Paragraph("Business Intelligence | Financial Analytics | Customer Insights",
                             ParagraphStyle('Footer2', parent=styles['Normal'], fontSize=11, alignment=TA_CENTER)))

    elements.append(PageBreak())

    # PROJECT 1: MARKET INTELLIGENCE DASHBOARD
    elements.append(Paragraph("Project 1: Market Intelligence Dashboard", title_style))
    elements.append(Spacer(1, 0.15*inch))

    # KPIs Table
    kpi_data = [
        ['KPI', 'Value', 'Impact'],
        ['Market Cap Analyzed', '$1.3 Trillion', 'Comprehensive market coverage'],
        ['Data Collection Rate', '100%', '1,350 records across 90 days'],
        ['Companies Tracked', '15', 'Major technology sector leaders'],
        ['Dashboard Deployment', 'Tableau Public', 'Executive-level visualization']
    ]
    kpi_table = Table(kpi_data, colWidths=[2*inch, 1.8*inch, 2.5*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), oxford_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_blue]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
    ]))
    elements.append(kpi_table)
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("<b>Business Problem:</b> Need for comprehensive market intelligence platform to analyze technology sector performance, competitive positioning, and investment risk.", body_style))

    elements.append(Paragraph("<b>My Approach:</b>", small_heading))
    approach = """• Built Python API integration with Alpha Vantage for real-time financial data<br/>
    • Designed SQLite database schema for efficient data management<br/>
    • Created advanced SQL queries for competitive analysis and risk metrics (VaR)<br/>
    • Developed executive-level Tableau dashboard for strategic decision-making"""
    elements.append(Paragraph(approach, body_style))

    elements.append(Paragraph("<b>Technical Stack:</b> Python | SQL (SQLite) | Tableau Public | Alpha Vantage API | Git", body_style))

    elements.append(Paragraph("<b>Key Results:</b>", small_heading))
    results = """• End-to-end pipeline: API → Database → Analysis → Visualization<br/>
    • Advanced SQL: Multi-table joins, CTEs, window functions<br/>
    • Risk analytics: Value at Risk (VaR) calculations and portfolio metrics<br/>
    • Business storytelling through executive dashboard"""
    elements.append(Paragraph(results, body_style))

    elements.append(Paragraph("<b>Business Value:</b> Provides strategic insights for investment decisions, competitive positioning, and market timing. Demonstrates ability to transform raw financial data into actionable executive intelligence.", body_style))

    elements.append(PageBreak())

    # PROJECT 2: SALES PERFORMANCE ANALYTICS
    elements.append(Paragraph("Project 2: Sales Performance Analytics", title_style))
    elements.append(Spacer(1, 0.15*inch))

    # KPIs Table
    kpi_data = [
        ['KPI', 'Value', 'Impact'],
        ['Total Revenue Analyzed', '$589,089', 'Comprehensive revenue analysis'],
        ['Customers Analyzed', '30', 'Full customer segmentation'],
        ['Orders Processed', '30', 'Complete transaction analysis'],
        ['Avg Order Value', '$19,636', 'High-value transaction insights'],
        ['Top Category', 'Furniture', 'Highest revenue potential identified']
    ]
    kpi_table = Table(kpi_data, colWidths=[2*inch, 1.8*inch, 2.5*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), oxford_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_blue]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
    ]))
    elements.append(kpi_table)
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("<b>Business Problem:</b> E-commerce business needs to understand which categories drive revenue, how customer segments behave, which products perform best, and who the most valuable customers are.", body_style))

    elements.append(Paragraph("<b>My Approach:</b>", small_heading))
    approach = """• Collected product, customer, and transaction data from DummyJSON API<br/>
    • Analyzed revenue across product categories with performance ranking<br/>
    • Created demographic analysis (Gen Z, Millennials, Gen X, Boomers)<br/>
    • Built SQL queries with progressive complexity and comprehensive documentation"""
    elements.append(Paragraph(approach, body_style))

    elements.append(Paragraph("<b>Technical Stack:</b> SQL | Excel | Python | Tableau | DummyJSON API", body_style))

    elements.append(Paragraph("<b>Key Results:</b>", small_heading))
    results = """• Identified Furniture as highest revenue potential category<br/>
    • Millennials (25-35) identified as primary demographic segment<br/>
    • SQL expertise from basic aggregations to advanced window functions<br/>
    • Professional query documentation with business impact explanations<br/>
    • Built KPI dashboard: Revenue, Customers, Orders, AOV"""
    elements.append(Paragraph(results, body_style))

    elements.append(Paragraph("<b>Business Value:</b> Enables data-driven inventory decisions, targeted marketing by customer segment, and product portfolio optimization. Clear SQL documentation facilitates team collaboration.", body_style))

    elements.append(PageBreak())

    # PROJECT 3: CUSTOMER BEHAVIOR ANALYTICS
    elements.append(Paragraph("Project 3: Customer Behavior Analytics", title_style))
    elements.append(Spacer(1, 0.15*inch))

    # KPIs Table
    kpi_data = [
        ['KPI', 'Value', 'Impact'],
        ['Data Source', 'Google Analytics 4', 'Real-world enterprise platform'],
        ['Analysis Period', 'Nov 2020 - Jan 2021', '3-month behavioral tracking'],
        ['Cohort Analysis', 'Month-over-month', 'Retention pattern identification'],
        ['Segmentation Model', 'Multi-dimensional', 'Engagement + value tiers'],
        ['Churn Prediction', 'Risk scoring', 'Proactive intervention prioritization']
    ]
    kpi_table = Table(kpi_data, colWidths=[2*inch, 1.8*inch, 2.5*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), oxford_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_blue]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
    ]))
    elements.append(kpi_table)
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("<b>Business Problem:</b> Optimize customer retention, predict churn risk, maximize lifetime value, and understand customer journey patterns to reduce acquisition costs.", body_style))

    elements.append(Paragraph("<b>My Approach:</b>", small_heading))
    approach = """• Leveraged Google Analytics 4 BigQuery public dataset<br/>
    • Built cohort analysis for month-over-month retention tracking<br/>
    • Created engagement scoring with weighted activity metrics<br/>
    • Developed churn prediction based on engagement patterns<br/>
    • Mapped multi-touch attribution to optimize conversion paths"""
    elements.append(Paragraph(approach, body_style))

    elements.append(Paragraph("<b>Technical Stack:</b> Google Analytics 4 | BigQuery SQL | Python | Advanced SQL | Data Visualization", body_style))

    elements.append(Paragraph("<b>Key Results:</b>", small_heading))
    results = """• Cohort-based retention analysis with lifecycle progression<br/>
    • Multi-dimensional customer profiling with value tiers<br/>
    • Predictive churn scoring with intervention prioritization<br/>
    • Complex window functions, CTEs, and behavioral event analysis<br/>
    • Strategic recommendations for loyalty programs"""
    elements.append(Paragraph(results, body_style))

    elements.append(Paragraph("<b>Business Value:</b> Enables proactive churn prevention, personalized engagement, optimized marketing spend, and lifetime value maximization. Real-world GA4 data demonstrates enterprise platform expertise.", body_style))

    elements.append(PageBreak())

    # PROJECT 4: REAL ESTATE INVESTMENT ANALYSIS
    elements.append(Paragraph("Project 4: Real Estate Investment Analysis", title_style))
    elements.append(Spacer(1, 0.15*inch))

    # KPIs Table
    kpi_data = [
        ['KPI', 'Value', 'Impact'],
        ['Data Sources', '3 APIs', 'RentCast, FRED, ATTOM integration'],
        ['Financial Metrics', 'Cap Rate, Cash Flow, ROI', 'Comprehensive investment analysis'],
        ['SQL Complexity', '5 levels', 'Basic to advanced queries'],
        ['Investment Scoring', 'Multi-factor algorithm', '5+ weighted factors'],
        ['Geographic Analysis', 'Location-based', 'Market velocity & pricing trends']
    ]
    kpi_table = Table(kpi_data, colWidths=[2*inch, 1.8*inch, 2.5*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), oxford_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_blue]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
    ]))
    elements.append(kpi_table)
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("<b>Business Problem:</b> Real estate investors need systematic approach to evaluate properties, calculate ROI metrics, assess market conditions, and identify optimal investment opportunities.", body_style))

    elements.append(Paragraph("<b>My Approach:</b>", small_heading))
    approach = """• Integrated RentCast API (valuations), FRED API (economics), ATTOM Data (market)<br/>
    • Built comprehensive ROI calculators: Cap Rate, Cash Flow, Cash-on-Cash Return<br/>
    • Performed location-based pricing trends and market velocity analysis<br/>
    • Developed weighted investment scoring algorithm with 5+ factors<br/>
    • Designed SQL query suite from basic to advanced (5 complexity levels)"""
    elements.append(Paragraph(approach, body_style))

    elements.append(Paragraph("<b>Technical Stack:</b> Python | SQL (SQLite) | Multiple APIs | Financial Modeling | Geographic Analysis", body_style))

    elements.append(Paragraph("<b>Key Results:</b>", small_heading))
    results = """• Financial analytics: Cap rate, monthly cash flow, ROI projections<br/>
    • Multi-API integration with error handling and validation<br/>
    • Advanced SQL: Multi-CTE investment scoring with weighted factors<br/>
    • Market intelligence: Time series, seasonal patterns, velocity tracking<br/>
    • Systematic property evaluation framework"""
    elements.append(Paragraph(results, body_style))

    elements.append(Paragraph("<b>Business Value:</b> Provides data-driven investment decision framework, reduces risk through comprehensive analysis, optimizes portfolio allocation, and identifies high-ROI opportunities. Demonstrates financial modeling and multi-source integration.", body_style))

    # Build PDF
    doc.build(elements)
    print(f"PDF created successfully: {filename}")
    return filename

if __name__ == "__main__":
    create_portfolio_pdf()
