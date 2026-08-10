#!/usr/bin/env python3
"""Genera la versión inglesa a partir del HTML español ya renderizado."""

from __future__ import annotations

import argparse
import html
import os
import re
import tempfile
from pathlib import Path


TRANSLATIONS = {
    "Pablo Ibáñez-Porras — Investigador predoctoral en CISA-INIA-CSIC": "Pablo Ibáñez-Porras — Predoctoral Researcher at CISA-INIA-CSIC",
    "CV de Pablo Ibáñez-Porras: Investigador predoctoral en CISA-INIA-CSIC. Enfoque aplicado de la física y las matemáticas al sector agrotecnológico mediante modelización matemática y aplicación de algoritmos GIS.": "Pablo Ibáñez-Porras's CV: Predoctoral Researcher at CISA-INIA-CSIC. Applying physics and mathematics to agrotechnology through mathematical modelling and GIS algorithms.",
    "Menú": "Menu",
    "Sobre mí": "About me",
    "Trayectoria": "Career",
    "Publicaciones": "Publications",
    "Actividad académica": "Academic activity",
    "Actividad Académica": "Academic Activity",
    "Docencia": "Teaching",
    "Herramientas": "Tools",
    "Divulgación": "Science outreach",
    "Contacto": "Contact",
    "Investigador predoctoral en CISA-INIA-CSIC": "Predoctoral Researcher at CISA-INIA-CSIC",
    "Enfoque aplicado de la física y las matemáticas al sector agrotecnológico mediante modelización matemática y aplicación de algoritmos GIS.": "Applying physics and mathematics to agrotechnology through mathematical modelling and GIS algorithms.",
    "Enlaces de contacto y perfiles": "Contact links and profiles",
    "Descargar CV en PDF": "Download CV as PDF",
    "Investigador predoctoral en el Centro de Investigación en Sanidad Animal (CISA-INIA-CSIC), especializado en epidemiología espacial y sistemas de vigilancia en tiempo real para enfermedades emergentes bajo el enfoque One Health. Combino mi formación en Física y Modelización Matemática con herramientas SIG, ciencia de datos y aprendizaje automático para el desarrollo de sistemas de alerta temprana frente a la influenza aviar y otras enfermedades transfronterizas, con proyectos como DiFLUsion, ProtectIA y SMARTe.": "Predoctoral researcher at the Animal Health Research Centre (CISA-INIA-CSIC), specialising in spatial epidemiology and real-time surveillance systems for emerging diseases under a One Health approach. I combine my background in Physics and Mathematical Modelling with GIS, data science and machine learning to develop early-warning systems for avian influenza and other transboundary diseases, including DiFLUsion, ProtectIA and SMARTe.",
    "Años de trayectoria": "Years of experience",
    "Foros científicos": "Scientific events",
    "Horas acreditadas": "Accredited training hours",
    "Física · Modelización · Epidemiología espacial": "Physics · Mathematical Modelling · Spatial Epidemiology",
    "Formación y Experiencia": "Education and Experience",
    "Doctorado en Ingeniería Informática (en curso)": "PhD in Computer Engineering (ongoing)",
    "Universidad de Salamanca": "University of Salamanca",
    "Programa codirigido por": "Programme jointly supervised by",
    "(Centro de Investigación en Sanidad Animal, CISA-INIA-CSIC) y": "(Animal Health Research Centre, CISA-INIA-CSIC) and",
    "(Instituto Universitario de Física Fundamental y Matemáticas, IUFFYM-USAL).": "(University Institute of Fundamental Physics and Mathematics, IUFFYM-USAL).",
    "Desarrollo y aplicación de un modelo integral de evaluación del riesgo epidemiológico mediante modelización matemática y computacional, orientado al análisis de los factores asociados a la introducción y difusión de la IAAP en aves silvestres y a la estimación del riesgo de transmisión a explotaciones ganaderas.": "Development and application of an integrated epidemiological risk-assessment model using mathematical and computational modelling to analyse the factors associated with the introduction and spread of HPAI in wild birds and estimate transmission risk to livestock holdings.",
    "Desarrollo de un modelo de difusión intrapeninsular de IAAP en aves silvestres e identificación de conexiones epidemiológicas entre casos mediante análisis filogenético.": "Development of a model for the spread of HPAI among wild birds within the Iberian Peninsula and identification of epidemiological links between cases through phylogenetic analysis.",
    "Centro de Investigación en Sanidad Animal (CISA-INIA-CSIC)": "Animal Health Research Centre (CISA-INIA-CSIC)",
    "Contrato financiado por Encomienda de Gestión del Ministerio de Agricultura, Pesca y Alimentación (2025-2027)": "Position funded through a management agreement with the Spanish Ministry of Agriculture, Fisheries and Food (2025–2027)",
    "Creación de modelos, visores y aplicaciones para la evaluación rápida de riesgos frente a la aparición de patógenos": "Development of models, viewers and applications for rapid risk assessment of emerging pathogens",
    "Contrato financiado por European Partnership on Animal Health and Welfare (2024-2027)": "Position funded by the European Partnership on Animal Health and Welfare (2024–2027)",
    "Modelo de cálculo de coste-beneficio de la vacunación temprana en jabalí silvestre ante la aparición de brotes de Peste Porcina Africana (PPA)": "Cost-benefit model of early wild-boar vaccination following African swine fever (ASF) outbreaks",
    "Contrato financiado por Proyecto VACDIVA (2023-2024)": "Position funded by the VACDIVA project (2023–2024)",
    "Mejora del sistema de alertas DiFLUsion de introducción de Influenza Aviar por aves silvestres en España y desarrollo de la herramienta ProtectIA de análisis de riesgo de introducción de la enfermedad en explotaciones avícolas": "Enhancement of the DiFLUsion warning system for avian-influenza introduction by wild birds in Spain and development of ProtectIA to assess introduction risk in poultry holdings",
    "Contrato financiado por Encomienda de Gestión del Ministerio de Agricultura, Pesca y Alimentación (2022-2023)": "Position funded through a management agreement with the Spanish Ministry of Agriculture, Fisheries and Food (2022–2023)",
    "Contratado": "Research appointment",
    "Máster Universitario en Modelización Matemática": "Master's Degree in Mathematical Modelling",
    "TFM: \"Modelo de propagación de epidemias entre comunidades definidas sobre redes complejas considerando flujo poblacional\". ·": "MSc thesis: ‘Epidemic-spread model between communities defined on complex networks considering population flow’. ·",
    "Ver trabajo": "View project",
    "Formación académica": "Academic education",
    "Modelización de la interacción de haces de protones con distintos objetivos basada en el método Montecarlo": "Monte Carlo modelling of proton-beam interactions with different targets",
    "Centro de Láseres Pulsados Ultracortos y Ultraintensos (CLPU)": "Centre for Pulsed, Ultrashort and Ultraintense Lasers (CLPU)",
    "Prácticas de grado": "Undergraduate internship",
    "Grado en Física": "BSc in Physics",
    "TFG: \"Redes complejas: Descripción, análisis y aplicaciones\". ·": "BSc thesis: ‘Complex networks: description, analysis and applications’. ·",
    "Formación continua por especialidad": "Continuing education by specialism",
    "GIS y teledetección": "GIS and remote sensing",
    "ArcGIS Pro y Online, QGIS, Google Earth Engine, teledetección y desarrollo de aplicaciones geoespaciales.": "ArcGIS Pro and Online, QGIS, Google Earth Engine, remote sensing and geospatial application development.",
    "IA, datos y programación": "AI, data and programming",
    "Aprendizaje automático y deep learning aplicados a investigación, Python, Docker, análisis estadístico y flujos reproducibles.": "Machine learning and deep learning for research, Python, Docker, statistical analysis and reproducible workflows.",
    "Matemáticas y modelización": "Mathematics and modelling",
    "Métodos numéricos, ecuaciones diferenciales y simulación científica aplicada.": "Numerical methods, differential equations and applied scientific simulation.",
    "One Health y agrotecnología": "One Health and agrotechnology",
    "Análisis de riesgo sanitario, enfermedades transfronterizas, patología veterinaria y digitalización del sector agropecuario.": "Health-risk analysis, transboundary diseases, veterinary pathology and digitalisation of the agricultural sector.",
    "Investigación y competencias": "Research and professional skills",
    "Comunicación científica, revisión bibliográfica, investigación cualitativa, idiomas y competencias profesionales.": "Scientific communication, literature review, qualitative research, languages and professional skills.",
    "Simulación espacial de estrategias de vacunación del jabalí frente a la peste porcina africana. Los escenarios se traducen en restricciones comerciales y pérdidas potencialmente evitadas para los productores porcinos.": "Spatial simulation of wild-boar vaccination strategies against African swine fever. The scenarios are translated into trade restrictions and potentially avoidable losses for pig producers.",
    "Sistema de alerta espacio-temporal que integra brotes, condiciones ambientales y movimientos de aves silvestres para anticipar semanalmente el riesgo de introducción de IAAP.": "A spatio-temporal warning system integrating outbreaks, environmental conditions and wild-bird movements to provide weekly forecasts of HPAI introduction risk.",
    "Otras publicaciones y contribuciones como coautor": "Other publications and co-authored contributions",
    "Otras publicaciones científicas y contribuciones como coautor": "Other scientific publications and co-authored contributions",
    "Artículos técnico-profesionales y de transferencia": "Technical and knowledge-transfer articles",
    "Influenza Aviar: cambios en la dinámica de la enfermedad y cómo anticiparnos a ella mediante sistemas de vigilancia a tiempo real": "Avian influenza: changing disease dynamics and how real-time surveillance systems can help us anticipate them",
    "encuentros científicos": "scientific events",
    "como autor principal o ponente": "as lead author or speaker",
    "comunicaciones orales": "oral presentations",
    "pósteres": "posters",
    "aportaciones como coautor": "co-authored contributions",
    "Vigilancia de influenza aviar": "Avian-influenza surveillance",
    "Resistencia antimicrobiana ambiental": "Environmental antimicrobial resistance",
    "Peste porcina africana": "African swine fever",
    "One Health e interoperabilidad": "One Health and interoperability",
    "Epidemiología espacial y SIG": "Spatial epidemiology and GIS",
    "Fauna silvestre y salud ambiental": "Wildlife and environmental health",
    "Contribuciones destacadas como autor principal": "Highlighted international contributions as lead author",
    "Aplicación de la herramienta WiBISS al norte de Italia para explorar cómo distintas estrategias de vacunación del jabalí podrían contribuir al control de la peste porcina africana y a reducir sus consecuencias económicas.": "Application of WiBISS in northern Italy to explore how different wild-boar vaccination strategies could help control African swine fever and reduce its economic consequences.",
    "Aplicación de la herramienta DiFLUsion en España para evaluar el riesgo de introducción de IAAP asociado a los movimientos migratorios de aves.": "Application of DiFLUsion in Spain to assess the risk of HPAI introduction associated with migratory bird movements.",
    "Marco espacial que integra fuentes antropogénicas, contexto territorial y puntos de muestreo para estandarizar la vigilancia ambiental de la resistencia antimicrobiana y facilitar comparaciones reproducibles entre territorios.": "A spatial framework integrating anthropogenic sources, territorial context and sampling points to standardise environmental antimicrobial-resistance surveillance and enable reproducible comparisons across regions.",
    "DiFLUsion evoluciona hacia un sistema operativo de alerta temprana codesarrollado con responsables de vigilancia que conecta modelización espacio-temporal, necesidades de usuario y política sanitaria.": "DiFLUsion is evolving into an operational early-warning system co-developed with surveillance authorities that connects spatio-temporal modelling, user needs and health policy.",
    "Visor de evaluación rápida que interpreta la velocidad y dirección del frente epidémico de peste porcina africana para priorizar territorialmente la vigilancia y las medidas de control.": "A rapid-assessment viewer that interprets the speed and direction of the African swine fever epidemic front to prioritise surveillance and control measures geographically.",
    "Simulación espacial de estrategias de vacunación del jabalí frente a la peste porcina africana que traduce los escenarios en restricciones comerciales y pérdidas potencialmente evitadas para los productores porcinos.": "A spatial simulation of wild-boar vaccination strategies against African swine fever that translates scenarios into trade restrictions and potentially avoidable losses for pig producers.",
    "Herramienta web que centraliza observaciones georreferenciadas para registrar, visualizar y explorar varamientos de mamíferos marinos con fines de investigación y vigilancia.": "A web tool that centralises georeferenced observations to record, visualise and explore marine-mammal strandings for research and surveillance.",
    "Marco espacial para estandarizar la vigilancia ambiental de la resistencia antimicrobiana. Integra fuentes antropogénicas, contexto territorial y puntos de muestreo para facilitar comparaciones reproducibles entre territorios.": "A spatial framework for standardising environmental antimicrobial-resistance surveillance. It integrates anthropogenic sources, territorial context and sampling points to enable reproducible comparisons across regions.",
    "Evolución de DiFLUsion hacia un sistema operativo de alerta temprana desarrollado con los responsables de vigilancia. La contribución conecta modelización espacio-temporal, necesidades de usuario y transferencia a política sanitaria.": "Evolution of DiFLUsion into an operational early-warning system co-developed with surveillance authorities. The contribution connects spatio-temporal modelling, user needs and translation into health policy.",
    "Visor de evaluación rápida que interpreta la velocidad y dirección del frente epidémico de peste porcina africana. Facilita la priorización territorial de la vigilancia y de las medidas de control.": "A rapid-assessment viewer that interprets the speed and direction of the African swine fever epidemic front. It supports territorial prioritisation of surveillance and control measures.",
    "Herramienta web para registrar y visualizar varamientos de mamíferos marinos. Centraliza observaciones georreferenciadas y facilita su exploración para investigación y vigilancia.": "A web tool for recording and visualising marine-mammal strandings. It centralises georeferenced observations and supports their exploration for research and surveillance.",
    "Otras contribuciones como autor principal": "Other lead-author contributions",
    "Mapeo de las fuentes de emisión antropogénicas de AMR": "Mapping anthropogenic sources of antimicrobial-resistance emissions",
    "ProtectIA: Herramienta geoespacial para la prevención de la influenza aviar": "ProtectIA: A geospatial tool for avian-influenza prevention",
    "Herramientas de geoprocesamiento como ayuda a enfermedades emergentes": "Geoprocessing tools to support emerging-disease response",
    "Epidemiología y análisis espacial: Aplicación de los SIG para entender la dinámica de las enfermedades y para la gestión de la salud pública y animal con una perspectiva One Health": "Epidemiology and spatial analysis: using GIS to understand disease dynamics and manage public and animal health from a One Health perspective",
    "Contaminación de suelos por antibióticos y genes de resistencia a antimicrobianos": "Soil contamination by antibiotics and antimicrobial-resistance genes",
    "Sistema de alerta a tiempo real para influenza aviar: DiFLUsion": "Real-time avian-influenza warning system: DiFLUsion",
    "Hormigas, gallinas y matemáticas": "Ants, chickens and mathematics",
    "Oral · INIAciando ciencia": "Oral · INIAciando Science",
    "Sistema de vigilancia de influenza aviar DiFLUsion: aplicación directa de los datos de los programas de Ciencia Ciudadana de SEO/BirdLife": "DiFLUsion avian-influenza surveillance system: direct use of data from SEO/BirdLife citizen-science programmes",
    "Asesoría científico-técnica": "Scientific and technical advice",
    "Asesoría técnica sobre la situación de la Influenza Aviar de Alta Patogenicidad (IAAP)": "Technical advice on the highly pathogenic avian influenza (HPAI) situation",
    "Asesoría técnica sobre la situación de la Influenza Aviar de Alta Patogenicidad (IAAP) y el uso de DiFLUsion como sistema de alerta temprana": "Technical advice on the highly pathogenic avian influenza (HPAI) situation and the use of DiFLUsion as an early-warning system",
    "Múltiples sesiones de colaboración con organismos nacionales e internacionales, administraciones y otros actores implicados en la vigilancia sanitaria, aportando análisis epidemiológico, interpretación del riesgo y herramientas para apoyar la toma de decisiones y la preparación frente a posibles introducciones de la enfermedad.": "Multiple collaborative sessions with national and international organisations, public authorities and other stakeholders involved in health surveillance, providing epidemiological analysis, risk interpretation and tools to support decision-making and preparedness for possible disease introductions.",
    "· sesiones: julio 2022, febrero 2023, julio 2023, octubre 2023.": "· sessions: July 2022, February 2023, July 2023 and October 2023.",
    "Cursos impartidos y actividad docente": "Taught courses and teaching activity",
    "Docencia internacional destacada": "Featured international teaching",
    "Taller docente sobre el papel de los paseriformes en la conectividad de influenza aviar y resistencia antimicrobiana bajo escenarios de cambio climático.": "Workshop on the role of passerines in the connectivity of avian influenza and antimicrobial resistance under climate-change scenarios.",
    "Curso internacional sobre análisis de riesgo para el control de enfermedades animales transfronterizas, impartido para la representación subregional de WOAH en el Sudeste Asiático.": "International course on risk analysis for transboundary animal-disease control, delivered for WOAH's Sub-Regional Representation for South-East Asia.",
    "Implementación de la IA en la investigación en sanidad animal": "Implementing AI in animal-health research",
    "Formación aplicada sobre inteligencia artificial, big data y digitalización en investigación de sanidad animal y medicamentos veterinarios.": "Applied training in artificial intelligence, big data and digitalisation for animal-health and veterinary-medicine research.",
    "Tutor del Programa Científic@s en Prácticas": "Mentor for the Scientists in Practice programme",
    "Tutorización de estudiantes durante una experiencia de inmersión en investigación científica en el CISA-INIA/CSIC.": "Mentoring students during an immersive scientific-research placement at CISA-INIA/CSIC.",
    "Análisis de la distribución espacio-temporal de distintas enfermedades animales": "Analysis of the spatio-temporal distribution of several animal diseases",
    "Supervisión de prácticas externas centradas en el análisis de la distribución espacio-temporal de enfermedades animales.": "Supervision of external placements focused on the spatio-temporal distribution of animal diseases.",
    "Herramientas matemáticas aplicadas al suavizado temporal de rutas migratorias": "Mathematical tools for temporal smoothing of migration routes",
    "Supervisión de un Trabajo de Fin de Grado sobre herramientas matemáticas para el suavizado temporal de rutas migratorias.": "Supervision of a bachelor's thesis on mathematical tools for temporal smoothing of migration routes.",
    "Análisis de la distribución espacio-temporal de brotes de IAAP en España": "Analysis of the spatio-temporal distribution of HPAI outbreaks in Spain",
    "Supervisión de prácticas externas sobre el análisis de la distribución espacio-temporal de brotes de influenza aviar de alta patogenicidad en España.": "Supervision of external placements on the spatio-temporal distribution of highly pathogenic avian-influenza outbreaks in Spain.",
    "Seminarios, jornadas, talleres y otros foros": "Seminars, workshops and other forums",
    "Principal": "Lead",
    "Docente": "Instructor",
    "Inteligencia Artificial: Base y modelos aplicables al grupo de Epidemiología y Sanidad Ambiental": "Artificial Intelligence: foundations and models for the Epidemiology and Environmental Health group",
    "SMARTe: Una interfaz espacial para la vigilancia ambiental estandarizada mediante AMR": "SMARTe: A spatial interface for standardised environmental AMR surveillance",
    "ProtectIA: Herramienta multicriterio para la priorización del riesgo de influenza aviar en comarcas ganaderas": "ProtectIA: A multi-criteria tool for prioritising avian-influenza risk in livestock districts",
    "Análisis de datos en epidemiología": "Data analysis in epidemiology",
    "DiFLUsion: un modelo SIG aplicado a la industria ganadera": "DiFLUsion: a GIS model applied to the livestock industry",
    "DiFLUsion: sistema de alerta a tiempo real frente a la influenza aviar": "DiFLUsion: a real-time avian-influenza warning system",
    "Laboratorio Central de Veterinaria de Algete · abril 2023": "Central Veterinary Laboratory of Algete · April 2023",
    "Herramientas desarrolladas": "Developed tools",
    "Sistema de alerta temprana para influenza aviar de alta patogenicidad": "Early-warning system for highly pathogenic avian influenza",
    "DiFLUsion es un modelo matemático que estima el riesgo de introducción de IAAP a partir de las conexiones migratorias entre territorios con brotes y zonas susceptibles de aparición, integrando información epidemiológica, espacial y temporal.": "DiFLUsion is a mathematical model that estimates the risk of HPAI introduction from migratory connections between outbreak areas and areas susceptible to emergence, integrating epidemiological, spatial and temporal information.",
    "Marco digital geoespacial para estandarizar y comparar la presión ambiental asociada a la resistencia antimicrobiana (AMR) desencadenada por fuentes antropogénicas. Integra características del territorio y permite incorporar puntos de estudio definidos por el usuario, facilitando análisis  entre estudios.": "A geospatial digital framework for standardising and comparing environmental pressure associated with antimicrobial resistance (AMR) from anthropogenic sources. It integrates territorial characteristics and user-defined study points to facilitate cross-study analyses.",
    "FrontWave es un marco de análisis espacio-temporal para reconstruir el avance temprano de una epidemia a partir de observaciones georreferenciadas. Compara distintas estrategias de selección espacial e interpolación para generar superficies de tiempo de llegada, permitiendo caracterizar la expansión territorial de la propagación.": "FrontWave is a spatio-temporal analysis framework for reconstructing the early advance of an epidemic from georeferenced observations. It compares spatial-selection and interpolation strategies to generate arrival-time surfaces and characterise territorial spread.",
    "Paneles web interactivos para explorar y visualizar eventos epidemiológicos, junto con datos espaciales, temporales y ambientales. Desarrollados como soporte para las actividades  análisis del grupo EySA, facilitan la consulta, interpretación y seguimiento de la situación epidemiológica.": "Interactive web dashboards for exploring and visualising epidemiological events alongside spatial, temporal and environmental data. Developed to support the EySA group's analyses, they facilitate consultation, interpretation and monitoring of the epidemiological situation.",
    "Herramienta geoespacial multicriterio para la prevención de la influenza aviar": "Multi-criteria geospatial tool for avian-influenza prevention",
    "Prioriza comarcas y explotaciones avícolas según su riesgo de introducción de IAAP. Integra presencia de aves silvestres, contexto territorial, densidad ganadera y bioseguridad. Traduce el análisis multicriterio en mapas operativos para orientar vigilancia, prevención y asignación de recursos.": "Prioritises livestock districts and poultry holdings according to their risk of HPAI introduction. It integrates wild-bird presence, territorial context, livestock density and biosecurity, translating multi-criteria analysis into operational maps for surveillance, prevention and resource allocation.",
    "Sistema de alerta espacio-temporal para influenza aviar de alta patogenicidad": "Spatio-temporal warning system for highly pathogenic avian influenza",
    "Identifica semanalmente zonas con riesgo de introducción de IAAP en España. Integra notificaciones WOAH, temperaturas de AEMET, fenología y rutas migratorias de aves. Su arquitectura modular combina ArcGIS Pro y Python para generar alertas operativas de vigilancia.": "Identifies areas at risk of HPAI introduction in Spain each week. It integrates WOAH notifications, AEMET temperatures, phenology and bird-migration routes. Its modular ArcGIS Pro and Python architecture generates operational surveillance alerts.",
    "Marco digital espacial para estandarizar la presión ambiental vinculada a la resistencia antimicrobiana. Integra fuentes antropogénicas, contexto territorial y puntos de muestreo. Facilita análisis AMR comparables y escalables entre estudios, regiones y países.": "A spatial digital framework for standardising environmental pressure associated with antimicrobial resistance. It integrates anthropogenic sources, territorial context and sampling points, enabling comparable and scalable AMR analyses across studies, regions and countries.",
    "Simula escenarios de vacunación del jabalí frente a la peste porcina africana. Traduce el efecto espacial en zonas de restricción y pérdidas evitadas para el sector porcino. Combina autómatas celulares, datos epidemiológicos y evaluación económica.": "Simulates wild-boar vaccination scenarios against African swine fever. It translates spatial effects into restriction zones and avoided losses for the pig sector, combining cellular automata, epidemiological data and economic assessment.",
    "Visor interactivo para analizar la velocidad y dirección del frente epidémico de PPA en jabalí. Convierte notificaciones espacio-temporales en una lectura rápida del avance. Ayuda a priorizar la vigilancia y las estrategias territoriales de control.": "An interactive viewer for analysing the speed and direction of the ASF epidemic front in wild boar. It turns spatio-temporal notifications into a rapid picture of disease progression and supports the prioritisation of surveillance and territorial control strategies.",
    "Paneles web que integran brotes, movimientos, población susceptible y variables ambientales para describir y anticipar riesgos. Incluyen desarrollos como DashFLUboard y aplicaciones de vigilancia HPAI en Europa y Kazajistán. Acercan el análisis espacial a usuarios no especialistas.": "Web dashboards integrating outbreaks, movements, susceptible populations and environmental variables to describe and anticipate risk. They include DashFLUboard and HPAI-surveillance applications for Europe and Kazakhstan, making spatial analysis accessible to non-specialist users.",
    "Abrir referencia ↗": "Open reference ↗",
    "Pasa el cursor, usa las flechas del teclado o toca una tarjeta para explorar.": "Hover, use the arrow keys or tap a card to explore.",
    "Divulgación científica": "Science outreach",
    "Divulgación destacada": "Featured science outreach",
    "Instituto de Investigación en Inteligencia Artificial (IIIA - CSIC) · Barcelona · febrero 2026": "Artificial Intelligence Research Institute (IIIA-CSIC) · Barcelona · February 2026",
    "Detectives de epidemias: Gallinas y matemáticas": "Epidemic detectives: chickens and mathematics",
    "Charla sobre cómo la física, las matemáticas y los datos ayudan a seguir y anticipar una epidemia.": "Talk on how physics, mathematics and data can help track and anticipate an epidemic.",
    "Abrir enlace ↗": "Open link ↗",
    "Tutorización de estudiantes para conocer de primera mano el trabajo y los métodos de la investigación científica.": "Mentoring students so they can experience scientific work and research methods first-hand.",
    "Semana de la Ciencia y la Tecnología · 2022": "Science and Technology Week · 2022",
    "Epidemias y pandemias, conviértete en el virus más peligroso": "Epidemics and pandemics: become the most dangerous virus",
    "Actividad participativa para comprender de forma lúdica la propagación y las cadenas de transmisión de agentes infecciosos.": "An interactive activity exploring the spread and transmission chains of infectious agents through play.",
    "Conviértete en un auténtico detective de epidemias": "Become a real epidemic detective",
    "Taller participativo centrado en observación, datos y toma de decisiones frente a brotes.": "An interactive workshop focused on observation, data and decision-making during outbreaks.",
    "Noche Europea de los Investigadores · 2022": "European Researchers' Night · 2022",
    "Premios, becas y estancias": "Awards, fellowships and research stays",
    "Estancia de Investigación MOVTEC 2025-12": "MOVTEC 2025-12 research stay",
    "Premio a la Investigación 2024": "2024 Research Award",
    "Beca de introducción a la actividad investigadora": "Introduction to Research Fellowship",
    "Instituto Universitario de Física Fundamental y Matemáticas (IUFFYM) · Salamanca · enero 2021": "University Institute of Fundamental Physics and Mathematics (IUFFYM) · Salamanca · January 2021",
    "Habilidades e Idiomas": "Skills and Languages",
    "Inglés": "English",
    "Idioma": "Language",
    "Teléfono": "Phone",
    "Actualizado: 07/08/2026": "Updated: 07/08/2026",
    "Retrato de Pablo Ibáñez-Porras": "Portrait of Pablo Ibáñez-Porras",
    "Resumen de participación científica": "Summary of scientific participation",
    "Áreas de participación científica": "Areas of scientific activity",
    "Carrusel de herramientas científicas": "Scientific-tools carousel",
    "Abrir Detectives de epidemias: Gallinas y matemáticas": "Open Epidemic detectives: chickens and mathematics",
    "Abrir Epidemias y pandemias, conviértete en el virus más peligroso": "Open Epidemics and pandemics: become the most dangerous virus",
}


PHRASE_REPLACEMENTS = (
    ("Abrir enlace:", "Open link:"),
    ("Publicación ·", "Publication ·"),
    ("Póster ·", "Poster ·"),
    ("Conferencia Esri España", "Esri Spain Conference"),
    ("IV Jornadas Internacionales de Jóvenes Investigadores", "4th International Young Researchers Meeting"),
    ("I Congreso Interdisciplinar de Medicina e Ingeniería", "1st Interdisciplinary Congress on Medicine and Engineering"),
    ("2ª Asamblea general de la Conexión CSIC de Biología Computacional y Bioinformática", "2nd General Assembly of the CSIC Computational Biology and Bioinformatics Network"),
    ("X Simposio CONDEGRES", "10th CONDEGRES Symposium"),
    ("Jornadas Vigilancia Sanitaria 2023: presente y futuro para 2030", "Health Surveillance Meeting 2023: present and future towards 2030"),
    ("Congreso Español de Ornitología", "Spanish Ornithology Congress"),
    ("Taller de formación sobre Inteligencia Artificial, Big Data y digitalización en medicamentos veterinarios", "Workshop on Artificial Intelligence, Big Data and digitalisation in veterinary medicines"),
    ("Supervisión de Trabajo de Fin de Grado", "Bachelor's thesis supervision"),
    ("Supervisión de prácticas externas", "External-placement supervision"),
    ("CISA-INIA/CSIC (seminario interno)", "CISA-INIA/CSIC (internal seminar)"),
    ("Jornada Tecnología Geográfica (JTG) en CSIC 2026: Innovación, Análisis y Ciencia", "CSIC Geographic Technology Meeting 2026: Innovation, Analysis and Science"),
    ("Jornada Científica Desafío Gripes Zoonóticas", "Zoonotic Influenza Challenge Scientific Meeting"),
    ("Ciclos de webinar UI1", "UI1 webinar series"),
    ("Seminario", "Seminar"),
    ("Taller", "Workshop"),
    ("enero", "January"),
    ("febrero", "February"),
    ("marzo", "March"),
    ("abril", "April"),
    ("mayo", "May"),
    ("junio", "June"),
    ("julio", "July"),
    ("agosto", "August"),
    ("septiembre", "September"),
    ("octubre", "October"),
    ("noviembre", "November"),
    ("diciembre", "December"),
    (" · Docente · ", " · Instructor · "),
    ("Divulgación ·", "Science outreach ·"),
    ("Docencia ·", "Teaching ·"),
    ("Barcelona ·", "Barcelona ·"),
    ("Madrid ·", "Madrid ·"),
)


SPANISH_CHECK = re.compile(
    r"\b(?:investigador|formación|actividad|herramientas|divulgación|contacto|"
    r"investigación|vigilancia|enfermedad|análisis|modelo|sistema|taller|seminario|"
    r"asesoría|supervisión|ciencia|científica|epidemiología|matemáticas|docente)\b",
    re.I,
)


def translate_value(value: str) -> str:
    translated = TRANSLATIONS.get(value, value)
    if translated == value:
        for source, target in PHRASE_REPLACEMENTS:
            translated = translated.replace(source, target)
    return translated


def translate_html(source: str) -> tuple[str, list[str]]:
    protected: list[str] = []

    def stash(match: re.Match[str]) -> str:
        protected.append(match.group(0))
        return f"@@CV_PROTECTED_{len(protected) - 1}@@"

    working = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", stash, source, flags=re.I | re.S)

    def translate_node(match: re.Match[str]) -> str:
        raw = match.group(1)
        stripped = raw.strip()
        if not stripped:
            return match.group(0)
        prefix = raw[: len(raw) - len(raw.lstrip())]
        suffix = raw[len(raw.rstrip()) :]
        return ">" + prefix + html.escape(translate_value(html.unescape(stripped)), quote=False) + suffix + "<"

    working = re.sub(r">([^<]+)<", translate_node, working)

    def translate_attribute(match: re.Match[str]) -> str:
        return match.group(1) + html.escape(translate_value(html.unescape(match.group(2))), quote=True) + match.group(3)

    working = re.sub(r'((?:aria-label|alt|title|placeholder|content)=")([^"]*)(")', translate_attribute, working, flags=re.I)
    working = working.replace('<html lang="es">', '<html lang="en">', 1)
    working = working.replace(
        '<a class="lang-switch" href="index-en.html" hreflang="en" lang="en">English</a>',
        '<a class="lang-switch" href="index.html" hreflang="es" lang="es">Español</a>',
        1,
    )
    working = working.replace(
        'href="CV%20Pablo%20Ib%C3%A1%C3%B1ez-Porras.pdf"',
        'href="CV%20Pablo%20Ib%C3%A1%C3%B1ez-Porras%20EN.pdf"',
        1,
    )

    for index, block in enumerate(protected):
        working = working.replace(f"@@CV_PROTECTED_{index}@@", block)
    working = working.replace(
        '"jobTitle": "Investigador predoctoral en CISA-INIA-CSIC"',
        '"jobTitle": "Predoctoral Researcher at CISA-INIA-CSIC"',
        1,
    )

    missing: list[str] = []
    for match in re.finditer(r">([^<]+)<", re.sub(r"<(script|style)\b[^>]*>.*?</\1>", "", working, flags=re.I | re.S)):
        candidate = html.unescape(match.group(1)).strip()
        if candidate and SPANISH_CHECK.search(candidate) and candidate not in missing:
            missing.append(candidate)
    return working, missing


def write_english(source_path: Path, output_path: Path) -> list[str]:
    translated, missing = translate_html(source_path.read_text(encoding="utf-8"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(prefix=output_path.stem + ".", suffix=".tmp", dir=output_path.parent)
    os.close(handle)
    temp_path = Path(temp_name)
    try:
        temp_path.write_text(translated, encoding="utf-8", newline="\n")
        os.replace(temp_path, output_path)
    finally:
        temp_path.unlink(missing_ok=True)
    return missing


def main() -> None:
    cv_dir = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=cv_dir / "index.html")
    parser.add_argument("--output", type=Path, default=cv_dir / "index-en.html")
    args = parser.parse_args()
    missing = write_english(args.source.resolve(), args.output.resolve())
    print(f"English CV generated: {args.output.resolve()}")
    if missing:
        print("Review pending translations:")
        for item in missing:
            print(f"- {item}")


if __name__ == "__main__":
    main()
