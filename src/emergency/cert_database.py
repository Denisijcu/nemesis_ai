#!/usr/bin/env python3
"""
Némesis IA - CERT Database
Capítulo 12: El Botón Rojo

Base de datos de CERTs y equipos de respuesta
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CERTContact:
    """Información de contacto de un CERT"""
    name: str
    organization: str
    email: str
    country: str
    website: str
    phone: Optional[str] = None
    emergency_email: Optional[str] = None
    pgp_key: Optional[str] = None
    jurisdiction: str = "NATIONAL"
    languages: List[str] = None
    
    def __post_init__(self):
        if self.languages is None:
            self.languages = ["EN"]


class CERTDatabase:
    """Base de datos de CERTs y equipos de respuesta"""
    
    def __init__(self):
        """Inicializa base de datos de CERTs"""
        
        self.certs = self._load_cert_contacts()
        
        logger.info(f"🚨 CERT Database inicializada - {len(self.certs)} CERTs")
    
    def _load_cert_contacts(self) -> Dict[str, CERTContact]:
        """Carga contactos de CERTs principales"""
        
        certs = {
            # Estados Unidos
            'US-CERT': CERTContact(
                name='US-CERT',
                organization='Cybersecurity and Infrastructure Security Agency',
                email='cert@cisa.dhs.gov',
                emergency_email='SOC@cisa.dhs.gov',
                country='US',
                website='https://www.cisa.gov/uscert',
                phone='+1-888-282-0870',
                jurisdiction='NATIONAL',
                languages=['EN']
            ),
            
            # Unión Europea
            'CERT-EU': CERTContact(
                name='CERT-EU',
                organization='Computer Emergency Response Team for EU Institutions',
                email='cert-eu@ec.europa.eu',
                emergency_email='cert-eu@ec.europa.eu',
                country='EU',
                website='https://cert.europa.eu',
                jurisdiction='REGIONAL',
                languages=['EN', 'FR', 'DE']
            ),
            
            # Reino Unido
            'NCSC-UK': CERTContact(
                name='NCSC-UK',
                organization='National Cyber Security Centre',
                email='report@ncsc.gov.uk',
                emergency_email='incident@ncsc.gov.uk',
                country='UK',
                website='https://www.ncsc.gov.uk',
                phone='+44-0345-070-0832',
                jurisdiction='NATIONAL',
                languages=['EN']
            ),
            
            # Alemania
            'CERT-Bund': CERTContact(
                name='CERT-Bund',
                organization='BSI Computer Emergency Response Team',
                email='certbund@bsi.bund.de',
                country='DE',
                website='https://www.bsi.bund.de/cert-bund',
                jurisdiction='NATIONAL',
                languages=['DE', 'EN']
            ),
            
            # Francia
            'CERT-FR': CERTContact(
                name='CERT-FR',
                organization='ANSSI CERT-FR',
                email='cert-fr.cossi@ssi.gouv.fr',
                country='FR',
                website='https://www.cert.ssi.gouv.fr',
                jurisdiction='NATIONAL',
                languages=['FR', 'EN']
            ),
            
            # España
            'INCIBE-CERT': CERTContact(
                name='INCIBE-CERT',
                organization='Instituto Nacional de Ciberseguridad',
                email='incidencias@incibe.es',
                country='ES',
                website='https://www.incibe.es/incibe-cert',
                phone='+34-900-116-117',
                jurisdiction='NATIONAL',
                languages=['ES', 'EN']
            ),
            
            # Canadá
            'CCCS': CERTContact(
                name='Canadian Centre for Cyber Security',
                organization='Communications Security Establishment',
                email='contact@cyber.gc.ca',
                country='CA',
                website='https://cyber.gc.ca',
                jurisdiction='NATIONAL',
                languages=['EN', 'FR']
            ),
            
            # Australia
            'ACSC': CERTContact(
                name='ACSC',
                organization='Australian Cyber Security Centre',
                email='asd.assist@defence.gov.au',
                country='AU',
                website='https://www.cyber.gov.au',
                phone='+61-1300-292-371',
                jurisdiction='NATIONAL',
                languages=['EN']
            ),
            
            # Japón
            'JPCERT': CERTContact(
                name='JPCERT/CC',
                organization='Japan Computer Emergency Response Team',
                email='info@jpcert.or.jp',
                emergency_email='ew-info@jpcert.or.jp',
                country='JP',
                website='https://www.jpcert.or.jp',
                jurisdiction='NATIONAL',
                languages=['JP', 'EN']
            ),
            
            # Internacional
            'FIRST': CERTContact(
                name='FIRST',
                organization='Forum of Incident Response and Security Teams',
                email='first-sec@first.org',
                country='INTL',
                website='https://www.first.org',
                jurisdiction='INTERNATIONAL',
                languages=['EN']
            )
        }
        
        return certs
    
    def get_cert(self, cert_id: str) -> Optional[CERTContact]:
        """
        Obtiene información de un CERT
        
        Args:
            cert_id: ID del CERT
            
        Returns:
            CERTContact o None
        """
        return self.certs.get(cert_id)
    
    def get_cert_by_country(self, country_code: str) -> List[CERTContact]:
        """
        Obtiene CERTs por país
        
        Args:
            country_code: Código de país (US, UK, etc)
            
        Returns:
            Lista de CERTs
        """
        return [
            cert for cert in self.certs.values()
            if cert.country == country_code
        ]
    
    def get_all_certs(self) -> List[CERTContact]:
        """Obtiene todos los CERTs"""
        return list(self.certs.values())
    
    def search_certs(self, query: str) -> List[CERTContact]:
        """
        Busca CERTs por nombre u organización
        
        Args:
            query: Término de búsqueda
            
        Returns:
            Lista de CERTs coincidentes
        """
        query_lower = query.lower()
        
        return [
            cert for cert in self.certs.values()
            if query_lower in cert.name.lower() or
               query_lower in cert.organization.lower() or
               query_lower in cert.country.lower()
        ]
    
    def get_recommended_certs(
        self,
        threat_level: str,
        source_country: Optional[str] = None
    ) -> List[CERTContact]:
        """
        Obtiene CERTs recomendados basados en amenaza
        
        Args:
            threat_level: CRITICAL, HIGH, MEDIUM, LOW
            source_country: País origen del ataque
            
        Returns:
            Lista de CERTs recomendados
        """
        recommended = []
        
        # Siempre incluir CERT local (US-CERT por defecto)
        recommended.append(self.certs['US-CERT'])
        
        # Si es crítico, incluir CERT-EU y FIRST
        if threat_level in ['CRITICAL', 'HIGH']:
            if 'CERT-EU' in self.certs:
                recommended.append(self.certs['CERT-EU'])
            if 'FIRST' in self.certs:
                recommended.append(self.certs['FIRST'])
        
        # Si conocemos país origen, incluir su CERT
        if source_country:
            country_certs = self.get_cert_by_country(source_country)
            recommended.extend(country_certs)
        
        # Eliminar duplicados
        seen = set()
        unique_recommended = []
        for cert in recommended:
            if cert.name not in seen:
                seen.add(cert.name)
                unique_recommended.append(cert)
        
        return unique_recommended