// Citizen profile and personalization service
// Manages local storage persistence, demo user profiles, and scheme matching rules.

const PROFILE_KEY = 'adhikar_setu_profile';
const USER_KEY = 'adhikar_setu_user';

export const DEMO_PROFILES = [
  {
    profile_id: 'prof_farmer_rj',
    name: 'Ramesh Kumar',
    age: 46,
    gender: 'Male',
    state: 'Rajasthan',
    district: 'Jaipur',
    income: 140000,
    occupation: 'Farmer',
    category: 'OBC',
    disability_status: 'No',
    qualification: '10th Pass'
  },
  {
    profile_id: 'prof_student_rj',
    name: 'Pooja Sharma',
    age: 20,
    gender: 'Female',
    state: 'Rajasthan',
    district: 'Kota',
    income: 180000,
    occupation: 'Student',
    category: 'SC',
    disability_status: 'No',
    qualification: '12th Pass'
  },
  {
    profile_id: 'prof_rural_rj',
    name: 'Sunita Devi',
    age: 38,
    gender: 'Female',
    state: 'Rajasthan',
    district: 'Jodhpur',
    income: 90000,
    occupation: 'Daily Wage Earner',
    category: 'ST',
    disability_status: 'No',
    qualification: 'Below 10th'
  }
];

export function getStoredUser() {
  try {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function saveStoredUser(user) {
  try {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
    window.dispatchEvent(new Event('auth-change'));
  } catch (err) {
    console.error('Failed to save user session', err);
  }
}

export function logoutUser() {
  try {
    localStorage.removeItem(USER_KEY);
    window.dispatchEvent(new Event('auth-change'));
  } catch (err) {
    console.error('Failed to clear user session', err);
  }
}

export function getStoredProfile() {
  try {
    const raw = localStorage.getItem(PROFILE_KEY);
    if (raw) return JSON.parse(raw);
    return null;
  } catch {
    return null;
  }
}

export function saveStoredProfile(profile) {
  try {
    const enriched = {
      ...profile,
      profile_id: profile.profile_id || `prof_${Date.now().toString(36)}`,
      updated_at: new Date().toISOString()
    };
    localStorage.setItem(PROFILE_KEY, JSON.stringify(enriched));
    // Also save simple user session if not logged in
    const currentUser = getStoredUser();
    if (!currentUser) {
      saveStoredUser({
        name: enriched.name,
        phone: '9876543210',
        loggedInAt: new Date().toISOString()
      });
    }
    window.dispatchEvent(new Event('profile-change'));
    return enriched;
  } catch (err) {
    console.error('Failed to save citizen profile', err);
    return profile;
  }
}

/**
 * Evaluates whether a scheme matches a citizen's profile.
 * Returns an object: { isMatch: boolean, score: number, reasons: string[] }
 */
export function calculateSchemeMatch(scheme, profile) {
  if (!profile) {
    return { isMatch: true, score: 0, reasons: [] };
  }

  const reasons = [];
  let score = 0;

  // 1. State match
  const schemeState = (scheme.state || (scheme.beneficiaryState && scheme.beneficiaryState[0]) || '').toLowerCase();
  const profileState = (profile.state || '').toLowerCase();

  if (schemeState === 'central' || schemeState === 'all' || !schemeState) {
    reasons.push('Central Government Scheme available nationwide');
    score += 1;
  } else if (schemeState === profileState) {
    reasons.push(`State Government Scheme for ${profile.state} residents`);
    score += 3;
  }

  // 2. Occupation match
  const profileOcc = (profile.occupation || '').toLowerCase();
  const targetOccs = (scheme.targetOccupations || []).map((o) => o.toLowerCase());
  const tags = (scheme.tags || []).map((t) => t.toLowerCase());

  if (targetOccs.includes(profileOcc) || tags.includes(profileOcc)) {
    reasons.push(`Tailored for your occupation: ${profile.occupation}`);
    score += 4;
  } else if (profileOcc === 'farmer' && (tags.includes('agriculture') || scheme.category === 'Agriculture')) {
    reasons.push('Matches your agriculture / farming background');
    score += 4;
  } else if (profileOcc === 'student' && (tags.includes('education') || tags.includes('scholarship') || scheme.category === 'Education')) {
    reasons.push('Designed for students & education assistance');
    score += 4;
  }

  // 3. Category match
  const profileCat = profile.category;
  const targetCats = scheme.targetCategories || [];
  if (targetCats.length > 0) {
    if (targetCats.includes(profileCat)) {
      reasons.push(`Special provisions for ${profileCat} category`);
      score += 3;
    }
  }

  // 4. Income ceiling check
  const profileIncome = Number(profile.income) || 0;
  if (scheme.maxIncome) {
    if (profileIncome <= scheme.maxIncome) {
      reasons.push(`Annual income under the ₹${(scheme.maxIncome / 100000).toFixed(1)}L ceiling`);
      score += 2;
    }
  }

  return {
    isMatch: score > 0,
    score,
    reasons
  };
}
