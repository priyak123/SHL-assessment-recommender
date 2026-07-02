import json

trace_recs = {
  "Occupational Personality Questionnaire OPQ32r": {
    "test_type": "P",
    "url": "https://www.shl.com/products/product-catalog/view/occupational-personality-questionnaire-opq32r/"
  },
  "OPQ Universal Competency Report 2.0": {
    "test_type": "P",
    "url": "https://www.shl.com/products/product-catalog/view/opq-universal-competency-report-2-0/"
  },
  "OPQ Leadership Report": {
    "test_type": "P",
    "url": "https://www.shl.com/products/product-catalog/view/opq-leadership-report/"
  },
  "SHL Verify Interactive G+": {
    "test_type": "A",
    "url": "https://www.shl.com/products/product-catalog/view/shl-verify-interactive-g/"
  },
  "Graduate Scenarios": {
    "test_type": "B",
    "url": "https://www.shl.com/products/product-catalog/view/graduate-scenarios/"
  },
  "Smart Interview Live Coding": {
    "test_type": "K",
    "url": "https://www.shl.com/products/product-catalog/view/smart-interview-live-coding/"
  },
  "Linux Programming (General)": {
    "test_type": "K",
    "url": "https://www.shl.com/products/product-catalog/view/linux-programming-general/"
  },
  "Networking and Implementation (New)": {
    "test_type": "K",
    "url": "https://www.shl.com/products/product-catalog/view/networking-and-implementation-new/"
  },
  "SVAR Spoken English (US) (New)": {
    "test_type": "K",
    "url": "https://www.shl.com/products/product-catalog/view/svar-spoken-english-us-new/"
  },
  "Contact Center Call Simulation (New)": {
    "test_type": "S",
    "url": "https://www.shl.com/products/product-catalog/view/contact-center-call-simulation-new/"
  },
  "Entry Level Customer Serv - Retail & Contact Center": {
    "test_type": "P,C",
    "url": "https://www.shl.com/products/product-catalog/view/entry-level-customer-serv-retail-and-contact-center/"
  },
  "Customer Service Phone Simulation": {
    "test_type": "B,S",
    "url": "https://www.shl.com/products/product-catalog/view/customer-service-phone-simulation/"
  },
  "SHL Verify Interactive – Numerical Reasoning": {
    "test_type": "A,S",
    "url": "https://www.shl.com/products/product-catalog/view/shl-verify-interactive-numerical-reasoning/"
  },
  "Financial Accounting (New)": {
    "test_type": "K",
    "url": "https://www.shl.com/products/product-catalog/view/financial-accounting-new/"
  },
  "Basic Statistics (New)": {
    "test_type": "K",
    "url": "https://www.shl.com/products/product-catalog/view/basic-statistics-new/"
  },
  "Global Skills Assessment": {
    "test_type": "C, K",
    "url": "https://www.shl.com/products/product-catalog/view/global-skills-assessment/"
  },
  "Global Skills Development Report": {
    "test_type": "D",
    "url": "https://www.shl.com/products/product-catalog/view/global-skills-development-report/"
  },
  "OPQ MQ Sales Report": {
    "test_type": "P",
    "url": "https://www.shl.com/products/product-catalog/view/opq-mq-sales-report/"
  },
  "Sales Transformation 2.0 - Individual Contributor": {
    "test_type": "P",
    "url": "https://www.shl.com/products/product-catalog/view/salestransformationreport2-0-individualcontributor/"
  },
  "Dependability and Safety Instrument (DSI)": {
    "test_type": "P",
    "url": "https://www.shl.com/products/product-catalog/view/dependability-and-safety-instrument-dsi/"
  },
  "Manufac. & Indust. - Safety & Dependability 8.0": {
    "test_type": "P",
    "url": "https://www.shl.com/products/product-catalog/view/safety-and-dependability-focus-8-0/"
  },
  "Workplace Health and Safety (New)": {
    "test_type": "K",
    "url": "https://www.shl.com/products/product-catalog/view/workplace-health-and-safety-new/"
  },
  "HIPAA (Security)": {
    "test_type": "K",
    "url": "https://www.shl.com/products/product-catalog/view/hipaa-security/"
  },
  "Medical Terminology (New)": {
    "test_type": "K",
    "url": "https://www.shl.com/products/product-catalog/view/medical-terminology-new/"
  },
  "Microsoft Word 365 - Essentials (New)": {
    "test_type": "K,S",
    "url": "https://www.shl.com/products/product-catalog/view/microsoft-word-365-essentials-new/"
  },
  "MS Excel (New)": {
    "test_type": "K",
    "url": "https://www.shl.com/products/product-catalog/view/ms-excel-new/"
  },
  "MS Word (New)": {
    "test_type": "K",
    "url": "https://www.shl.com/products/product-catalog/view/ms-word-new/"
  },
  "Microsoft Excel 365 (New)": {
    "test_type": "K,S",
    "url": "https://www.shl.com/products/product-catalog/view/microsoft-excel-365-new/"
  },
  "Microsoft Word 365 (New)": {
    "test_type": "K,S",
    "url": "https://www.shl.com/products/product-catalog/view/microsoft-word-365-new/"
  },
  "Core Java (Advanced Level) (New)": {
    "test_type": "K",
    "url": "https://www.shl.com/products/product-catalog/view/core-java-advanced-level-new/"
  },
  "Spring (New)": {
    "test_type": "K",
    "url": "https://www.shl.com/products/product-catalog/view/spring-new/"
  },
  "RESTful Web Services (New)": {
    "test_type": "K",
    "url": "https://www.shl.com/products/product-catalog/view/restful-web-services-new/"
  },
  "SQL (New)": {
    "test_type": "K",
    "url": "https://www.shl.com/products/product-catalog/view/sql-new/"
  },
  "Amazon Web Services (AWS) Development (New)": {
    "test_type": "K",
    "url": "https://www.shl.com/products/product-catalog/view/amazon-web-services-aws-development-new/"
  },
  "Docker (New)": {
    "test_type": "K",
    "url": "https://www.shl.com/products/product-catalog/view/docker-new/"
  }
}

catalog = json.load(open('C:/Users/HELLO/.gemini/antigravity/scratch/shl_recommender/shl_product_catalog.json', encoding='utf-8'), strict=False)
catalog_by_url = {item['link']: item for item in catalog}

KEY_MAP = {
    'Ability & Aptitude': 'A',
    'Assessment Exercises': 'E',
    'Biodata & Situational Judgment': 'B',
    'Competencies': 'C',
    'Development & 360': 'D',
    'Knowledge & Skills': 'K',
    'Personality & Behavior': 'P',
    'Simulations': 'S'
}

mismatches = 0
for name, val in trace_recs.items():
    url = val['url']
    exp_type = val['test_type']
    if url not in catalog_by_url:
        print(f"MISM-URL: '{name}' url {url} not found in catalog!")
        mismatches += 1
        continue
    item = catalog_by_url[url]
    mapped = [KEY_MAP[k] for k in item.get('keys', []) if k in KEY_MAP]
    calc_type1 = ','.join(mapped)
    
    # Strip spaces for comparison
    if exp_type.replace(' ', '') != calc_type1.replace(' ', ''):
        print(f"MISM-TYPE: '{name}' | Catalog Name: '{item['name']}' | Exp: '{exp_type}' | Calc: '{calc_type1}'")
        mismatches += 1

print(f"Total mismatches: {mismatches}")
