const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function request(path, options = {}) {
 const token = window.localStorage.getItem('gem_access_token');
 const response = await fetch(`${API_URL}${path}`, {
  ...options,
  headers: {
   'Content-Type': 'application/json',
   ...(token ? {Authorization: `Bearer ${token}`} : {}),
   ...(options.headers || {})
  }
 });
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
export function clearSession() { window.localStorage.removeItem('gem_access_token'); }