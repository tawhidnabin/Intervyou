import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators, AbstractControl, ValidationErrors } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../core/auth.service';

function passwordStrengthValidator(control: AbstractControl): ValidationErrors | null {
  const v = control.value || '';
  if (v.length < 8) return null;
  if (!/[A-Z]/.test(v)) return { weak: 'Must include an uppercase letter.' };
  if (!/[a-z]/.test(v)) return { weak: 'Must include a lowercase letter.' };
  if (!/[0-9]/.test(v)) return { weak: 'Must include a number.' };
  return null;
}

function passwordMatchValidator(group: AbstractControl): ValidationErrors | null {
  const pw = group.get('password')?.value;
  const confirm = group.get('confirmPassword')?.value;
  if (pw && confirm && pw !== confirm) {
    return { mismatch: true };
  }
  return null;
}

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent {
  form: FormGroup;
  loading = false;
  error = '';

  constructor(private fb: FormBuilder, private auth: AuthService, private router: Router) {
    this.form = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(2), Validators.maxLength(100)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8), passwordStrengthValidator]],
      confirmPassword: ['', [Validators.required]]
    }, { validators: passwordMatchValidator });
  }

  get passwordErrors(): string {
    const ctrl = this.form.get('password');
    if (!ctrl?.touched || !ctrl?.errors) return '';
    if (ctrl.errors['required']) return 'Password is required.';
    if (ctrl.errors['minlength']) return 'Password must be at least 8 characters.';
    if (ctrl.errors['weak']) return ctrl.errors['weak'];
    return '';
  }

  get confirmErrors(): string {
    const ctrl = this.form.get('confirmPassword');
    if (!ctrl?.touched) return '';
    if (ctrl?.errors?.['required']) return 'Please confirm your password.';
    if (this.form.errors?.['mismatch'] && ctrl?.touched) return 'Passwords do not match.';
    return '';
  }

  submit() {
    this.form.markAllAsTouched();
    if (this.form.invalid) return;

    this.loading = true;
    this.error = '';
    const { name, email, password } = this.form.value;
    this.auth.register(name, email, password).subscribe({
      next: () => this.router.navigate(['/dashboard']),
      error: (err: any) => {
        this.error = err.error?.error || 'Registration failed. Please try again.';
        this.loading = false;
      }
    });
  }
}
