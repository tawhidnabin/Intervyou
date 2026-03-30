import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { NgChartsModule } from 'ng2-charts';
import { ChartData, ChartOptions } from 'chart.js';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule, RouterLink, NgChartsModule],
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss']
})
export class HistoryComponent implements OnInit {
  sessions: any[] = [];
  loading = true;

  lineData: ChartData<'line'> = { labels: [], datasets: [] };
  lineOptions: ChartOptions<'line'> = {
    responsive: true,
    scales: { y: { min: 0, max: 100, title: { display: true, text: 'Score' } } },
    plugins: { legend: { display: false } }
  };

  constructor(private api: ApiService, private router: Router) {}

  ngOnInit() {
    this.api.getSessions().subscribe({
      next: s => { this.sessions = s; this.buildChart(s); this.loading = false; },
      error: () => { this.loading = false; }
    });
  }

  private buildChart(sessions: any[]) {
    const completed = sessions.filter(s => s.overall_score != null).reverse();
    this.lineData = {
      labels: completed.map(s => new Date(s.started_at).toLocaleDateString()),
      datasets: [{ data: completed.map(s => s.overall_score), borderColor: '#4f46e5', backgroundColor: 'rgba(79,70,229,0.08)', fill: true, tension: 0.3, pointRadius: 5, pointBackgroundColor: '#4f46e5' }]
    };
  }

  scoreColor(s: number) { return s >= 70 ? 'score-green' : s >= 40 ? 'score-amber' : 'score-red'; }
  view(id: number) { this.router.navigate(['/practice', id, 'results']); }
}
