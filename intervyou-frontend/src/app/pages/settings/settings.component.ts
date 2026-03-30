import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { ApiService } from '../../core/api.service';
import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit {
  profileForm = this.fb.group({ name: ['', Validators.required], email: ['', [Validators.required, Validators.email]] });
  pwForm = this.fb.group({ old_password: ['', Validators.required], new_password: ['', [Validators.required, Validators.minLength(8)]] });

  profileMsg = ''; profileErr = '';
  pwMsg = ''; pwErr = '';
  saving = false; savingPw = false;

  constructor(private fb: FormBuilder, private api: ApiService, private auth: AuthService) {}

  ngOnInit() {
    this.auth.currentUser$.subscribe(u => {
      if (u) this.profileForm.patchValue({ name: u.name, email: u.email });
    });
  }

  saveProfile() {
    if (this.profileForm.invalid) return;
    this.saving = true; this.profileMsg = ''; this.profileErr = '';
    this.api.updateProfile(this.profileForm.value).subscribe({
      next: u => { this.profileMsg = 'Profile updated!'; this.saving = false; },
      error: () => { this.profileErr = 'Failed to update profile.'; this.saving = false; }
    });
  }

  changePassword() {
    if (this.pwForm.invalid) return;
    this.savingPw = true; this.pwMsg = ''; this.pwErr = '';
    this.api.changePassword(this.pwForm.value).subscribe({
      next: () => { this.pwMsg = 'Password changed!'; this.pwForm.reset(); this.savingPw = false; },
      error: err => { this.pwErr = err.error?.error || 'Failed to change password.'; this.savingPw = false; }
    });
  }
}
