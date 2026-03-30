import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { AuthService } from './auth.service';

export const jwtInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(AuthService);
  const token = auth.getToken();

  // Don't attach token to auth endpoints (login, register, etc.)
  const isAuthEndpoint = req.url.includes('/api/auth/');
  const authReq = (token && !isAuthEndpoint)
    ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
    : token
      ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
      : req;

  return next(authReq).pipe(
    catchError(err => {
      // Only auto-logout on 401 for non-auth endpoints to prevent loops
      if (err.status === 401 && !req.url.includes('/api/auth/')) {
        auth.silentLogout();
      }
      return throwError(() => err);
    })
  );
};
