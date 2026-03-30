import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink, RouterOutlet, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { AuthService } from './core/auth.service';
import { ChatbotComponent } from './shared/components/chatbot/chatbot.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, ChatbotComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  user$ = this.auth.currentUser$;
  mobileOpen = false;
  currentUrl = '';

  constructor(public auth: AuthService, private router: Router) {
    this.router.events.pipe(filter(e => e instanceof NavigationEnd))
      .subscribe((e: any) => { this.currentUrl = e.url; this.mobileOpen = false; });
  }

  get isAuthPage(): boolean {
    return false; // navbar shows on ALL pages
  }

  get isPublicPage(): boolean {
    return this.currentUrl === '/' || this.currentUrl === '' || this.currentUrl.startsWith('/contact');
  }

  logout() { this.auth.logout(); }
}
