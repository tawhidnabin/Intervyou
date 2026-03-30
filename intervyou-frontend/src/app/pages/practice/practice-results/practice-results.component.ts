import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { NgChartsModule } from 'ng2-charts';
import { ChartData, ChartOptions } from 'chart.js';
import { ApiService } from '../../../core/api.service';

@Component({
  selector: 'app-practice-results',
  standalone: true,
  imports: [CommonModule, RouterLink, NgChartsModule],
  templateUrl: './practice-results.component.html',
  styleUrls: ['./practice-results.component.scss']
})
export class PracticeResultsComponent implements OnInit {
  session: any = null;
  loading = true;
  error = '';
  expandedIndex = -1;

  radarData: ChartData<'radar'> = { labels: [], datasets: [] };
  radarOptions: ChartOptions<'radar'> = {
    scales: { r: { min: 0, max: 100, ticks: { stepSize: 25, font: { size: 10 } } } },
    plugins: { legend: { display: false } }
  };

  constructor(private route: ActivatedRoute, private api: ApiService) {}

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('sessionId'));
    this.api.getSession(id).subscribe({
      next: s => { this.session = s; this.buildChart(s.responses); this.loading = false; },
      error: () => { this.error = 'Failed to load results.'; this.loading = false; }
    });
  }

  private buildChart(responses: any[]) {
    if (!responses?.length) return;
    const avg = (key: string, mult = 1) => {
      const vals = responses.map(r => (r[key] ?? 0) * mult);
      return Math.round(vals.reduce((a, b) => a + b, 0) / vals.length);
    };
    this.radarData = {
      labels: ['Fluency', 'Relevance', 'Delivery', 'Overall'],
      datasets: [{
        data: [avg('fluency_score', 100), avg('relevance_score', 100), avg('fluency_score', 100), avg('overall_score')],
        backgroundColor: 'rgba(79,70,229,0.15)',
        borderColor: '#4f46e5',
        pointBackgroundColor: '#4f46e5',
        pointRadius: 4
      }]
    };
  }

  pct(val: number) { return Math.round(val * 100); }
  scoreColor(s: number) { return s >= 70 ? '#059669' : s >= 40 ? '#d97706' : '#dc2626'; }
}
