"""
PDF Generator Service - Generate PDF Complaints
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
from typing import Dict, Any

from app.core.logging import logger


class PDFGeneratorService:
    """PDF generation service for complaints"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1  # Center
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12,
            spaceBefore=12
        ))
    
    def generate_complaint_pdf(self, complaint_data: Dict[str, Any]) -> BytesIO:
        """
        Generate PDF for complaint
        
        Args:
            complaint_data: Complaint information
            
        Returns:
            BytesIO object containing PDF
        """
        buffer = BytesIO()
        
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build content
            story = []
            
            # Title
            title = Paragraph("CYBERCRIME COMPLAINT DRAFT", self.styles['CustomTitle'])
            story.append(title)
            story.append(Spacer(1, 0.2*inch))
            
            # Metadata
            meta_data = [
                ["Complaint ID:", complaint_data.get("complaint_id", "N/A")],
                ["Generated On:", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")],
                ["Crime Type:", complaint_data.get("crime_type", "N/A")]
            ]
            
            meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
            meta_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#555555')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(meta_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Victim Details
            story.append(Paragraph("VICTIM DETAILS", self.styles['CustomHeading']))
            victim_info = complaint_data.get("victim_info", {})
            victim_text = f"""
            <b>Name:</b> {victim_info.get('name', 'N/A')}<br/>
            <b>Email:</b> {victim_info.get('email', 'N/A')}<br/>
            <b>Phone:</b> {victim_info.get('phone', 'N/A')}<br/>
            <b>Address:</b> {victim_info.get('address', 'N/A')}
            """
            story.append(Paragraph(victim_text, self.styles['BodyText']))
            story.append(Spacer(1, 0.2*inch))
            
            # Incident Description
            story.append(Paragraph("INCIDENT DESCRIPTION", self.styles['CustomHeading']))
            description = complaint_data.get("incident_description", "No description provided")
            story.append(Paragraph(description, self.styles['BodyText']))
            story.append(Spacer(1, 0.2*inch))
            
            # Instructions
            story.append(Paragraph("NEXT STEPS", self.styles['CustomHeading']))
            instructions = """
            1. Keep this document for your records<br/>
            2. Visit <b>https://cybercrime.gov.in</b><br/>
            3. Click "File a Complaint"<br/>
            4. Register/Login with mobile number<br/>
            5. Select appropriate crime category<br/>
            6. Copy incident description from this document<br/>
            7. Upload all evidence (screenshots, transaction IDs)<br/>
            8. Submit and save acknowledgment number<br/>
            <br/>
            <b>EMERGENCY:</b> For financial fraud, call <b>1930</b> immediately.
            """
            story.append(Paragraph(instructions, self.styles['BodyText']))
            
            # Build PDF
            doc.build(story)
            
            # Reset buffer position
            buffer.seek(0)
            
            logger.info(f"Generated PDF for complaint: {complaint_data.get('complaint_id')}")
            
            return buffer
            
        except Exception as e:
            logger.error(f"Error generating PDF: {e}", exc_info=True)
            raise


# Global instance
pdf_generator_service = PDFGeneratorService()
