import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Router } from '@angular/router';

const API = 'http://localhost:5000/api/auth';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private _currentUser$ = new BehaviorSubject<any>(this._loadUser());
  currentUser$ = this._currentUser$.asObservable();

  constructor(private http: HttpClient, private router: Router) {}

  private _loadUser(): any {
    const u = localStorage.getItem('user');
    return u ? JSON.parse(u) : null;
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  login(email: string, password: string): Observable<any> {
    return this.http.post<any>(`${API}/login`, { email, password }).pipe(
      tap(res => this._store(res))
    );
  }

  register(name: string, email: string, password: string): Observable<any> {
    return this.http.post<any>(`${API}/register`, { name, email, password }).pipe(
      tap(res => this._store(res))
    );
  }

  refreshToken(): Observable<any> {
    const refreshToken = localStorage.getItem('refresh_token');
    return this.http.post<any>(`${API}/refresh`, {}, {
      headers: { Authorization: `Bearer ${refreshToken}` }
    }).pipe(
      tap(res => localStorage.setItem('token', res.token))
    );
  }

  verifyEmail(token: string): Observable<any> {
    return this.http.post<any>(`${API}/verify-email`, { token }).pipe(
      tap(res => {
        if (res.user) {
          localStorage.setItem('user', JSON.stringify(res.user));
          this._currentUser$.next(res.user);
        }
      })
    );
  }

  resendVerification(): Observable<any> {
    return this.http.post<any>(`${API}/resend-verification`, {});
  }

  forgotPassword(email: string): Observable<any> {
    return this.http.post<any>(`${API}/forgot-password`, { email });
  }

  resetPassword(token: string, newPassword: string): Observable<any> {
    return this.http.post<any>(`${API}/reset-password`, { token, new_password: newPassword });
  }

  logout(): void {
    // Try to revoke token on backend, but don't block on failure
    const token = this.getToken();
    this._clearStorage();
    if (token) {
      this.http.post(`${API}/logout`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      }).subscribe({ error: () => {} });
    }
    this.router.navigate(['/auth/signin']);
  }

  silentLogout(): void {
    // Clear storage without calling backend (used by interceptor to prevent loops)
    this._clearStorage();
    this.router.navigate(['/auth/signin']);
  }

  private _store(res: any): void {
    localStorage.setItem('token', res.token);
    if (res.refresh_token) {
      localStorage.setItem('refresh_token', res.refresh_token);
    }
    localStorage.setItem('user', JSON.stringify(res.user));
    this._currentUser$.next(res.user);
  }

  private _clearStorage(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    this._currentUser$.next(null);
  }
}
