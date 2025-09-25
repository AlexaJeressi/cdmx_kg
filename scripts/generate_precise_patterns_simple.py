#!/usr/bin/env python3
"""
Generate precise but simple regex patterns for all laws from CSV data
This creates exact patterns for each law name without over-escaping
"""

import pandas as pd
import re

def create_simple_pattern(law_name):
    """Create a simple, readable regex pattern for exact law name matching"""
    # Clean the law name
    cleaned = law_name.strip()
    
    # Remove quotes if present
    if cleaned.startswith('"') and cleaned.endswith('"'):
        cleaned = cleaned[1:-1]
    
    # Escape only the essential regex characters that might actually appear in law names
    pattern = cleaned
    pattern = pattern.replace('(', r'\(')
    pattern = pattern.replace(')', r'\)')
    pattern = pattern.replace('.', r'\.')
    
    # Make spaces flexible (handle multiple spaces)
    pattern = re.sub(r'\s+', r'\\s+', pattern)
    
    # Add word boundaries for precise matching
    pattern = r'\b' + pattern + r'\b'
    
    return pattern

def categorize_law(law_name):
    """Simple categorization based on law type"""
    name_lower = law_name.lower()
    
    if 'código' in name_lower:
        if 'federal' in name_lower:
            return 'CODIGO_FEDERAL'
        elif 'ciudad de méxico' in name_lower or 'distrito federal' in name_lower:
            return 'CODIGO_CDMX'
        else:
            return 'CODIGO'
    elif 'ley orgánica' in name_lower:
        return 'LEY_ORGANICA'
    elif 'ley general' in name_lower:
        return 'LEY_GENERAL'
    elif 'ley nacional' in name_lower:
        return 'LEY_NACIONAL'
    elif 'ley federal' in name_lower:
        return 'LEY_FEDERAL'
    elif 'reglamento' in name_lower:
        return 'REGLAMENTO'
    elif 'constitución' in name_lower:
        return 'CONSTITUCION'
    elif 'ley' in name_lower:
        if 'ciudad de méxico' in name_lower or 'distrito federal' in name_lower:
            return 'LEY_CDMX'
        else:
            return 'LEY'
    else:
        return 'OTRO'

def generate_federal_patterns():
    """Generate simple patterns for federal laws"""
    print("Reading federal laws data...")
    df = pd.read_csv('/Users/alexa/Projects/cdmx_kg/data/leyes_reglamentos_federales.csv')
    
    patterns = []
    
    for idx, row in df.iterrows():
        law_name = str(row['nombre']).strip()
        if pd.isna(law_name) or law_name == 'nombre':
            continue
            
        # Create simple regex pattern
        pattern = create_simple_pattern(law_name)
        
        # Categorize
        category = categorize_law(law_name)
        
        # Create the tuple (pattern, full_name, category)
        patterns.append((pattern, law_name.upper(), category))
    
    print(f"Generated {len(patterns)} federal law patterns")
    return patterns

def generate_cdmx_patterns():
    """Generate simple patterns for CDMX laws"""
    print("Reading CDMX laws data...")
    df = pd.read_csv('/Users/alexa/Projects/cdmx_kg/data/leyes_reglamentos_cdmx.csv')
    
    patterns = []
    
    for idx, row in df.iterrows():
        law_name = str(row['name']).strip()
        if pd.isna(law_name) or law_name == 'name':
            continue
            
        # Create simple regex pattern
        pattern = create_simple_pattern(law_name)
        
        # Categorize
        category = categorize_law(law_name)
        
        # Create the tuple (pattern, full_name, category)
        patterns.append((pattern, law_name.upper(), category))
    
    print(f"Generated {len(patterns)} CDMX law patterns")
    return patterns

def write_patterns_file(patterns, filename, title, description):
    """Write clean patterns to a Python file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n")
        f.write(f"# {description}\n")
        f.write("# Auto-generated precise patterns for each law\n\n")
        
        f.write("LAWS_REGEX = [\n")
        for pattern, full_name, category in patterns:
            # Escape quotes in the pattern and name for Python string
            pattern_safe = pattern.replace('"', '\\"')
            name_safe = full_name.replace('"', '\\"')
            f.write(f'    (r"{pattern_safe}", "{name_safe}", "{category}"),\n')
        
        f.write("]\n\n")
        
        # Generate categories dictionary
        categories = set(pattern[2] for pattern in patterns)
        f.write("LAW_CATEGORIES = {\n")
        for category in sorted(categories):
            f.write(f'    "{category}": "{category.replace("_", " ").title()}",\n')
        f.write("}\n")

if __name__ == "__main__":
    print("Generating simple, precise regex patterns for all laws...")
    
    # Generate federal patterns
    federal_patterns = generate_federal_patterns()
    write_patterns_file(
        federal_patterns,
        '/Users/alexa/Projects/cdmx_kg/scripts/federal_laws_patterns_precise.py',
        'Precise Federal Laws Patterns',
        'Simple, exact regex patterns for each federal law from leyes_reglamentos_federales.csv'
    )
    
    # Generate CDMX patterns  
    cdmx_patterns = generate_cdmx_patterns()
    write_patterns_file(
        cdmx_patterns,
        '/Users/alexa/Projects/cdmx_kg/scripts/cdmx_laws_patterns_precise.py',
        'Precise CDMX Laws Patterns', 
        'Simple, exact regex patterns for each CDMX law from leyes_reglamentos_cdmx.csv'
    )
    
    print(f"\n✅ Generated simple, precise patterns:")
    print(f"   - Federal: {len(federal_patterns)} laws")
    print(f"   - CDMX: {len(cdmx_patterns)} laws")
    print(f"   - Total: {len(federal_patterns) + len(cdmx_patterns)} precise patterns")
    print("\nFiles created:")
    print("   - federal_laws_patterns_precise.py")
    print("   - cdmx_laws_patterns_precise.py")
