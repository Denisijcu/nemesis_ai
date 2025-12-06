#!/usr/bin/env python3
"""
Némesis IA - PDF Generator
Capítulo 10: El Fiscal Digital

Generador de documentos PDF para evidencia legal
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image as RLImage
)
from reportlab.lib import colors

logger = logging.getLogger(__name__)


class PDFGenerator:
    """Generador de PDFs para evidencia legal"""
    
    def __init__(self):
        """Inicializa el generador"""
        
        # Estilos
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        logger.info("📄 PDFGenerator inicializado")
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados"""
        
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Sección
        self.styles.add(ParagraphStyle(
            name='CustomSection',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#444444'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        ))
        
        # Body justificado
        self.styles.add(ParagraphStyle(
            name='JustifiedBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
        
        # Metadata
        self.styles.add(ParagraphStyle(
            name='Metadata',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            spaceAfter=6
        ))
    
    def create_document(
        self,
        filepath: str,
        title: str,
        pagesize=letter
    ) -> SimpleDocTemplate:
        """
        Crea documento PDF base
        
        Args:
            filepath: Ruta del archivo
            title: Título del documento
            pagesize: Tamaño de página
            
        Returns:
            SimpleDocTemplate
        """
        
        doc = SimpleDocTemplate(
            filepath,
            pagesize=pagesize,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
            title=title
        )
        
        return doc
    
    def add_header(
        self,
        title: str,
        subtitle: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> List:
        """
        Crea header del documento
        
        Args:
            title: Título principal
            subtitle: Subtítulo
            metadata: Metadatos del documento
            
        Returns:
            Lista de elementos Platypus
        """
        
        elements = []
        
        # Título
        elements.append(Paragraph(title, self.styles['CustomTitle']))
        elements.append(Spacer(1, 12))
        
        # Subtítulo
        if subtitle:
            elements.append(Paragraph(subtitle, self.styles['CustomSubtitle']))
            elements.append(Spacer(1, 12))
        
        # Metadata
        if metadata:
            metadata_text = "<br/>".join([
                f"<b>{key}:</b> {value}"
                for key, value in metadata.items()
            ])
            elements.append(Paragraph(metadata_text, self.styles['Metadata']))
            elements.append(Spacer(1, 20))
        
        # Línea separadora
        elements.append(Spacer(1, 12))
        
        return elements
    
    def add_section(
        self,
        title: str,
        content: str,
        style: str = 'JustifiedBody'
    ) -> List:
        """
        Añade sección al documento
        
        Args:
            title: Título de la sección
            content: Contenido
            style: Estilo del contenido
            
        Returns:
            Lista de elementos
        """
        
        elements = []
        
        # Título de sección
        elements.append(Paragraph(title, self.styles['CustomSection']))
        elements.append(Spacer(1, 6))
        
        # Contenido
        elements.append(Paragraph(content, self.styles[style]))
        elements.append(Spacer(1, 12))
        
        return elements
    
    def add_table(
        self,
        data: List[List],
        column_widths: Optional[List] = None,
        header_style: bool = True
    ) -> Table:
        """
        Crea tabla
        
        Args:
            data: Datos de la tabla
            column_widths: Anchos de columnas
            header_style: Si usar estilo de header
            
        Returns:
            Table objeto
        """
        
        table = Table(data, colWidths=column_widths)
        
        # Estilo base
        style_commands = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey if header_style else colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke if header_style else colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]
        
        table.setStyle(TableStyle(style_commands))
        
        return table
    
    def add_evidence_box(self, evidence_data: Dict) -> List:
        """
        Crea caja de evidencia destacada
        
        Args:
            evidence_data: Datos de la evidencia
            
        Returns:
            Lista de elementos
        """
        
        elements = []
        
        # Crear tabla para la caja de evidencia
        data = [
            ['EVIDENCE ITEM', ''],
            ['Evidence ID:', evidence_data.get('evidence_id', 'N/A')],
            ['Type:', evidence_data.get('type', 'N/A')],
            ['Collected:', evidence_data.get('collected_at', 'N/A')],
            ['Hash:', evidence_data.get('hash', 'N/A')[:32] + '...'],
            ['Classification:', evidence_data.get('classification', 'N/A')],
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a1a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('SPAN', (0, 0), (-1, 0)),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f0f0f0')),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(Spacer(1, 12))
        elements.append(table)
        elements.append(Spacer(1, 12))
        
        return elements
    
    def add_signature_section(
        self,
        signatures: List[Dict]
    ) -> List:
        """
        Añade sección de firmas
        
        Args:
            signatures: Lista de firmantes
            
        Returns:
            Lista de elementos
        """
        
        elements = []
        
        elements.append(Spacer(1, 30))
        elements.append(Paragraph("SIGNATURES", self.styles['CustomSection']))
        elements.append(Spacer(1, 20))
        
        for sig in signatures:
            sig_text = f"""
            <b>{sig['name']}</b><br/>
            {sig['title']}<br/>
            Date: {sig.get('date', datetime.now().strftime('%Y-%m-%d'))}<br/>
            Signature: _________________________
            """
            elements.append(Paragraph(sig_text, self.styles['Normal']))
            elements.append(Spacer(1, 20))
        
        return elements
    
    def add_footer_text(self, text: str) -> List:
        """Añade texto de pie de página"""
        
        elements = []
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(
            f"<i>{text}</i>",
            self.styles['Metadata']
        ))
        
        return elements
    
    def generate_legal_disclaimer(self) -> str:
        """Genera disclaimer legal"""
        
        return """
        This document contains legally privileged and confidential information.
        It is intended solely for the use of the individual or entity to whom it is addressed.
        If you are not the intended recipient, you are hereby notified that any disclosure,
        copying, distribution, or taking of any action in reliance on the contents of this
        information is strictly prohibited. This document has been generated automatically
        by NEMESIS IA Forensic System and maintains chain of custody integrity through
        cryptographic verification.
        """
    
    def build_pdf(
        self,
        filepath: str,
        elements: List,
        title: str = "Legal Document"
    ):
        """
        Construye el PDF final
        
        Args:
            filepath: Ruta del archivo
            elements: Lista de elementos Platypus
            title: Título del documento
        """
        
        logger.info(f"📄 Generando PDF: {filepath}")
        
        doc = self.create_document(filepath, title)
        doc.build(elements)
        
        logger.info(f"✅ PDF generado: {filepath}")