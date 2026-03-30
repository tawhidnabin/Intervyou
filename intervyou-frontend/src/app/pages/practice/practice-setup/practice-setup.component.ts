import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ApiService } from '../../../core/api.service';

@Component({
  selector: 'app-practice-setup',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './practice-setup.component.html',
  styleUrls: ['./practice-setup.component.scss']
})
export class PracticeSetupComponent {
  form = this.fb.group({
    job_role: ['', Validators.required],
    level: ['beginner', Validators.required]
  });
  loading = false;
  error = '';

  roles = [
    'Software Engineer', 'Product Manager', 'Data Scientist',
    'Marketing Manager', 'Finance Analyst', 'HR Manager',
    'Sales Executive', 'UX Designer', 'General'
  ];

  levels = [
    {
      id: 'beginner',
      label: 'Beginner',
      emoji: '',
      desc: 'Foundational questions about yourself, strengths and motivations.',
      color: '#059669',
      bg: '#f0fdf4',
      border: '#bbf7d0',
      questions: 'Easy questions'
    },
    {
      id: 'intermediate',
      label: 'Intermediate',
      emoji: '',
      desc: 'Behavioural STAR questions requiring specific examples from experience.',
      color: '#d97706',
      bg: '#fffbeb',
      border: '#fde68a',
      questions: 'Medium questions'
    },
    {
      id: 'master',
      label: 'Master',
      emoji: '',
      desc: 'Senior-level strategic and complex situational questions.',
      color: '#dc2626',
      bg: '#fef2f2',
      border: '#fecaca',
      questions: 'Hard questions'
    }
  ];

  constructor(private fb: FormBuilder, private api: ApiService, private router: Router) {}

  selectLevel(id: string) {
    this.form.patchValue({ level: id });
  }

  start() {
    if (this.form.invalid) return;
    this.loading = true;
    const { job_role, level } = this.form.value;
    this.api.startSession(job_role!, level!).subscribe({
      next: res => this.router.navigate(['/practice', res.session_id], { queryParams: { level } }),
      error: () => { this.error = 'Failed to start session. Please try again.'; this.loading = false; }
    });
  }
}
