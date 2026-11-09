// MOCK DATA: Government Schemes and Alerts.
// Includes schemes from data/sample_schemes.json with dual-contract compatibility
// (supports both camelCase frontend fields and snake_case backend fields).

export const schemes = [
  {
    scheme_id: 'sch_pm_kisan',
    slug: 'sch-pm-kisan',
    name: 'Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)',
    schemeName: 'Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)',
    schemeShortTitle: 'PM-KISAN',
    level: 'Central',
    state: 'Central',
    category: 'Agriculture',
    schemeCategory: ['Agriculture, Rural & Environment'],
    tags: ['farmer', 'agriculture', 'income-support', 'central'],
    description: "Income support scheme to all landholding farmers' families in the country to supplement their financial needs for agricultural inputs.",
    briefDescription: "Direct income support of Rs. 6,000/year to all landholding farmer families across India.",
    nodalMinistryName: 'Ministry of Agriculture and Farmers Welfare',
    ministry: 'Ministry of Agriculture and Farmers Welfare',
    schemeFor: 'Individual',
    beneficiaryState: ['All'],
    targetOccupations: ['Farmer', 'Agriculture'],
    maxIncome: null,
    benefits: [
      'Direct benefit transfer of Rs. 6,00,0 per year in three equal 4-monthly installments of Rs. 2,000 each directly into bank accounts.',
      'Aadhaar-linked DBT for 100% transparency and zero middleman fee.'
    ],
    eligibility: [
      'Small and marginal landholder farmer families with cultivable landholding up to 2 hectares.',
      'Valid Aadhaar and bank account linked with NPCI.',
      'Citizen must not be an institutional landholder or high-income taxpayer.'
    ],
    documents: [
      'Aadhaar card',
      'Land ownership citizenship documents (Khatauni / Jamabandi)',
      'Active bank account passbook with IFSC code'
    ],
    application_process: [
      'Visit the official PM-KISAN portal (pmkisan.gov.in).',
      'Click on Farmers Corner and select New Farmer Registration.',
      'Submit Aadhaar number, state, district, and landholding details for verification.',
      'State nodal officer verifies the land record and approves disbursement.'
    ],
    official_url: 'https://pmkisan.gov.in',
    officialSourceUrl: 'https://pmkisan.gov.in',
    lastUpdated: '2026-10-15',
    priority: 1
  },
  {
    scheme_id: 'sch_ayushman_bharat',
    slug: 'sch-ayushman-bharat',
    name: 'Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana (PM-JAY)',
    schemeName: 'Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana (PM-JAY)',
    schemeShortTitle: 'PM-JAY',
    level: 'Central',
    state: 'Central',
    category: 'Health',
    schemeCategory: ['Health & Wellness', 'Social Welfare'],
    tags: ['health', 'insurance', 'low-income', 'hospitalization', 'central'],
    description: 'National public health insurance fund that aims to provide free access to healthcare for low income earners in the country.',
    briefDescription: 'Cashless health insurance coverage up to Rs. 5 Lakhs per family per year for secondary and tertiary hospitalization.',
    nodalMinistryName: 'Ministry of Health and Family Welfare',
    ministry: 'Ministry of Health and Family Welfare',
    schemeFor: 'Family',
    beneficiaryState: ['All'],
    targetOccupations: ['Daily Wage Earner', 'Farmer', 'Unemployed', 'Contractual Worker', 'Other'],
    maxIncome: 300000,
    benefits: [
      'Cashless and paperless access to healthcare services up to Rs. 5,00,000 per family per year for secondary and tertiary care hospitalization.',
      'Covers pre-existing diseases from day one and includes pre- and post-hospitalization expenses for up to 15 days.'
    ],
    eligibility: [
      'Families identified under the Socio-Economic Caste Census (SECC) 2011 database as deprived rural households and occupational categories of urban workers.',
      'Low income households without an active government employee in the family.'
    ],
    documents: [
      'Aadhaar card or Ration Card',
      'PM-JAY Family ID card / Golden Card',
      'Government issued Photo ID proof'
    ],
    application_process: [
      'Check eligibility online on mera.pmjay.gov.in or visit any empaneled hospital.',
      'Present identity proof to the Ayushman Mitra desk at the empaneled hospital for instant biometric verification.',
      'Receive Ayushman Golden Card and access cashless medical treatments.'
    ],
    official_url: 'https://pmjay.gov.in',
    officialSourceUrl: 'https://pmjay.gov.in',
    lastUpdated: '2026-10-20',
    priority: 1
  },
  {
    scheme_id: 'sch_devnarayan_sc',
    slug: 'sch-devnarayan-sc',
    name: 'Devnarayan Gurukul Yojana',
    schemeName: 'Devnarayan Gurukul Yojana',
    schemeShortTitle: 'Devnarayan Yojana',
    level: 'State',
    state: 'Rajasthan',
    category: 'Education',
    schemeCategory: ['Education & Learning', 'Social Justice'],
    tags: ['education', 'student', 'rajasthan', 'backward-classes', 'scholarship'],
    description: 'Educational scheme in Rajasthan providing free residential schooling in reputed private English medium schools for students from Special Backward Classes.',
    briefDescription: 'Free English-medium residential schooling (Class 6 to 12) for MBC / Special Backward Class students in Rajasthan.',
    nodalMinistryName: 'Department of Social Justice and Empowerment',
    ministry: 'Department of Social Justice and Empowerment',
    schemeFor: 'Individual',
    beneficiaryState: ['Rajasthan'],
    targetOccupations: ['Student'],
    targetCategories: ['OBC', 'MBC', 'SC', 'ST'],
    maxIncome: 250000,
    benefits: [
      'Free quality education from Class 6 to 12 in selected prestigious residential schools, including lodging, boarding, uniforms, and textbooks.',
      'Free coaching support for engineering, medical, and competitive state exams.'
    ],
    eligibility: [
      'Resident of Rajasthan belonging to designated Special Backward Classes (Banjara, Gadia Luhar, Gujjar, Raika, Gadaria).',
      'Family annual income not exceeding Rs. 2.5 Lakhs.',
      'Student must have passed Class 5 with at least 50% marks.'
    ],
    documents: [
      'Rajasthan Domicile Certificate (Bonafide)',
      'Caste Certificate (SBC / MBC / OBC)',
      'Income Certificate of parents',
      'Previous class marksheet and School Transfer Certificate'
    ],
    application_process: [
      'Apply online through Rajasthan SSO portal (sso.rajasthan.gov.in) using SJMS application form.',
      'Appear for the state entrance examination conducted by the Department of Social Justice.',
      'Selected students are allotted seats based on merit ranking.'
    ],
    official_url: 'https://sje.rajasthan.gov.in',
    officialSourceUrl: 'https://sje.rajasthan.gov.in',
    lastUpdated: '2026-10-01',
    priority: 2
  },
  {
    scheme_id: 'sch_pm_awas_yojana',
    slug: 'sch-pm-awas-yojana',
    name: 'Pradhan Mantri Awas Yojana - Gramin (PMAY-G)',
    schemeName: 'Pradhan Mantri Awas Yojana - Gramin (PMAY-G)',
    schemeShortTitle: 'PMAY-G',
    level: 'Central',
    state: 'Central',
    category: 'Housing',
    schemeCategory: ['Housing & Urban Affairs', 'Rural Development'],
    tags: ['housing', 'rural', 'low-income', 'shelter', 'central'],
    description: 'Flagship social welfare programme to provide pucca houses with basic amenities to all houseless households living in kutcha and dilapidated houses.',
    briefDescription: 'Financial aid of Rs. 1.2 Lakh to build a permanent pucca house with toilet and electricity in rural areas.',
    nodalMinistryName: 'Ministry of Rural Development',
    ministry: 'Ministry of Rural Development',
    schemeFor: 'Family',
    beneficiaryState: ['All'],
    targetOccupations: ['Daily Wage Earner', 'Farmer', 'Contractual Worker', 'Unemployed', 'Other'],
    maxIncome: 200000,
    benefits: [
      'Financial assistance of Rs. 1,20,000 in plains and Rs. 1,30,000 in hilly/difficult areas for pucca house construction.',
      'Additional 90/95 person days of unskilled labour under MGNREGS (approx. Rs. 20,000+).',
      'Assistance of Rs. 12,000 for toilet construction under Swachh Bharat Mission.'
    ],
    eligibility: [
      'Houseless families or households living in zero, one or two-room houses with kutcha wall and roof as per SECC 2011 / Awaas+ data.',
      'No pucca house owned anywhere in India by any household member.'
    ],
    documents: [
      'Aadhaar card of all adult family members',
      'Active Bank account passbook',
      'MGNREGA Job Card number',
      'Affidavit of not owning a pucca house'
    ],
    application_process: [
      'Gram Sabha verifies the eligible beneficiary list derived from Awaas+ survey.',
      'Registration completed through Gram Panchayat office or online portal.',
      'Funds transferred directly to bank account in 3 construction milestone stages.'
    ],
    official_url: 'https://pmayg.nic.in',
    officialSourceUrl: 'https://pmayg.nic.in',
    lastUpdated: '2026-09-28',
    priority: 2
  },
  {
    scheme_id: 'sch_post_matric_scholarship',
    slug: 'sch-post-matric-scholarship',
    name: 'Post-Matric Scholarship for SC/ST/OBC Students',
    schemeName: 'Post-Matric Scholarship for SC/ST/OBC Students',
    schemeShortTitle: 'Post-Matric Scholarship',
    level: 'State',
    state: 'Rajasthan',
    category: 'Education',
    schemeCategory: ['Education & Learning', 'Social Welfare'],
    tags: ['scholarship', 'student', 'higher-education', 'rajasthan', 'sc', 'st', 'obc'],
    description: 'Scholarship assistance for students belonging to Scheduled Castes, Scheduled Tribes, and Other Backward Classes studying post-matriculation courses.',
    briefDescription: 'Full tuition fee reimbursement and monthly stipend for SC/ST/OBC college and higher secondary students.',
    nodalMinistryName: 'Social Justice and Empowerment Department',
    ministry: 'Social Justice and Empowerment Department',
    schemeFor: 'Individual',
    beneficiaryState: ['Rajasthan'],
    targetOccupations: ['Student'],
    targetCategories: ['SC', 'ST', 'OBC', 'EWS'],
    maxIncome: 250000,
    benefits: [
      '100% reimbursement of non-refundable tuition and examination fees along with monthly maintenance allowances.',
      'Direct DBT credit to the student bank account.'
    ],
    eligibility: [
      'Bonafide resident of Rajasthan studying in recognized higher secondary schools or colleges.',
      'Annual family income ceiling of Rs. 2,50,000 for SC/ST and Rs. 1,50,000 for OBC.'
    ],
    documents: [
      'Jan Aadhaar Card / Aadhaar Card',
      'Caste Certificate issued by Rajasthan Govt',
      'Income Certificate of parents',
      'Fee receipt of current academic year',
      'Previous class Marksheet'
    ],
    application_process: [
      'Log in to Rajasthan Single Sign On (SSO) portal (sso.rajasthan.gov.in).',
      'Access Scholarship (SJMS) application and fill academic details.',
      'Upload verified fee receipts and submit to institution nodal officer for approval.'
    ],
    official_url: 'https://sje.rajasthan.gov.in',
    officialSourceUrl: 'https://sje.rajasthan.gov.in',
    lastUpdated: '2026-10-10',
    priority: 3
  },
  {
    scheme_id: 'sch_mukhyamantri_chiranjeevi',
    slug: 'sch-mukhyamantri-chiranjeevi',
    name: 'Mukhyamantri Chiranjeevi Swasthya Bima Yojana',
    schemeName: 'Mukhyamantri Chiranjeevi Swasthya Bima Yojana',
    schemeShortTitle: 'Chiranjeevi Bima',
    level: 'State',
    state: 'Rajasthan',
    category: 'Health',
    schemeCategory: ['Health & Wellness'],
    tags: ['health', 'insurance', 'rajasthan', 'medical', 'family'],
    description: 'Universal health insurance scheme for all families residing in Rajasthan covering tertiary and secondary care hospitalization costs.',
    briefDescription: 'Universal health insurance coverage up to Rs. 25 Lakhs per family across government and private hospitals in Rajasthan.',
    nodalMinistryName: 'Department of Medical, Health and Family Welfare',
    ministry: 'Department of Medical, Health and Family Welfare',
    schemeFor: 'Family',
    beneficiaryState: ['Rajasthan'],
    targetOccupations: ['Farmer', 'Daily Wage Earner', 'Self-Employed', 'Student', 'Other'],
    maxIncome: null,
    benefits: [
      'Cashless medical treatment cover up to Rs. 25,00,000 per family per year across empaneled government and private hospitals.',
      'Includes accidental death insurance coverage up to Rs. 5,00,000.'
    ],
    eligibility: [
      'All resident families of Rajasthan possessing a valid Jan Aadhaar card.',
      'Free coverage for NFSA beneficiaries, SECC families, small & marginal farmers, and contractual workers.'
    ],
    documents: [
      'Jan Aadhaar card',
      'Aadhaar card of family members',
      'Mobile number linked to Jan Aadhaar'
    ],
    application_process: [
      'Register at nearest E-Mitra kiosk or online through the Chiranjeevi portal using Jan Aadhaar ID.',
      'Eligible free categories are pre-enrolled; others pay nominal annual premium.',
      'Show Jan Aadhaar card at hospital Chiranjeevi helpdesk during admission.'
    ],
    official_url: 'https://chiranjeevi.rajasthan.gov.in',
    officialSourceUrl: 'https://chiranjeevi.rajasthan.gov.in',
    lastUpdated: '2026-10-25',
    priority: 2
  }
];

export const alerts = [
  {
    id: 'a1',
    title: 'New Scheme Application Window Open',
    message: 'Post-Matric Scholarship portal is now accepting applications for the 2026-27 academic session.',
    schemeSlug: 'sch-post-matric-scholarship',
    createdAt: '2026-11-01',
  },
  {
    id: 'a2',
    title: 'PM-KISAN Installment Update',
    message: 'Next 4-monthly installment DBT disbursement schedule announced for registered farmers.',
    schemeSlug: 'sch-pm-kisan',
    createdAt: '2026-10-28',
  }
];
