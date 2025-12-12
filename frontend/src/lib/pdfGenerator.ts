import jsPDF from 'jspdf'
import { format } from 'date-fns'

interface ComplaintData {
  complaint_id: string
  crime_type: string
  incident_date: string
  incident_description: string
  amount_lost?: number
  victim_name: string
  victim_email: string
  victim_phone: string
  victim_address: string
  draft_text?: string
  created_at: string
}

export async function downloadComplaintPDF(complaint: ComplaintData): Promise<void> {
  const doc = new jsPDF()
  const pageWidth = doc.internal.pageSize.getWidth()
  const margin = 20
  const lineHeight = 7
  let yPosition = 20

  // Header
  doc.setFontSize(20)
  doc.setFont('helvetica', 'bold')
  doc.text('Cybercrime Complaint', pageWidth / 2, yPosition, { align: 'center' })
  yPosition += 10

  doc.setFontSize(12)
  doc.setFont('helvetica', 'normal')
  doc.text(complaint.complaint_id, pageWidth / 2, yPosition, { align: 'center' })
  yPosition += 15

  // Divider
  doc.setDrawColor(200)
  doc.line(margin, yPosition, pageWidth - margin, yPosition)
  yPosition += 10

  // Crime Type
  doc.setFontSize(11)
  doc.setFont('helvetica', 'bold')
  doc.text('Crime Type:', margin, yPosition)
  doc.setFont('helvetica', 'normal')
  doc.text(complaint.crime_type.replace(/_/g, ' '), margin + 35, yPosition)
  yPosition += lineHeight

  // Incident Date
  doc.setFont('helvetica', 'bold')
  doc.text('Incident Date:', margin, yPosition)
  doc.setFont('helvetica', 'normal')
  doc.text(format(new Date(complaint.incident_date), 'MMMM dd, yyyy'), margin + 35, yPosition)
  yPosition += lineHeight

  // Amount Lost (if applicable)
  if (complaint.amount_lost) {
    doc.setFont('helvetica', 'bold')
    doc.text('Amount Lost:', margin, yPosition)
    doc.setFont('helvetica', 'normal')
    doc.setTextColor(255, 0, 0)
    doc.text(`₹${complaint.amount_lost.toLocaleString('en-IN')}`, margin + 35, yPosition)
    doc.setTextColor(0, 0, 0)
    yPosition += lineHeight
  }

  yPosition += 5

  // Victim Information Section
  doc.setFontSize(14)
  doc.setFont('helvetica', 'bold')
  doc.text('Victim Information', margin, yPosition)
  yPosition += 8

  doc.setFontSize(11)
  doc.setFont('helvetica', 'bold')
  doc.text('Name:', margin, yPosition)
  doc.setFont('helvetica', 'normal')
  doc.text(complaint.victim_name, margin + 25, yPosition)
  yPosition += lineHeight

  doc.setFont('helvetica', 'bold')
  doc.text('Email:', margin, yPosition)
  doc.setFont('helvetica', 'normal')
  doc.text(complaint.victim_email, margin + 25, yPosition)
  yPosition += lineHeight

  doc.setFont('helvetica', 'bold')
  doc.text('Phone:', margin, yPosition)
  doc.setFont('helvetica', 'normal')
  doc.text(complaint.victim_phone, margin + 25, yPosition)
  yPosition += lineHeight

  doc.setFont('helvetica', 'bold')
  doc.text('Address:', margin, yPosition)
  yPosition += lineHeight
  const addressLines = doc.splitTextToSize(complaint.victim_address, pageWidth - 2 * margin)
  doc.setFont('helvetica', 'normal')
  doc.text(addressLines, margin + 5, yPosition)
  yPosition += addressLines.length * lineHeight + 5

  // Incident Description Section
  doc.setFontSize(14)
  doc.setFont('helvetica', 'bold')
  doc.text('Incident Description', margin, yPosition)
  yPosition += 8

  doc.setFontSize(11)
  doc.setFont('helvetica', 'normal')
  const descriptionLines = doc.splitTextToSize(complaint.incident_description, pageWidth - 2 * margin)
  doc.text(descriptionLines, margin, yPosition)
  yPosition += descriptionLines.length * lineHeight + 10

  // Complaint Draft (if available)
  if (complaint.draft_text) {
    if (yPosition > 250) {
      doc.addPage()
      yPosition = 20
    }

    doc.setFontSize(14)
    doc.setFont('helvetica', 'bold')
    doc.text('Complaint Draft', margin, yPosition)
    yPosition += 8

    doc.setFontSize(10)
    doc.setFont('helvetica', 'normal')
    const draftLines = doc.splitTextToSize(complaint.draft_text, pageWidth - 2 * margin)
    
    for (let i = 0; i < draftLines.length; i++) {
      if (yPosition > 280) {
        doc.addPage()
        yPosition = 20
      }
      doc.text(draftLines[i], margin, yPosition)
      yPosition += 6
    }
  }

  // Footer
  if (yPosition > 270) {
    doc.addPage()
    yPosition = 20
  }

  yPosition = doc.internal.pageSize.getHeight() - 30
  doc.setDrawColor(200)
  doc.line(margin, yPosition, pageWidth - margin, yPosition)
  yPosition += 6

  doc.setFontSize(9)
  doc.setTextColor(100)
  doc.text(`Generated on: ${format(new Date(), 'MMMM dd, yyyy HH:mm')}`, margin, yPosition)
  doc.text('Cyber SOP Assistant', pageWidth - margin, yPosition, { align: 'right' })
  yPosition += 5

  doc.setFontSize(8)
  doc.text('⚠️ This is a system-generated document. Verify all information before submission.', pageWidth / 2, yPosition, { align: 'center' })

  // Save PDF
  const filename = `complaint_${complaint.complaint_id}_${format(new Date(), 'yyyyMMdd')}.pdf`
  doc.save(filename)
}
