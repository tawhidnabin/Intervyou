import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-score-card',
  standalone: true,
  imports: [CommonModule, MatCardModule],
  template: `
    <mat-card class="score-card" [ngClass]="colorClass">
      <mat-card-content>
        <div class="score-value">{{ score }}</div>
        <div class="score-label">{{ label }}</div>
        <div class="score-bar">
          <div class="score-fill" [style.width.%]="score"></div>
        </div>
        <div class="score-desc" *ngIf="description">{{ description }}</div>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .score-card { text-align:center; padding:8px; min-width:120px; }
    .score-value { font-size:36px; font-weight:700; }
    .score-label { font-size:12px; color:#666; text-transform:uppercase; letter-spacing:1px; }
    .score-bar { height:4px; background:#e0e0e0; border-radius:2px; margin:8px 0 4px; }
    .score-fill { height:100%; border-radius:2px; transition:width 0.5s; }
    .score-desc { font-size:11px; color:#888; }
    .green .score-value { color:#4caf50; }
    .green .score-fill { background:#4caf50; }
    .amber .score-value { color:#ff9800; }
    .amber .score-fill { background:#ff9800; }
    .red .score-value { color:#f44336; }
    .red .score-fill { background:#f44336; }
  `]
})
export class ScoreCardComponent {
  @Input() label = '';
  @Input() score = 0;
  @Input() description = '';

  get colorClass(): string {
    if (this.score >= 70) return 'green';
    if (this.score >= 40) return 'amber';
    return 'red';
  }
}
