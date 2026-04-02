import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

const BASE = environment.apiUrl;

@Injectable({ providedIn: 'root' })
export class ApiService {
  constructor(private http: HttpClient) {}

  // Questions
  getQuestions(level = 'beginner', category = 'all', count = 5): Observable<any[]> {
    return this.http.get<any[]>(`${BASE}/questions/?level=${level}&category=${category}&count=${count}`);
  }

  // Sessions
  startSession(jobRole: string, level: string = 'beginner'): Observable<any> {
    return this.http.post<any>(`${BASE}/sessions/start`, { job_role: jobRole, level });
  }
  submitAudio(formData: FormData): Observable<any> {
    return this.http.post<any>(`${BASE}/analysis/submit`, formData);
  }
  submitText(sessionId: number, questionId: number, answerText: string): Observable<any> {
    return this.http.post<any>(`${BASE}/analysis/submit-text`, {
      session_id: sessionId, question_id: questionId, answer_text: answerText
    });
  }
  completeSession(id: number): Observable<any> {
    return this.http.post<any>(`${BASE}/sessions/${id}/complete`, {});
  }
  getSessions(): Observable<any[]> {
    return this.http.get<any[]>(`${BASE}/sessions/`);
  }
  getSession(id: number): Observable<any> {
    return this.http.get<any>(`${BASE}/sessions/${id}`);
  }

  // User
  getDashboardStats(): Observable<any> {
    return this.http.get<any>(`${BASE}/user/dashboard-stats`);
  }
  getMe(): Observable<any> {
    return this.http.get<any>(`${BASE}/user/me`);
  }
  updateProfile(data: any): Observable<any> {
    return this.http.put<any>(`${BASE}/user/profile`, data);
  }
  changePassword(data: any): Observable<any> {
    return this.http.post<any>(`${BASE}/user/change-password`, data);
  }

  // Misc
  sendContact(email: string, message: string): Observable<any> {
    return this.http.post<any>(`${BASE}/contact`, { email, message });
  }

  // Chatbot
  sendChatMessage(message: string, history: any[] = []): Observable<any> {
    return this.http.post<any>(`${BASE}/chatbot/message`, { message, history });
  }
  getSessionFeedback(data: any): Observable<any> {
    return this.http.post<any>(`${BASE}/chatbot/session-feedback`, data);
  }
  getAiFeedback(responseId: number): Observable<any> {
    return this.http.post<any>(`${BASE}/analysis/ai-feedback/${responseId}`, {});
  }
}
