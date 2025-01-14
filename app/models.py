import sqlite3
from datetime import datetime

DB_NAME = "anomaly_analysis.db"

def insert_severity_levels():
  """Inserta niveles de severidad por defecto."""
  connection = sqlite3.connect(DB_NAME)
  cursor = connection.cursor()

  levels = [("low",), ("medium",), ("high",)]
  try:
    cursor.executemany("INSERT INTO severity_level (name) VALUES (?);", levels)
    connection.commit()
  except sqlite3.IntegrityError:
    pass

  connection.close()

def add_document(title, document_type, content=None, source=None):
  """Añade un documento a la tabla documents."""
  connection = sqlite3.connect(DB_NAME)
  cursor = connection.cursor()

  cursor.execute("""
  INSERT INTO document (title, document_type, content, source) 
  VALUES (?, ?, ?, ?);
  """, (title, document_type, content, source))
    
  connection.commit()
  document_id = cursor.lastrowid
  connection.close()
  return document_id

def add_anomaly(name, severity_id, document_id):
  """Añade una anomalía a la tabla anomalies."""
  connection = sqlite3.connect(DB_NAME)
  cursor = connection.cursor()

  cursor.execute("""
  INSERT INTO anomalie (name, severity_id, document_id) 
  VALUES (?, ?, ?);
  """, (name, severity_id, document_id))
    
  connection.commit()
  anomaly_id = cursor.lastrowid
  connection.close()
  return anomaly_id

def get_all_anomalies():
  """Obtiene todas las anomalías con detalles relacionados."""
  connection = sqlite3.connect(DB_NAME)
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()

  cursor.execute("""
  SELECT 
    a.id AS anomalyId,
    a.name AS anomalyName,
    s.name AS severity,
    d.title AS documentTitle,
    d.document_type AS documentType,
    d.source AS documentSource,
    a.created_at AS detectedAt
  FROM 
    anomalie a
  JOIN 
    severity_level s ON a.severity_id = s.id
  JOIN 
    document d ON a.document_id = d.id
  ORDER BY 
    a.created_at DESC;
  """)
    
  results = [dict(row) for row in cursor.fetchall()]
  connection.close()
    
  return results
