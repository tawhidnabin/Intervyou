import { Routes } from '@angular/router';
import { authGuard } from './core/auth.guard';

export const routes: Routes = [
  { path: '', loadComponent: () => import('./pages/home/home.component').then(m => m.HomeComponent) },
  { path: 'auth/signin', loadComponent: () => import('./pages/auth/signin/signin.component').then(m => m.SigninComponent) },
  { path: 'auth/signup', loadComponent: () => import('./pages/auth/signup/signup.component').then(m => m.SignupComponent) },
  { path: 'contact', loadComponent: () => import('./pages/contact/contact.component').then(m => m.ContactComponent) },
  { path: 'dashboard', loadComponent: () => import('./pages/dashboard/dashboard.component').then(m => m.DashboardComponent), canActivate: [authGuard] },
  { path: 'practice', loadComponent: () => import('./pages/practice/practice-setup/practice-setup.component').then(m => m.PracticeSetupComponent), canActivate: [authGuard] },
  { path: 'practice/:sessionId', loadComponent: () => import('./pages/practice/practice-session/practice-session.component').then(m => m.PracticeSessionComponent), canActivate: [authGuard] },
  { path: 'practice/:sessionId/results', loadComponent: () => import('./pages/practice/practice-results/practice-results.component').then(m => m.PracticeResultsComponent), canActivate: [authGuard] },
  { path: 'history', loadComponent: () => import('./pages/history/history.component').then(m => m.HistoryComponent), canActivate: [authGuard] },
  { path: 'settings', loadComponent: () => import('./pages/settings/settings.component').then(m => m.SettingsComponent), canActivate: [authGuard] },
  // legacy redirects
  { path: 'login', redirectTo: 'auth/signin', pathMatch: 'full' },
  { path: 'register', redirectTo: 'auth/signup', pathMatch: 'full' },
  { path: '**', redirectTo: '' }
];
