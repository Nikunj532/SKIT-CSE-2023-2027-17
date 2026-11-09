import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { t } from '../i18n';
import {
  getStoredProfile,
  saveStoredProfile,
  DEMO_PROFILES
} from '../services/profile';

/**
 * Citizen Profile Setup page (Sprint 2).
 * Collects demographic and socio-economic parameters used to determine scheme eligibility.
 */
export default function ProfileSetup() {
  const navigate = useNavigate();
  const [success, setSuccess] = useState(false);
  const [formData, setFormData] = useState(() => {
    const existing = getStoredProfile();
    if (existing) {
      return {
        name: existing.name || '',
        age: existing.age ?? '',
        gender: existing.gender || 'Male',
        state: existing.state || 'Rajasthan',
        district: existing.district || '',
        income: existing.income ?? '',
        occupation: existing.occupation || 'Farmer',
        category: existing.category || 'General',
        disability_status: existing.disability_status || 'No',
        qualification: existing.qualification || '10th Pass'
      };
    }
    return {
      name: '',
      age: '',
      gender: 'Male',
      state: 'Rajasthan',
      district: 'Jaipur',
      income: '',
      occupation: 'Farmer',
      category: 'OBC',
      disability_status: 'No',
      qualification: '10th Pass'
    };
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleApplyDemo = (demo) => {
    setFormData({
      name: demo.name,
      age: demo.age,
      gender: demo.gender,
      state: demo.state,
      district: demo.district,
      income: demo.income,
      occupation: demo.occupation,
      category: demo.category,
      disability_status: demo.disability_status,
      qualification: demo.qualification
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const payload = {
      ...formData,
      age: Number(formData.age) || 0,
      income: Number(formData.income) || 0
    };

    saveStoredProfile(payload);
    setSuccess(true);

    setTimeout(() => {
      navigate('/dashboard');
    }, 800);
  };

  return (
    <div className="container" style={{ maxWidth: '780px' }}>
      <div className="card">
        <h1>{t('profile.title')}</h1>
        <p className="muted">{t('profile.subtitle')}</p>

        {success && (
          <div className="notice notice--success" role="status">
            <p><strong>✓ {t('profile.successMsg')}</strong></p>
          </div>
        )}

        <div style={{ background: '#f8fafc', padding: '12px', borderRadius: '8px', marginBottom: '16px' }}>
          <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#334155' }}>
            ⚡ {t('profile.quickFill')}:
          </span>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '6px' }}>
            {DEMO_PROFILES.map((p) => (
              <button
                key={p.profile_id}
                type="button"
                className="btn btn--sm btn--secondary"
                onClick={() => handleApplyDemo(p)}
              >
                {p.name} ({p.occupation})
              </button>
            ))}
          </div>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group form-grid--full">
              <label htmlFor="name" className="form-label">{t('profile.name')} *</label>
              <input
                id="name"
                name="name"
                type="text"
                required
                className="form-input"
                placeholder="e.g. Ramesh Kumar"
                value={formData.name}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="age" className="form-label">{t('profile.age')} *</label>
              <input
                id="age"
                name="age"
                type="number"
                min="1"
                max="120"
                required
                className="form-input"
                placeholder="e.g. 35"
                value={formData.age}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="gender" className="form-label">{t('profile.gender')} *</label>
              <select
                id="gender"
                name="gender"
                className="form-select"
                value={formData.gender}
                onChange={handleChange}
              >
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Transgender">Transgender</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="state" className="form-label">{t('profile.state')} *</label>
              <select
                id="state"
                name="state"
                className="form-select"
                value={formData.state}
                onChange={handleChange}
              >
                <option value="Rajasthan">Rajasthan</option>
                <option value="Delhi">Delhi</option>
                <option value="Uttar Pradesh">Uttar Pradesh</option>
                <option value="Bihar">Bihar</option>
                <option value="Madhya Pradesh">Madhya Pradesh</option>
                <option value="Gujarat">Gujarat</option>
                <option value="Haryana">Haryana</option>
                <option value="Punjab">Punjab</option>
                <option value="Maharashtra">Maharashtra</option>
                <option value="Other">Other State</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="district" className="form-label">{t('profile.district')} *</label>
              <input
                id="district"
                name="district"
                type="text"
                required
                className="form-input"
                placeholder="e.g. Jaipur"
                value={formData.district}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="income" className="form-label">{t('profile.income')} *</label>
              <input
                id="income"
                name="income"
                type="number"
                min="0"
                step="5000"
                required
                className="form-input"
                placeholder="e.g. 150000"
                value={formData.income}
                onChange={handleChange}
              />
              <span className="form-hint">Used to evaluate income ceiling for scholarships & benefits.</span>
            </div>

            <div className="form-group">
              <label htmlFor="occupation" className="form-label">{t('profile.occupation')} *</label>
              <select
                id="occupation"
                name="occupation"
                className="form-select"
                value={formData.occupation}
                onChange={handleChange}
              >
                <option value="Farmer">Farmer / Agriculture</option>
                <option value="Student">Student</option>
                <option value="Daily Wage Earner">Daily Wage Earner / Laborer</option>
                <option value="Self-Employed">Self-Employed / Small Business</option>
                <option value="Contractual Worker">Contractual Worker</option>
                <option value="Private Employee">Private Employee</option>
                <option value="Government Employee">Government Employee</option>
                <option value="Unemployed">Unemployed</option>
                <option value="Homemaker">Homemaker</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="category" className="form-label">{t('profile.category')} *</label>
              <select
                id="category"
                name="category"
                className="form-select"
                value={formData.category}
                onChange={handleChange}
              >
                <option value="General">General</option>
                <option value="OBC">OBC (Other Backward Classes)</option>
                <option value="SC">SC (Scheduled Caste)</option>
                <option value="ST">ST (Scheduled Tribe)</option>
                <option value="EWS">EWS (Economically Weaker Section)</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="disability_status" className="form-label">{t('profile.disability')} *</label>
              <select
                id="disability_status"
                name="disability_status"
                className="form-select"
                value={formData.disability_status}
                onChange={handleChange}
              >
                <option value="No">No</option>
                <option value="Yes">Yes</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="qualification" className="form-label">{t('profile.qualification')}</label>
              <select
                id="qualification"
                name="qualification"
                className="form-select"
                value={formData.qualification}
                onChange={handleChange}
              >
                <option value="Below 10th">Below 10th</option>
                <option value="10th Pass">10th Pass</option>
                <option value="12th Pass">12th Pass</option>
                <option value="Diploma">Diploma / ITI</option>
                <option value="Graduate">Graduate (B.A., B.Sc., B.Tech, etc.)</option>
                <option value="Post Graduate">Post Graduate (M.A., M.Sc., M.Tech, etc.)</option>
                <option value="Doctorate">Doctorate / Ph.D.</option>
              </select>
            </div>
          </div>

          <div className="form-actions">
            <button type="submit" className="btn">
              {t('profile.saveButton')}
            </button>
            <button
              type="button"
              className="btn btn--ghost"
              onClick={() => navigate('/dashboard')}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
