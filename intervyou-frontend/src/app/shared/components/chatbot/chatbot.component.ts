import { Component, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../core/api.service';
import { AuthService } from '../../../core/auth.service';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.scss']
})
export class ChatbotComponent {
  @ViewChild('messagesContainer') messagesContainer!: ElementRef;

  isOpen = false;
  isLoading = false;
  userInput = '';
  messages: ChatMessage[] = [];
  isLoggedIn = false;

  suggestions = [
    'How do I answer "Tell me about yourself"?',
    'What is the STAR method?',
    'Tips for video interviews',
    'How to handle salary questions'
  ];

  constructor(private api: ApiService, private auth: AuthService) {
    this.auth.currentUser$.subscribe(u => this.isLoggedIn = !!u);
  }

  toggle() {
    this.isOpen = !this.isOpen;
    if (this.isOpen && this.messages.length === 0) {
      this.messages.push({
        role: 'assistant',
        content: 'Hi! I\'m your AI Interview Coach. Ask me anything about interview preparation — question strategies, answer structures, delivery tips, or career advice.',
        timestamp: new Date()
      });
    }
  }

  sendMessage(text?: string) {
    const msg = (text || this.userInput).trim();
    if (!msg || this.isLoading) return;

    this.messages.push({ role: 'user', content: msg, timestamp: new Date() });
    this.userInput = '';
    this.isLoading = true;
    this.scrollToBottom();

    const history = this.messages.map(m => ({ role: m.role, content: m.content }));

    this.api.sendChatMessage(msg, history).subscribe({
      next: res => {
        this.messages.push({ role: 'assistant', content: res.response, timestamp: new Date() });
        this.isLoading = false;
        this.scrollToBottom();
      },
      error: () => {
        this.messages.push({
          role: 'assistant',
          content: 'Sorry, I could not connect to the AI service. Please make sure Ollama is running (ollama serve) and try again.',
          timestamp: new Date()
        });
        this.isLoading = false;
        this.scrollToBottom();
      }
    });
  }

  useSuggestion(s: string) {
    this.sendMessage(s);
  }

  clearChat() {
    this.messages = [{
      role: 'assistant',
      content: 'Chat cleared. How can I help you prepare for your interview?',
      timestamp: new Date()
    }];
  }

  onKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  private scrollToBottom() {
    setTimeout(() => {
      if (this.messagesContainer) {
        const el = this.messagesContainer.nativeElement;
        el.scrollTop = el.scrollHeight;
      }
    }, 50);
  }
}
