# Improved examples for LangExtract to reduce alignment warnings
# Copy these examples into your notebook Cell 5

# Examples for government entity extraction - based on real legal document patterns
gov_entity_examples = [
    lx.data.ExampleData(
        text="Son autoridades en materia ambiental en la Ciudad de México: I. La Jefatura de Gobierno; II. La Secretaría del Medio Ambiente;",
        extractions=[
            lx.data.Extraction(extraction_class="entity", extraction_text="Jefatura de Gobierno"),
            lx.data.Extraction(extraction_class="entity", extraction_text="Secretaría del Medio Ambiente")
        ]
    ),
    lx.data.ExampleData(
        text="La aplicación de esta Ley corresponde al Gobierno de la Ciudad de México, a través de la Secretaría y las Alcaldías.",
        extractions=[
            lx.data.Extraction(extraction_class="entity", extraction_text="Gobierno de la Ciudad de México"),
            lx.data.Extraction(extraction_class="entity", extraction_text="Secretaría"),
            lx.data.Extraction(extraction_class="entity", extraction_text="Alcaldías")
        ]
    ),
    lx.data.ExampleData(
        text="El Tribunal Superior de Justicia de la Ciudad de México y la Procuraduría General de Justicia tendrán competencia.",
        extractions=[
            lx.data.Extraction(extraction_class="entity", extraction_text="Tribunal Superior de Justicia de la Ciudad de México"),
            lx.data.Extraction(extraction_class="entity", extraction_text="Procuraduría General de Justicia")
        ]
    ),
    lx.data.ExampleData(
        text="La Comisión Ambiental Metropolitana y el Instituto de Verificación Administrativa de la Ciudad de México colaborarán.",
        extractions=[
            lx.data.Extraction(extraction_class="entity", extraction_text="Comisión Ambiental Metropolitana"),
            lx.data.Extraction(extraction_class="entity", extraction_text="Instituto de Verificación Administrativa de la Ciudad de México")
        ]
    ),
    lx.data.ExampleData(
        text="SEDEMA coordinará con las alcaldías y la Procuraduría Ambiental y del Ordenamiento Territorial (PAOT).",
        extractions=[
            lx.data.Extraction(extraction_class="entity", extraction_text="SEDEMA"),
            lx.data.Extraction(extraction_class="entity", extraction_text="alcaldías"),
            lx.data.Extraction(extraction_class="entity", extraction_text="Procuraduría Ambiental y del Ordenamiento Territorial"),
            lx.data.Extraction(extraction_class="entity", extraction_text="PAOT")
        ]
    ),
    lx.data.ExampleData(
        text="La Universidad Autónoma de la Ciudad de México (UACM) y la Secretaría de Educación participarán en programas ambientales.",
        extractions=[
            lx.data.Extraction(extraction_class="entity", extraction_text="Universidad Autónoma de la Ciudad de México"),
            lx.data.Extraction(extraction_class="entity", extraction_text="UACM"),
            lx.data.Extraction(extraction_class="entity", extraction_text="Secretaría de Educación")
        ]
    )
]

# Examples for article mention extraction - based on real legal document patterns
article_mention_examples = [
    lx.data.ExampleData(
        text="La presente Ley es reglamentaria de las disposiciones contenidas en el Apartado A del artículo 13 de la Constitución Política de la Ciudad de México",
        extractions=[
            lx.data.Extraction(extraction_class="mention", extraction_text="artículo 13 de la Constitución Política de la Ciudad de México"),
            lx.data.Extraction(extraction_class="mention", extraction_text="la presente Ley")
        ]
    ),
    lx.data.ExampleData(
        text="En todo lo no previsto en la presente Ley, se aplicará supletoriamente la Ley de Procedimiento Administrativo de la Ciudad de México",
        extractions=[
            lx.data.Extraction(extraction_class="mention", extraction_text="la presente Ley"),
            lx.data.Extraction(extraction_class="mention", extraction_text="la Ley de Procedimiento Administrativo de la Ciudad de México")
        ]
    ),
    lx.data.ExampleData(
        text="De conformidad con lo establecido en el artículo 4º de la Constitución Política de los Estados Unidos Mexicanos",
        extractions=[
            lx.data.Extraction(extraction_class="mention", extraction_text="artículo 4º de la Constitución Política de los Estados Unidos Mexicanos")
        ]
    ),
    lx.data.ExampleData(
        text="Para los efectos de esta Ley se aplicarán las disposiciones del Código Civil para el Distrito Federal",
        extractions=[
            lx.data.Extraction(extraction_class="mention", extraction_text="esta Ley"),
            lx.data.Extraction(extraction_class="mention", extraction_text="del Código Civil para el Distrito Federal")
        ]
    ),
    lx.data.ExampleData(
        text="Las sanciones previstas en los artículos 237 y 238 del Código Penal para el Distrito Federal serán aplicables",
        extractions=[
            lx.data.Extraction(extraction_class="mention", extraction_text="artículos 237 y 238 del Código Penal para el Distrito Federal")
        ]
    ),
    lx.data.ExampleData(
        text="El reglamento de esta Ley establecerá los procedimientos específicos conforme al artículo 89 fracción I",
        extractions=[
            lx.data.Extraction(extraction_class="mention", extraction_text="reglamento de esta Ley"),
            lx.data.Extraction(extraction_class="mention", extraction_text="artículo 89 fracción I")
        ]
    ),
    lx.data.ExampleData(
        text="Los lineamientos que establezca el reglamento de la presente Ley deberán considerar los criterios técnicos",
        extractions=[
            lx.data.Extraction(extraction_class="mention", extraction_text="el reglamento de la presente Ley"),
            lx.data.Extraction(extraction_class="mention", extraction_text="la presente Ley")
        ]
    ),
    lx.data.ExampleData(
        text="Los criterios técnicos y metodológicos se establecerán conforme a las normas oficiales mexicanas que expida la Secretaría",
        extractions=[
            lx.data.Extraction(extraction_class="mention", extraction_text="normas oficiales mexicanas")
        ]
    )
]

print("✅ Improved LangExtract examples defined with better text alignment")

# Enhanced article mention extraction logic with regulation self-reference handling
def extract_article_mentions_enhanced(batch_df):
    """Extract article mentions with proper handling of regulation self-references"""
    
    mentions = []
    
    # Get the current law name for self-references
    current_law = batch_df.iloc[0]['document_name'] if len(batch_df) > 0 else "LEY AMBIENTAL DE LA CIUDAD DE MÉXICO"
    
    # Process each row individually
    for row in batch_df.itertuples():
        try:
            result = lx.extract(
                text_or_documents=row.text,
                prompt_description=f"Extract ALL legal references from this Mexican legal text. Include article numbers, law names, constitutional references, codes, regulations, decrees, and treaties. For self-references like 'esta Ley' or 'la presente Ley', consider it as referring to: {current_law}",
                examples=article_mention_examples,
                model_id="gpt-4o-mini",
                api_key=os.environ.get('OPENAI_API_KEY'),
                fence_output=True,
                use_schema_constraints=False
            )
            
            if result and hasattr(result, 'extractions'):
                for extraction in result.extractions:
                    if hasattr(extraction, 'extraction_text'):
                        mention_text = extraction.extraction_text
                        
                        # Parse the extracted text to identify components
                        art_num = None
                        law_name = None
                        processed_mention = mention_text
                        
                        # Handle regulation self-references
                        if "reglamento de esta ley" in mention_text.lower():
                            law_name = f"REGLAMENTO DE LA {current_law}"
                            processed_mention = mention_text
                        elif "reglamento de la presente ley" in mention_text.lower():
                            law_name = f"REGLAMENTO DE LA {current_law}"
                            processed_mention = mention_text
                        elif "esta ley" in mention_text.lower() or "presente ley" in mention_text.lower():
                            law_name = current_law
                            processed_mention = mention_text
                        else:
                            # Extract article number if present
                            import re
                            art_match = re.search(r'artículo[s]?\s+(\d+)', mention_text.lower())
                            if art_match:
                                art_num = art_match.group(1)
                            
                            # Extract law name based on common patterns
                            if "constitución" in mention_text.lower():
                                if "ciudad de méxico" in mention_text.lower():
                                    law_name = "CONSTITUCIÓN POLÍTICA DE LA CIUDAD DE MÉXICO"
                                else:
                                    law_name = "CONSTITUCIÓN POLÍTICA DE LOS ESTADOS UNIDOS MEXICANOS"
                            elif "código civil" in mention_text.lower():
                                law_name = "CÓDIGO CIVIL PARA EL DISTRITO FEDERAL"
                            elif "código penal" in mention_text.lower():
                                law_name = "CÓDIGO PENAL PARA EL DISTRITO FEDERAL"
                            elif "ley de procedimiento administrativo" in mention_text.lower():
                                law_name = "LEY DE PROCEDIMIENTO ADMINISTRATIVO DE LA CIUDAD DE MÉXICO"
                            elif "normas oficiales mexicanas" in mention_text.lower():
                                law_name = "NORMAS OFICIALES MEXICANAS"
                            else:
                                law_name = mention_text
                        
                        mentions.append({
                            'row_id': row.row_id,
                            'art_num': art_num,
                            'law_name': law_name or mention_text,
                            'mention_extraction': processed_mention
                        })
        
        except Exception as e:
            print(f"Error extracting mentions for row {row.row_id}: {e}")
            continue
    
    return mentions
