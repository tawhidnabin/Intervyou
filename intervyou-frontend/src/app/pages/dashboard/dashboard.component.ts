import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { AuthService } from '../../core/auth.service';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  user: any = null;
  stats = { sessions_count: 0, avg_score: 0, completed_count: 0 };
  recentSessions: any[] = [];
  loading = true;

  quickActions: { svg: SafeHtml; label: string; route: string; color: string }[];

  constructor(private auth: AuthService, private api: ApiService, private sanitizer: DomSanitizer) {
    this.quickActions = [
      { svg: this.safe('<path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/>'), label: 'Start Practice', route: '/practice', color: '#4f46e5' },
      { svg: this.safe('<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>'), label: 'View History', route: '/history', color: '#059669' },
      { svg: this.safe('<circle cx="12" cy="8" r="4"/><path d="M20 21a8 8 0 1 0-16 0"/>'), label: 'Settings', route: '/settings', color: '#64748b' },
    ];
  }

  ngOnInit() {
    this.auth.currentUser$.subscribe(u => this.user = u);
    this.api.getDashboardStats().subscribe({
      next: s => { this.stats = s; this.loading = false; },
      error: () => { this.loading = false; }
    });
    this.api.getSessions().subscribe({
      next: sessions => this.recentSessions = sessions.slice(0, 5),
      error: () => {}
    });
  }

  private safe(html: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(html);
  }

  getScoreClass(score: number): string {
    if (score >= 70) return 'score-green';
    if (score >= 40) return 'score-amber';
    return 'score-red';
  }
}
