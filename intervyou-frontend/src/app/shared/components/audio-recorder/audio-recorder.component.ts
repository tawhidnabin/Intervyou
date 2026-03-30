import { Component, EventEmitter, Input, OnDestroy, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-audio-recorder',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatIconModule],
  template: `
    <div class="recorder">
      <div class="timer" *ngIf="recording">
        <mat-icon class="pulse">fiber_manual_record</mat-icon>
        {{ elapsed }}s
      </div>

      <button mat-fab color="warn" (click)="startRecording()"
        *ngIf="!recording" [disabled]="disabled" aria-label="Start recording">
        <mat-icon>mic</mat-icon>
      </button>

      <button mat-fab color="primary" (click)="stopRecording()"
        *ngIf="recording" aria-label="Stop recording">
        <mat-icon>stop</mat-icon>
      </button>

      <p class="hint" *ngIf="!recording && !disabled">Click the microphone to start recording</p>
      <p class="hint recording-hint" *ngIf="recording">Recording... click stop when done</p>
      <p class="error" *ngIf="permissionError">{{ permissionError }}</p>
    </div>
  `,
  styles: [`
    .recorder { display:flex; flex-direction:column; align-items:center; gap:12px; padding:16px; }
    .timer { display:flex; align-items:center; gap:6px; font-size:18px; font-weight:600; color:#f44336; }
    .pulse { animation: pulse 1s infinite; color:#f44336; }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
    .hint { color:#666; font-size:13px; margin:0; }
    .recording-hint { color:#f44336; }
    .error { color:#f44336; font-size:13px; }
  `]
})
export class AudioRecorderComponent implements OnDestroy {
  @Input() disabled = false;
  @Output() audioBlob = new EventEmitter<Blob>();

  recording = false;
  elapsed = 0;
  permissionError = '';

  private mediaRecorder?: MediaRecorder;
  private chunks: Blob[] = [];
  private timer?: any;
  private stream?: MediaStream;

  async startRecording() {
    this.permissionError = '';
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.chunks = [];
      this.mediaRecorder = new MediaRecorder(this.stream, { mimeType: 'audio/webm' });
      this.mediaRecorder.ondataavailable = e => { if (e.data.size > 0) this.chunks.push(e.data); };
      this.mediaRecorder.onstop = () => {
        const blob = new Blob(this.chunks, { type: 'audio/webm' });
        this.audioBlob.emit(blob);
      };
      this.mediaRecorder.start();
      this.recording = true;
      this.elapsed = 0;
      this.timer = setInterval(() => this.elapsed++, 1000);
    } catch (e) {
      this.permissionError = 'Microphone access denied. Please allow microphone permissions.';
    }
  }

  stopRecording() {
    if (this.mediaRecorder && this.recording) {
      this.mediaRecorder.stop();
      this.stream?.getTracks().forEach(t => t.stop());
      clearInterval(this.timer);
      this.recording = false;
    }
  }

  ngOnDestroy() {
    this.stopRecording();
  }
}
