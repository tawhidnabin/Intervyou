import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatChipsModule } from '@angular/material/chips';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { NgChartsModule } from 'ng2-charts';
import { ChartData, ChartOptions } from 'chart.js';
import { ApiService } from '../../core/api.service';
import { ScoreCardComponent } from '../../shared/components/score-card/score-card.component';

@Component({
  selector: 'app-feedback',
  standalone: true,
  imports: [CommonModule, RouterLink, MatCardModule, MatTabsModule, MatExpansionModule,
    MatChipsModule, MatButtonModule, MatProgressSpinnerModule, MatIconModule,
    NgChartsModule, ScoreCardComponent],
  templateUrl: './feedback.component.html',
  styleUrls: ['./feedback.component.scss']
})
export class FeedbackComponent implements OnInit {
  session: any = null;
  loading = true;
  error = '';

  radarData: ChartData<'radar'> = { labels: [], datasets: [] };
  radarOptions: ChartOptions<'radar'> = {
    scales: { r: { min: 0, max: 100, ticks: { stepSize: 20 } } },
    plugins: { legend: { display: false } }
  };

  constructor(private route: ActivatedRoute, private api: ApiService) {}

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.api.getSession(id).subscribe({
      next: s => {
        this.session = s;
        this.buildChart(s.responses);
        this.loading = false;
      },
      error: () => { this.error = 'Failed to load session.'; this.loading = false; }
    });
  }

  private buildChart(responses: any[]) {
    if (!responses?.length) return;
    const avg = (key: string) => {
      const vals = responses.map(r => (r[key] ?? 0) * (key === 'overall_score' ? 1 : 100));
      return Math.round(vals.reduce((a, b) => a + b, 0) / vals.length);
    };
    this.radarData = {
      labels: ['Fluency', 'Relevance', 'Delivery', 'Overall'],
      datasets: [{
        data: [
          avg('fluency_score'),
          avg('relevance_score'),
          avg('fluency_score'),
          avg('overall_score')
        ],
        backgroundColor: 'rgba(63,81,181,0.2)',
        borderColor: '#3f51b5',
        pointBackgroundColor: '#3f51b5'
      }]
    };
  }

  scoreToPercent(val: number, isRaw = false): number {
    return isRaw ? Math.round(val) : Math.round(val * 100);
  }
}
