const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function request(path, options = {}) {
 const token = window.localStorage.getItem('gem_access_token');
 let response;
 try {
  response = await fetch(`${API_URL}${path}`, {
   ...options,
   headers: {
    'Content-Type': 'application/json',
    ...(token ? {Authorization: `Bearer ${token}`} : {}),
    ...(options.headers || {})
   }
  });
 } catch (error) {
  throw new Error(`Backend unavailable at ${API_URL}. Start the FastAPI server and try again.`);
 }
 if (!response.ok) {
  let message = `Request failed (${response.status})`;
  try { message = (await response.json()).detail || message; } catch (e) {}
  throw new Error(message);
 }
 return response.status === 204 ? null : response.json();
}

export function login(email, password) {
 return request('/auth/login', {method: 'POST', body: JSON.stringify({email, password})});
}

export function register(name, email, password) {
 return request('/auth/register', {
  method: 'POST',
  body: JSON.stringify({name, email, password})
 });
}

export function getTenders() { return request('/tenders/'); }
export function getBidders() { return request('/bidders/'); }
export function getBids() { return request('/bids/'); }
export function getDocuments() { return request('/documents/'); }
export function getRequirements() { return request('/compliance-requirements/'); }
export function getAnalyses() { return request('/compliance-analyses/'); }

export async function uploadTenderDocument(tenderId, file) {
 const token = window.localStorage.getItem('gem_access_token');
 const formData = new FormData();
 formData.append('file', file);
 const response = await fetch(`${API_URL}/documents/upload-tender?tender_id=${encodeURIComponent(tenderId)}`, {method: 'POST', headers: token ? {Authorization: `Bearer ${token}`} : {}, body: formData});
 if (!response.ok) throw new Error((await response.json()).detail || `Tender upload failed (${response.status})`);
 return response.json();
}

export async function importTenderDocument(file) {
 const token = window.localStorage.getItem('gem_access_token');
 const formData = new FormData();
 formData.append('file', file);
 const response = await fetch(`${API_URL}/documents/import-tender`, {method: 'POST', headers: token ? {Authorization: `Bearer ${token}`} : {}, body: formData});
 if (!response.ok) throw new Error((await response.json()).detail || `Tender import failed (${response.status})`);
 return response.json();
}

export async function uploadBidDocument(tenderId, companyName, file, bidNumber) {
 const token = window.localStorage.getItem('gem_access_token');
 const formData = new FormData();
 formData.append('file', file);
 const tenderQuery = tenderId ? `tender_id=${encodeURIComponent(tenderId)}` : `bid_number=${encodeURIComponent(bidNumber)}`;
 let response;
 try {
  response = await fetch(`${API_URL}/documents/upload-bid?${tenderQuery}&company_name=${encodeURIComponent(companyName)}`, {method: 'POST', headers: token ? {Authorization: `Bearer ${token}`} : {}, body: formData});
 } catch (error) {
  throw new Error(`Backend unavailable at ${API_URL}. Please start FastAPI and try again.`);
 }
 if (!response.ok) {
  let message = `Bid upload failed (${response.status})`;
  try { message = (await response.json()).detail || message; } catch (e) {}
  throw new Error(message);
 }
 return response.json();
}

export async function uploadTenderBid(tenderId, file, bidNumber) {
 const token = window.localStorage.getItem('gem_access_token');
 const formData = new FormData();
 formData.append('file', file);
 formData.append('document_type', 'bid');
 const tenderQuery = tenderId ? `tender_id=${encodeURIComponent(tenderId)}` : `bid_number=${encodeURIComponent(bidNumber)}`;
 const response = await fetch(`${API_URL}/documents/upload?${tenderQuery}&document_type=bid`, {
  method: 'POST',
  headers: token ? {Authorization: `Bearer ${token}`} : {},
  body: formData
 });
 if (!response.ok) {
  let message = `Upload failed (${response.status})`;
  try { message = (await response.json()).detail || message; } catch (e) {}
  throw new Error(message);
 }
 return response.json();
}

export function clearSession() { window.localStorage.removeItem('gem_access_token'); }