import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.scss']
})
export class ContactComponent {
  form = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    message: ['', [Validators.required, Validators.minLength(10)]]
  });
  loading = false; success = false; error = '';

  constructor(private fb: FormBuilder, private api: ApiService) {}

  submit() {
    if (this.form.invalid) return;
    this.loading = true; this.error = '';
    const { email, message } = this.form.value;
    this.api.sendContact(email!, message!).subscribe({
      next: () => { this.success = true; this.loading = false; this.form.reset(); },
      error: () => { this.error = 'Failed to send message. Please try again.'; this.loading = false; }
    });
  }
}
