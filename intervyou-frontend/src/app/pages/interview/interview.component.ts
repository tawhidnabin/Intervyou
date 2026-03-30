import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatChipsModule } from '@angular/material/chips';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatIconModule } from '@angular/material/icon';
import { AudioRecorderComponent } from '../../shared/components/audio-recorder/audio-recorder.component';
import { ScoreCardComponent } from '../../shared/components/score-card/score-card.component';
import { ApiService } from '../../core/api.service';

type State = 'loading' | 'ready' | 'recording' | 'processing' | 'feedback' | 'done';

@Component({
  selector: 'app-interview',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatButtonModule, MatProgressSpinnerModule,
    MatProgressBarModule, MatChipsModule, MatSnackBarModule, MatIconModule,
    AudioRecorderComponent, ScoreCardComponent],
  templateUrl: './interview.component.html',
  styleUrls: ['./interview.component.scss']
})
export class InterviewComponent implements OnInit {
  state: State = 'loading';
  questions: any[] = [];
  currentIndex = 0;
  sessionId: number | null = null;
  lastResult: any = null;
  error = '';

  constructor(private api: ApiService, private router: Router, private snack: MatSnackBar) {}

  ngOnInit() {
    this.api.startSession('General').subscribe({
      next: res => {
        this.sessionId = res.session_id;
        this.api.getQuestions().subscribe({
          next: qs => { this.questions = qs; this.state = 'ready'; },
          error: () => this.showError('Failed to load questions.')
        });
      },
      error: () => this.showError('Failed to start session.')
    });
  }

  get currentQuestion() { return this.questions[this.currentIndex]; }
  get progress() { return this.questions.length ? ((this.currentIndex) / this.questions.length) * 100 : 0; }

  onAudioBlob(blob: Blob) {
    if (!this.sessionId || !this.currentQuestion) return;
    this.state = 'processing';
    const fd = new FormData();
    fd.append('audio', blob, 'recording.webm');
    fd.append('session_id', String(this.sessionId));
    fd.append('question_id', String(this.currentQuestion.id));

    this.api.submitAudio(fd).subscribe({
      next: res => { this.lastResult = res; this.state = 'feedback'; },
      error: err => {
        this.showError(err.error?.error || 'Analysis failed. Please try again.');
        this.state = 'ready';
      }
    });
  }

  nextQuestion() {
    if (this.currentIndex < this.questions.length - 1) {
      this.currentIndex++;
      this.lastResult = null;
      this.state = 'ready';
    } else {
      this.state = 'done';
      this.api.completeSession(this.sessionId!).subscribe({
        next: () => this.router.navigate(['/history']),
        error: () => this.router.navigate(['/history'])
      });
    }
  }

  private showError(msg: string) {
    this.error = msg;
    this.snack.open(msg, 'Dismiss', { duration: 5000 });
    this.state = 'ready';
  }
}
