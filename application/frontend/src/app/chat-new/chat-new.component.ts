import { Component, OnInit } from '@angular/core';
import { AppService } from '../app.service';

@Component({
  selector: 'app-chat',
  templateUrl: './chat-new.component.html',
  styleUrls: ['./chat-new.component.css'],
})
export class ChatNewComponent implements OnInit {
  title = 'NLP Chatbot';
  topic: string = 'All';
  message = '';

  constructor(public appService: AppService) {}

  ngOnInit() {}

  sendMessage() {
    const data = { user_message: this.message };
    this.appService.messageArray.push({ name: 'user', message: this.message });
    this.appService.get_response(data).subscribe((response: any) => {
      this.appService.messageArray.push({
        name: 'bot',
        message: response.chat_bot_response,
      });
    });
    this.message = '';
  }

  reset_filter() {
    this.topic = 'all';
  }
}
