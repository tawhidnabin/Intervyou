import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  companies = ['Google', 'Amazon', 'Microsoft', 'Meta', 'Apple', 'Netflix'];

  features: { title: string; svgPath: SafeHtml; desc: string }[];

  constructor(private sanitizer: DomSanitizer) {
    this.features = [
      { title: 'AI-Powered Practice', svgPath: this.safe('<path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/>'), desc: 'Answer real interview questions and get instant AI feedback on your responses.' },
      { title: 'Detailed Analytics', svgPath: this.safe('<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>'), desc: 'Track fluency, relevance, speaking rate and filler words across every session.' },
      { title: 'Smart NLP Scoring', svgPath: this.safe('<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'), desc: 'Sentence-BERT NLP scores how relevant your answers are to ideal responses.' },
      { title: 'Targeted Feedback', svgPath: this.safe('<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>'), desc: 'Get specific, actionable feedback to improve with every practice session.' },
      { title: 'Progress Tracking', svgPath: this.safe('<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>'), desc: 'Visualise your improvement over time with score history charts.' },
      { title: 'Private & Secure', svgPath: this.safe('<rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>'), desc: 'Your sessions and recordings are private and stored securely.' },
    ];
  }

  private safe(html: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(html);
  }
}
