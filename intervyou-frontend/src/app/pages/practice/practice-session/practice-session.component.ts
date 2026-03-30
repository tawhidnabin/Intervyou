import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../../../core/api.service';
import { AudioRecorderComponent } from '../../../shared/components/audio-recorder/audio-recorder.component';

type State = 'loading' | 'ready' | 'processing' | 'feedback' | 'done';
type InputMode = 'voice' | 'text';

@Component({
  selector: 'app-practice-session',
  standalone: true,
  imports: [CommonModule, FormsModule, AudioRecorderComponent],
  templateUrl: './practice-session.component.html',
  styleUrls: ['./practice-session.component.scss']
})
export class PracticeSessionComponent implements OnInit, OnDestroy {
  state: State = 'loading';
  inputMode: InputMode = 'voice';
  questions: any[] = [];
  currentIndex = 0;
  sessionId!: number;
  level = 'beginner';
  lastResult: any = null;
  aiAnalysis: string | null = null;
  aiAnalysisLoading = false;
  error = '';
  textAnswer = '';
  processingStep = 0;
  private dotsInterval: any;
  private aiPollInterval: any;

  levelConfig: Record<string, { label: string; color: string; bg: string }> = {
    beginner:     { label: 'Beginner',     color: '#059669', bg: '#f0fdf4' },
    intermediate: { label: 'Intermediate', color: '#d97706', bg: '#fffbeb' },
    master:       { label: 'Master',       color: '#dc2626', bg: '#fef2f2' }
  };

  processingSteps = ['Scoring relevance...', 'Analysing content...', 'Generating feedback...'];
  processingStepsVoice = ['Transcribing audio...', 'Analysing delivery...', 'Scoring relevance...', 'Generating feedback...'];

  constructor(private route: ActivatedRoute, private api: ApiService, private router: Router) {}

  ngOnInit() {
    this.sessionId = Number(this.route.snapshot.paramMap.get('sessionId'));
    this.level = this.route.snapshot.queryParamMap.get('level') || 'beginner';
    this.api.getQuestions(this.level).subscribe({
      next: qs => { this.questions = qs; this.state = 'ready'; },
      error: () => { this.error = 'Failed to load questions.'; this.state = 'ready'; }
    });
  }

  ngOnDestroy() { clearInterval(this.dotsInterval); clearInterval(this.aiPollInterval); }

  get currentQuestion() { return this.questions[this.currentIndex]; }
  get progress() { return this.questions.length ? ((this.currentIndex) / this.questions.length) * 100 : 0; }
  get levelInfo() { return this.levelConfig[this.level] || this.levelConfig['beginner']; }
  get activeSteps() { return this.inputMode === 'voice' ? this.processingStepsVoice : this.processingSteps; }

  setMode(mode: InputMode) {
    this.inputMode = mode;
    this.error = '';
  }

  // Voice submission
  onAudioBlob(blob: Blob) {
    this.startProcessing();
    const fd = new FormData();
    fd.append('audio', blob, 'recording.webm');
    fd.append('session_id', String(this.sessionId));
    fd.append('question_id', String(this.currentQuestion.id));
    this.api.submitAudio(fd).subscribe({
      next: res => this.onResult(res),
      error: err => this.onError(err)
    });
  }

  // Text submission
  submitText() {
    if (!this.textAnswer.trim()) {
      this.error = 'Please type your answer before submitting.';
      return;
    }
    if (this.textAnswer.trim().length < 20) {
      this.error = 'Your answer is too short. Please provide more detail.';
      return;
    }
    this.startProcessing();
    this.api.submitText(this.sessionId, this.currentQuestion.id, this.textAnswer.trim()).subscribe({
      next: res => this.onResult(res),
      error: err => this.onError(err)
    });
  }

  nextQuestion() {
    this.error = '';
    this.textAnswer = '';
    this.aiAnalysis = null;
    this.aiAnalysisLoading = false;
    clearInterval(this.aiPollInterval);
    if (this.currentIndex < this.questions.length - 1) {
      this.currentIndex++;
      this.lastResult = null;
      this.state = 'ready';
    } else {
      this.state = 'done';
      this.api.completeSession(this.sessionId).subscribe({
        next: () => this.router.navigate(['/practice', this.sessionId, 'results']),
        error: () => this.router.navigate(['/practice', this.sessionId, 'results'])
      });
    }
  }

  private startProcessing() {
    this.state = 'processing';
    this.processingStep = 0;
    this.dotsInterval = setInterval(() => {
      this.processingStep = (this.processingStep + 1) % this.activeSteps.length;
    }, 2500);
  }

  private onResult(res: any) {
    clearInterval(this.dotsInterval);
    this.lastResult = res;
    this.aiAnalysis = null;
    this.aiAnalysisLoading = true;
    this.state = 'feedback';

    // Request AI analysis (single call, server generates synchronously)
    if (res.response_id) {
      this.api.getAiFeedback(res.response_id).subscribe({
        next: (data: any) => {
          if (data.ready && data.ai_analysis) {
            this.aiAnalysis = data.ai_analysis;
          }
          this.aiAnalysisLoading = false;
        },
        error: () => {
          this.aiAnalysisLoading = false;
        }
      });
    } else {
      this.aiAnalysisLoading = false;
    }
  }

  private onError(err: any) {
    clearInterval(this.dotsInterval);
    this.error = err.error?.error || 'Analysis failed. Please try again.';
    this.state = 'ready';
  }

  scoreColor(s: number) { return s >= 70 ? '#059669' : s >= 40 ? '#d97706' : '#dc2626'; }
  scoreBg(s: number) { return s >= 70 ? '#f0fdf4' : s >= 40 ? '#fffbeb' : '#fef2f2'; }
  scoreLabel(s: number) { return s >= 80 ? 'Excellent' : s >= 60 ? 'Good' : s >= 40 ? 'Fair' : 'Needs Work'; }
}
